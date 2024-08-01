import numpy
from numpy.typing import NDArray

from . import poly_t
from .util import find_faces


def number_of_moments(order: int) -> int:
    """
    Returns the number of moments with a given order or below.

    Args:
        order: Maximum polynomial order for the moments.

    Returns:
        Number of moments with that order or fewer.
    """
    return ((order + 1) * (order + 2) * (order + 3)) // 6


def get_volume(poly: poly_t) -> float:
    """
    Calculates the volume of a polyhedron (0th moment).

    Args:
        poly: Polyhedron to evaluate, in Schlegel representation.

    Returns:
        Volume of the polyhedron.
    """
    return get_moments(poly, 0)[0]


def get_moments(poly: poly_t, order: int) -> NDArray[numpy.float64]:
    """
    Calculates the moments of a polyhedron, up to the specified polynomial order.

    Args:
        poly: Polyhedron to evaluate, in Schlegel representation.
        order: Maximum polynomial order for moments.

    Returns: Moments, increasing polynomial order:
       [1, x, y, z, xx, xy, xz, yy, yz, zz, xxx, xxy, xxz, ...]
    """
    vertices = poly['vertices']
    neighbors = poly['neighbors']
    num_verts = vertices.shape[0]

    if num_verts == 0:
        return numpy.array([0], dtype=float)

    #
    # Decompose polyhedron into triangle fans
    #
    faces = find_faces(neighbors)

    triangle_fans = []
    max_face_len = max(len(face) for face in faces)
    triangle_inds = numpy.empty((max_face_len - 2, 3), dtype=int)
    for face in faces:
        # Build a triangle fan from each face
        ilen = len(face) - 2
        triangle_inds[:ilen, 0] = face[0]     # this assignment is a broadcast
        triangle_inds[:ilen, 1] = face[1:-1]
        triangle_inds[:ilen, 2] = face[2:]

        triverts = vertices[triangle_inds[:ilen]]
        triangle_fans.append(triverts)

    #
    # Calculate the 0th-order moment
    #
    triangles = numpy.vstack(triangle_fans)
    volumes = -numpy.linalg.det(triangles)
    moment0 = numpy.array([volumes.sum() / 6])

    if order == 0:
        return moment0

    #
    # Iteratively calculate higher-order moments, as per Koehl (2012).
    #
    prevlayer, curlayer = 0, 1
    inds = numpy.arange(order + 1)
    mx, my = numpy.meshgrid(inds, inds, indexing='ij')
    valid = numpy.zeros((2, order + 1, order + 1), dtype=bool)
    cropped = numpy.zeros((order + 1, order + 1), dtype=bool)

    Q = numpy.zeros((len(triangles), 3, order + 1, order + 1, 2), dtype=float)
    Q[:, :, 0, 0, prevlayer] = 1
    S = numpy.zeros((order + 1, order + 1, 2), dtype=float)
    S[0, 0, prevlayer] = 1
    valid[prevlayer, :, :] = False
    valid[prevlayer, 0, 0] = True
    moment_list = [moment0]
    for c in range(1, order + 1):
        valid[curlayer] = c >= mx + my
        # num_valid = (c + 1) * (c + 2) // 2      # always an int, see number_of_moments()

        Q_prev = Q[:, :, valid[prevlayer], prevlayer]
        Q[:, :, 0, :, curlayer] = 0

        S_prev = S[valid[prevlayer], prevlayer]
        S[0, :, curlayer] = 0

        cropped.fill(0)
        cropped[1:, :] = valid[curlayer, 1:, :]
        Q[:, :, cropped, curlayer] = triangles[:, :, 0:1] * Q_prev
        S[cropped, curlayer] = S_prev

        cropped = numpy.moveaxis(cropped, 0, 1)
        Q[:, :, cropped, curlayer] += triangles[:, :, 1:2] * Q_prev
        S[cropped, curlayer] += S_prev

        Q[:, :, valid[prevlayer], curlayer] += triangles[:, :, 2:3] * Q_prev
        S[valid[prevlayer], curlayer] += S_prev

        # Actually only need to cumsum S[:, valid[prevlayer], curlayer], but it's faster
        #  when done in-place for the whole array
        numpy.cumsum(Q, axis=1, out=Q)

        numer = (volumes[:, None] * Q[:, 2, valid[curlayer], curlayer]).sum(axis=0)
        denom = S[valid[curlayer], curlayer] * (c + 1) * (c + 2) * (c + 3)

        moment_list.append( (numer / denom).ravel())
        prevlayer, curlayer = curlayer, prevlayer

    return numpy.hstack(moment_list)
