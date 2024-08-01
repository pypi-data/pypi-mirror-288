"""
Benchmarking, run with `python3 -m adze.test.benchmark`

TODO: Consider using pytest-benchmark?
"""
from collections.abc import Callable
import logging

import numpy
from numpy.typing import NDArray

import adze
import adze.util

from .utils import build_rand_tetrahedron, rand_tetrahedron_vertices


logger = logging.getLogger(__name__)


def test_split(benchmark: Callable) -> None:
    poly = build_rand_tetrahedron()
    faceset = adze.planes_from_tetrahedron(rand_tetrahedron_vertices())
    benchmark(adze.clip, poly, faceset[0])


def test_split_bulk_1000(benchmark: Callable) -> None:
    NUM_TRIALS = 1000
    polys_bulk = [build_rand_tetrahedron() for _ in range(NUM_TRIALS)]
    faceset = adze.planes_from_tetrahedron(rand_tetrahedron_vertices())
    bulk = {
        'vertices': numpy.vstack([p['vertices'] for p in polys_bulk]),
        'neighbors': numpy.vstack([p['neighbors'] for p in polys_bulk]) + numpy.arange(NUM_TRIALS).repeat(4)[:, None] * 4,
        }
    benchmark(adze.clip, bulk, faceset[0])



def get_intersection_moments(poly: adze.poly_t, faces: NDArray[numpy.intp], poly_order: int) -> NDArray[numpy.float64]:
    # Clip the first tetrahedron using the faces of the second
    for face in faces:
        poly = adze.clip(poly, face)

    # find the moments (up to quadratic order) of the clipped poly
    om = adze.get_moments(poly, poly_order)
    return om


def test_intersection(benchmark: Callable, poly_order: int = 0) -> None:
    """
    Benchmark intersection between pairs of tetrahedra
    """
    poly = build_rand_tetrahedron()
    faces = adze.planes_from_tetrahedron(rand_tetrahedron_vertices())
    benchmark(get_intersection_moments, poly, faces, poly_order)

