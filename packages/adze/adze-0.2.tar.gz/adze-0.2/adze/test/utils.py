from typing import cast
import random
import numpy
from numpy.typing import NDArray
from numpy import pi, cos, sin, floating
from numpy.linalg import norm

import adze


PRNG = numpy.random.RandomState(12345)
PRNG_PYRANDOM = random.Random(12345)


# numerical tolerances for pass/warn/fail tests
TOL_WARN = 1e-8
TOL_FAIL = 1e-4

# minimum volume allowed for test polyhedra
MIN_VOLUME = 1e-8

# order of polynomial integration for all tests
POLY_ORDER = 0


def gen_torus_brep(
        n_theta: int = 20,
        n_phi: int = 20,
        r0: float = 1.0,
        r1: float = 0.1,
        ) -> tuple[NDArray[numpy.float64], NDArray[numpy.intp]]:
    """
    Generate a boundary representation for an elliptical torus
    """
    # Generate vertices
    theta, phi = numpy.meshgrid(
        numpy.linspace(0, 2*pi, n_theta, endpoint=False),
        numpy.linspace(0, 2*pi, n_phi, endpoint=False),
        )
    theta = theta.ravel(order='F')
    phi = phi.ravel(order='F')

    vertices = numpy.column_stack((
        (r0 + r1 * cos(theta)) * cos(phi),
        (r0 + r1 * cos(theta)) * sin(phi),
        r1 * sin(theta),
        ))

    # Generate faces
    i, j = numpy.meshgrid(numpy.arange(n_phi), numpy.arange(n_theta), indexing='ij')

    a = i * n_theta + j
    b = ((i + 1) % n_phi) * n_theta
    c = (j + 1) % n_theta

    aa = numpy.hstack((a, a)).ravel()
    bb = numpy.hstack((b + j, b + c)).ravel()
    cc = numpy.hstack((b + c, c + i * n_theta)).ravel()

    faces = numpy.column_stack((aa, bb, cc))

    return vertices, faces


def tetrahedron_volume(vertices: NDArray[numpy.floating] | list[NDArray[numpy.floating]]) -> float:
    ad, bd, cd = vertices[0:3] - vertices[3]
    return -ad @ numpy.cross(bd, cd) / 6


def flip_plane(plane: adze.plane_t) -> adze.plane_t:
    return (-plane[0], -plane[1])


def rand_tetrahedron_vertices(min_volume: float = MIN_VOLUME) -> NDArray[numpy.float64]:
    # generates a random tetrahedron with vertices on the unit sphere,
    # guaranteeing a volume of at least min_volume
    volume = 0.0
    while volume < min_volume:
        verts = [rand_unit_vector() for _ in range(4)]
        volume = tetrahedron_volume(verts)
        if volume < 0:
            verts[2], verts[3] = verts[3], verts[2]
            volume = -volume
    return numpy.asarray(verts)


def build_rand_tetrahedron(min_volume: float = MIN_VOLUME) -> adze.poly_t:
    return adze.build_tetrahedron(rand_tetrahedron_vertices(min_volume=min_volume))


def rand_unit_vector() -> NDArray[numpy.float64]:
    # generates a random, isotropically distributed unit vector
    s: numpy.floating | float  = 0.0
    while s == 0.0:
        v = PRNG.randn(3)
        s = norm(v)
    return v / s


def get_centroid(poly: adze.poly_t) -> NDArray[numpy.floating]:
    """
    Average the vertices to get the centroid
    """
    centroid = numpy.sum(poly['vertices'], axis=0) / poly['vertices'].shape[0]
    return centroid


def gen_plane_through_centroid(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a randomly-oriented plane passing through the polyhedron's centroid
    """
    centroid = get_centroid(poly)
    n = rand_unit_vector()
    d = cast(numpy.floating, -n @ centroid)
    return n, d


def gen_plane_from_face(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a plane coplanar with one of the polyhedron's faces
    """
    # make a plane coplanar with a face of the poly
    v0 = PRNG.randint(poly['vertices'].shape[0])
    v1, v2 = PRNG_PYRANDOM.sample(list(poly['neighbors'][v0]), 2)
    points = (poly['vertices'][vi] for vi in (v0, v1, v2))
    return gen_plane_through_points(*points)


def gen_plane_through_centroid_and_edge(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a plane through an edge of the polyhedron and the polyhedron's centroid
    """
    v0 = PRNG.randint(poly['vertices'].shape[0])
    v1 = PRNG.choice(poly['neighbors'][v0])
    p0 = poly['vertices'][v0]
    p1 = poly['vertices'][v1]
    centroid = get_centroid(poly)
    return gen_plane_through_points(p0, p1, centroid)


def gen_plane_through_edge(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a plane through an edge of the polyhedron, but otherwise randomly oriented
    """
    v0 = PRNG.randint(poly['vertices'].shape[0])
    v1 = PRNG.choice(poly['neighbors'][v0])
    p0 = poly['vertices'][v0]
    p1 = poly['vertices'][v1]
    return gen_plane_through_points(p0, p1, rand_unit_vector())


def gen_plane_through_centroid_and_vertex(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a plane through a vertex and the centroid, but otherwise randomly oriented
    """
    vertices = poly['vertices']
    p0 = vertices[PRNG.choice(vertices.shape[0])]
    centroid = get_centroid(poly)
    return gen_plane_through_points(p0, centroid, rand_unit_vector())


def gen_plane_through_vertex(
        poly: adze.poly_t,
        ) -> adze.plane_t:
    """
    Generate a plane passing through a vertex, but otherwise randomly oriented
    """
    vertices = poly['vertices']
    p0 = vertices[PRNG.choice(vertices.shape[0])]
    n = rand_unit_vector()
    d = -n @ p0
    return n, d


def gen_plane_through_points(
        p0: NDArray[floating],
        p1: NDArray[floating],
        p2: NDArray[floating],
        ) -> adze.plane_t:
    """
    Generate a plane passing through three given points
    """
    n = numpy.cross(p1 - p0, p2 - p0)
    n /= norm(n) + 1e-40
    d = -n @ p0
    return n, d


plane_generators = [
    gen_plane_through_centroid,
    gen_plane_from_face,
    gen_plane_through_centroid_and_edge,
    gen_plane_through_edge,
    gen_plane_through_centroid_and_vertex,
    gen_plane_through_vertex,
    ]

