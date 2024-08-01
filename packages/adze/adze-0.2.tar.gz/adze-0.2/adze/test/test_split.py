from collections.abc import Callable
import warnings
import logging

import pytest

import numpy
from numpy.typing import NDArray
from numpy import floating
from numpy.linalg import norm
from numpy.testing import assert_allclose

import adze
import adze.util

from .utils import TOL_FAIL, TOL_WARN, PRNG, MIN_VOLUME, flip_plane, tetrahedron_volume
from .utils import build_rand_tetrahedron, gen_plane_through_centroid, plane_generators, gen_torus_brep


logger = logging.getLogger(__name__)


def test_manual_tetrahedron(poly_order: int) -> None:
    tet = adze.build_tetrahedron([
        [0,0,0],
        [2,0,0],
        [0,2,0],
        [0,0,2]])

    volume = tetrahedron_volume(tet['vertices'])
    logger.debug(f'Splitting manual tetrahedron {tet}')
    logger.debug(f'volume {volume}')

    plane = numpy.array((-1, 0, 0)), 1
    p_left, p_right = adze.split(tet, plane)

    logger.debug(f'left {p_left}')
    logger.debug(f'right {p_right}')

    adze.util.check_poly(tet)
    adze.util.check_poly(p_left)
    adze.util.check_poly(p_right)

    m0 = adze.get_moments(tet, 0)
    ml = adze.get_moments(p_left, 0)
    mr = adze.get_moments(p_right, 0)

    logger.debug(f'0th moments: tot {m0[0]}, left {ml[0]}, right {mr[0]}')
    assert m0 == pytest.approx(volume, abs=TOL_FAIL)
    check_split_moments(tet, p_left, p_right, poly_order)


def test_manual_pyramid(poly_order: int) -> None:
    vertices = numpy.array([
        [0, 0, 1],
        [1, 1, 0],
        [1, -1, 0],
        [-1, -1, 0],
        [-1, 1, 0],
        ])
    faces = [
        [0, 1, 2],
        [0, 2, 3],
        [0, 3, 4],
        [0, 4, 1],
        [4, 3, 2, 1],
        ]

    # initialize a general polyhedron
    poly = adze.build_polyhedron(vertices, faces)       # type: ignore  # (mypy error?)
    adze.util.check_poly(poly)

    brep = adze.boundary_from_poly(poly)
    logger.info(f'Round-trip converted pyramid: {brep}')
    #adze.util.plot_brep(brep)

    stack_split(poly, poly_order)


def test_tetrahedrons_through_centroid(poly_order: int) -> None:
    """
    Splits some tetrahedrons through their centroids and
      checks if each two resulting volumes sum to the original
    """

    # Generate random tetrahedrons and clip planes
    ntets = 100
    polys = [build_rand_tetrahedron() for _ in range(ntets)]
    plane = gen_plane_through_centroid(polys[ntets//7])

    # split them all with the same plane
    poly12 = [adze.split(p, plane) for p in polys]
    poly1, poly2 = zip(*poly12, strict=True)

    for orig, p1, p2 in zip(polys, poly1, poly2, strict=True):
        adze.util.check_poly(orig)
        adze.util.check_poly(p1)
        adze.util.check_poly(p2)
        check_split_moments(orig, p1, p2, poly_order)


def test_manual_nonconvex(poly_order: int, n_zigs: int = 3, z_offset: float = 0.1) -> None:
    """
    Splits a non-convex polyhedron and checks if the resulting
      volumes add up to the original
    """
    # manually create a non-convex polyhedron
    num_verts = 4 * n_zigs
    vertices = numpy.empty((num_verts, 3), dtype=float)
    neighbors = numpy.empty((num_verts, 3), dtype=int)

    for v in range(n_zigs):
        m = n_zigs - v - 1
        v0 = numpy.array([v, v % 2 + z_offset, 0])
        v1 = numpy.array([m, m % 2, 0])
        vertices[v + 0 * n_zigs] = v0
        vertices[v + 1 * n_zigs] = v1
        vertices[v + 2 * n_zigs] = v0 + (0, 0, 1)
        vertices[v + 3 * n_zigs] = v1 + (0, 0, 1)

    nz2 = 2 * n_zigs
    for v in range(nz2):
        neighbors[v] = ((v + 1) % nz2,
                        (v - 1) % nz2,
                        v + nz2)
        neighbors[v + nz2] = neighbors[v][[1, 0, 2]] + (nz2, nz2, -nz2)
    poly = {
        'vertices': vertices,
        'neighbors': neighbors,
        }

    logger.debug("Checking poly...")
    adze.util.check_poly(poly)
    logger.debug("poly is valid.")

    #
    # Perform splits along three axes
    #
    def split_and_check(poly: adze.poly_t, plane: adze.plane_t, poly_order: int = 0) -> None:
        poly_l = adze.clip(poly, plane)
        poly_r = adze.clip(poly, flip_plane(plane))
        check_split_moments(poly, poly_l, poly_r, poly_order)

    # split along the x-axis (two single connected components)
    split_and_check(poly, (numpy.array((1, 0, 0)), -0.5 * (n_zigs - 1)), poly_order)

    # split along the z-axis (two single connected components)
    split_and_check(poly, (numpy.array((0, 0, 1)), -0.5), poly_order)

    # split along the y-axis (multiple connected components)
    split_and_check(poly, (numpy.array((0, 1, 0)), -0.5 * (1.0 + z_offset)), poly_order)


def test_torus(poly_order: int) -> None:
    """
    Recursively split a torus with random degenerate cut planes until the pieces
      are smaller than `MIN_VOLUME`, then check that the moments add up properly.

    This checks `build_polyhedron()` with for >3 edges per vertex and non-convex
      geometry.
    """
    vertices, faces = gen_torus_brep(n_theta=20, n_phi=20, r0=1.0, r1=0.1)

    # Shift center away from the origin, to avoid 0-valued moments
    vertices += (0.5, 0.7, 0.9)

    opoly = adze.build_polyhedron(vertices, faces)
#    adze.util.check_poly(opoly)

    brep = adze.boundary_from_poly(opoly)
    logger.debug(f'Round-trip converted torus: {brep}')
    #adze.util.plot_brep(brep)

    stack_split(opoly, poly_order)


def test_recursive(poly_order: int, num_trials: int = 10, max_depth: int = 6) -> None:
    """
    Starting with a tetrahedron, recusively split until the pieces
     are smaller than `MIN_VOLUME` or have been split more than `max_depth` times,
     then check that the moments add up as expected.
    """
    logger.info(f'Recursively splitting {num_trials} tetrahedra, maximum depth {max_depth}:')
    logger.info(' - Through centroid')
    for _ in range(num_trials):
        stack_split(build_rand_tetrahedron(), poly_order, plane_fun=gen_plane_through_centroid, max_depth=max_depth)

    logger.info(' - Through degenerate plane')
    for _ in range(num_trials):
        stack_split(build_rand_tetrahedron(), poly_order, max_depth=max_depth)

    logger.info(' - Through perturbed plane')
    for t in range(num_trials):
        perturb = 10 ** -(1 + t % 16)
        stack_split(build_rand_tetrahedron(), poly_order, perturb=perturb, max_depth=max_depth)


def check_split_moments(
        original_poly: adze.poly_t,
        left_poly: adze.poly_t,
        right_poly: adze.poly_t,
        poly_order: int = 0,
        ) -> tuple[NDArray[floating], NDArray[floating], NDArray[floating]]:
    m0, ml, mr = (adze.get_moments(x, poly_order) for x in (original_poly, left_poly, right_poly))
    logger.debug(f'Check: original {m0[0]} parts {(ml[0], mr[0])} sum {ml[0] + mr[0]}')

    # Make sure each part is smaller than the whole
    if not ml[0] < m0[0] * (1.0 + TOL_WARN):
        warnings.warn('ml[0] < m0[0]', stacklevel=1)
        assert(ml[0] < m0[0] * (1.0 + TOL_FAIL))
    if not mr[0] < m0[0] * (1.0 + TOL_WARN):
        warnings.warn('mr[0] < m0[0]', stacklevel=1)
        assert(mr[0] < m0[0] * (1.0 + TOL_FAIL))

    # make sure the sum of moments equals the original
    mtot = ml + mr
    assert_allclose(m0, mtot, atol=TOL_FAIL)
#    if not numpy.all(diff < TOL_FAIL):
#        logger.error(f'diff failed: {diff} \n original {m0} \n left {ml} \n right {mr}')
#        assert(False)
    if not numpy.allclose(m0, mtot, atol=TOL_WARN):
        warnings.warn('Moments outside tolerance', stacklevel=1)

    return m0, ml, mr


def stack_split(
        poly: adze.poly_t,
        poly_order: int,
        plane_fun: Callable | None = None,
        perturb: float = 0,
        max_depth: int = 10,
        ) -> None:
    stack = [(poly, 0)]

    i = 0
    while stack:
        i += 1
        poly, depth = stack.pop()

        # pick a plane
        if plane_fun is None:
            pfun_used = PRNG.choice(plane_generators)       # type: ignore
            plane = pfun_used(poly)
            while norm(plane[0]) == 0:
                pfun_used = PRNG.choice(plane_generators)   # type: ignore
                plane = pfun_used(poly)
            plane = list(plane)
            logger.debug(f'used {pfun_used}')
        else:
            plane = list(plane_fun(poly))

        # perturb the plane
        plane[0] *= 1 + perturb * (PRNG.rand() - 0.5)
        plane[1] *= 1 + perturb * (PRNG.rand() - 0.5)

        # split the poly
        poly_l = adze.clip(poly, plane)
        poly_r = adze.clip(poly, flip_plane(plane))
        m0, ml, mr = check_split_moments(poly, poly_l, poly_r, poly_order)

        logger.debug(f'nstack = {len(stack)}, depth = {depth}, '
                     f'opoly = {m0[0]:.10e}, p1 = {ml[0]:.10e}, p2 = {mr[0]:.10e}, '
                     f'err = {abs(1.0 - m0[0]/(ml[0] + mr[0])):.10e}')

        # add the children to the stack if they are big enough
        if depth < max_depth:
            if ml[0] > MIN_VOLUME:
                stack.append((poly_l, depth + 1))
            if mr[0] > MIN_VOLUME:
                stack.append((poly_r, depth + 1))
        if i % 300 == 0:
            logger.info(f'Stack split iter {i} length {len(stack)} depth {depth}')
