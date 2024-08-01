import numpy
from numpy import sin, cos
from numpy.typing import ArrayLike

from . import poly_t


def rotate(poly: poly_t, theta: float, axis: int) -> poly_t:
    """
    Rotate the polyhedron around an axis.

    Args:
        poly: Polyhedron to rotate. Changed in-place.
        theta: Angle to rotate by (radians).
        axis: Axis to rotate around (0-2).

    Returns:
        Rotated polyhedron.
        Data is altered in-place but also returned for convenience.
    """
    s, c = sin(theta), cos(theta)
    v0 = poly['vertices'][:, axis - 2].copy()
    v1 = poly['vertices'][:, axis - 1]
    poly['vertices'][:, axis - 2] = c * v0 - s * v1
    poly['vertices'][:, axis - 1] = s * v1 + c * v0
    return poly


def translate(poly: poly_t, shift: ArrayLike) -> poly_t:
    """
    Translate the polyhedron by a vector.

    Args:
        poly: Polyhedron to translate. Changed in-place.
        shift: Vector to translate by.

    Returns:
        Translated polyhedron.
        Data is altered in-place but also returned for convenience.
    """
    poly['vertices'] += shift
    return poly


def scale(poly: poly_t, factor: ArrayLike | float) -> poly_t:
    """
    Scale the polyhedron.
    Can scale by a single value, or scale each axis individually

    Args:
        poly: Polyhedron to scale. Changed in-place.
        factor: Scalar or vector to scale by.

    Returns:
        Scaled polyhedron.
        Data is altered in-place but also returned for convenience.
    """
    poly['vertices'] *= factor
    return poly


def affine(poly: poly_t, xform: ArrayLike) -> poly_t:
    """
    Perform arbitrary affine trasnformation on the polyhedron.

    Args:
        poly: Polyhedron to transform. Changed in-place.
        xform: 4x4 affine transformation matrix.

    Returns:
        Transformed polyhedron.
        Data is altered in-place but also returned for convenience.
    """
    xform = numpy.array(xform, copy=False)
    mat4x3 = xform[:, :3]
    mat4x1 = xform[:, 3]
    vh = mat4x3 @ poly['vertices'].T + mat4x1
    poly['vertices'][:] = (vh[:3, :] / vh[3, :]).T
    return poly
