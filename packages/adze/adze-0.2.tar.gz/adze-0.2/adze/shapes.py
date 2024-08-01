import numpy
from numpy.linalg import norm
from numpy.typing import ArrayLike

from . import poly_t, plane_t


def build_tetrahedron(vertices: ArrayLike) -> poly_t:
    """
    Build a Schelegel-representation tetrahedron.

    Args:
        vertices: 4x3 array, representing the vertex coordinates.

    Returns:
        Tetrahedron in Schelgel representation.
    """
    poly = {
        'vertices': numpy.array(vertices, dtype=float),
        'neighbors': numpy.array((
            (1, 3, 2),
            (2, 3, 0),
            (0, 3, 1),
            (1, 2, 0)), dtype=int),
        }
    return poly


def build_box(box_corners: ArrayLike) -> poly_t:
    """
    Build a Schelegel-representation box.

    Args:
        box_corners: 2x3 array, representing the vertex coordinates of
            two diagonally-opposite corners of the box.

    Returns:
        Box in Schelgel representation.
    """
    neighbors = [
        [1, 4, 3],
        [2, 5, 0],
        [3, 6, 1],
        [0, 7, 2],
        [7, 0, 5],
        [4, 1, 6],
        [5, 2, 7],
        [6, 3, 4],
        ]

    box_corners = numpy.asarray(box_corners)
    vertices = [
        [box_corners[0, 0], box_corners[0, 1], box_corners[0, 2]],
        [box_corners[1, 0], box_corners[0, 1], box_corners[0, 2]],
        [box_corners[1, 0], box_corners[1, 1], box_corners[0, 2]],
        [box_corners[0, 0], box_corners[1, 1], box_corners[0, 2]],
        [box_corners[0, 0], box_corners[0, 1], box_corners[1, 2]],
        [box_corners[1, 0], box_corners[0, 1], box_corners[1, 2]],
        [box_corners[1, 0], box_corners[1, 1], box_corners[1, 2]],
        [box_corners[0, 0], box_corners[1, 1], box_corners[1, 2]],
        ]

    return {
        'neighbors': numpy.array(neighbors, dtype=int),
        'vertices': numpy.array(vertices, dtype=float),
        }


def planes_from_box(box_corners: ArrayLike) -> list[plane_t]:
    """
    Construct a list of planes corresponding to the faces of a box.

    Args:
        box_corners: 2x3 array, representing the vertex coordinates of
            two diagonally-opposite corners of the box.

    Returns:
        List of planes, facing inwards.
    """
    box_corners = numpy.asarray(box_corners)
    faces = [
        (( 0,  0,  1), -box_corners[0, 2]),
        (( 0,  0, -1),  box_corners[1, 2]),
        (( 0,  1,  0), -box_corners[0, 1]),
        (( 0, -1,  0),  box_corners[1, 1]),
        (( 1,  0,  0), -box_corners[0, 0]),
        ((-1,  0,  0),  box_corners[1, 0]),
        ]

    return [(numpy.array(n), d) for n, d in faces]


def planes_from_tetrahedron(vertices: ArrayLike) -> list[plane_t]:
    """
    Construct a list of planes corresponding to the faces of a tetrahedron.

    Args:
        vertices: 4x3 array, representing the vertex coordinates.

    Returns:
        List of planes, facing inwards.
    """
    verts = numpy.asarray(vertices, dtype=float)
    vset_inds = numpy.array((
        [3, 1, 2, 1],
        [2, 0, 3, 2],
        [1, 3, 0, 3],
        [0, 2, 1, 0]))
    vertsets = numpy.moveaxis(numpy.dstack([verts[v] for v in vset_inds]), 2, 0)
    ab = vertsets[:, 0, :] - vertsets[:, 1, :]
    cd = vertsets[:, 2, :] - vertsets[:, 3, :]

    n = numpy.cross(ab, cd)
    n /= norm(n, axis=1)[:, None]
    centers = numpy.sum(vertsets[:, :3, :], axis=1) / 3
    d = -numpy.sum(n * centers, axis=1)

    return list(zip(n, d, strict=True))
