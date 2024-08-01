from collections.abc import Sequence
import numpy
from numpy.typing import ArrayLike, NDArray

from . import poly_t
from .split import split, clip
from .moments import get_moments, number_of_moments
from .shapes import planes_from_box
from .util import AdzeError


def voxelize(
        poly: poly_t,
        planes: Sequence[ArrayLike],
        include_outside: bool = False,
        order: int = 0,
        ) -> NDArray[numpy.float64]:
    """
    Voxelize a Schelegel-representation polyhedron on an arbitrary rectangular grid.

    The grid is specified by supplying 3 sets of axis-aligned planes, in the form
       `[[x0, x1, x2, ..., xX], [y0, y1, y2, ..., yY], [z0, z1, ..., zZ]]`
    The output array has size [X-1, Y-1, Z-1, N] (include_outside False) or
      `[X+1, Y+1, Z+1, N]` (`include_outside` True), where `N` is the number of moments
      corresponding to the requested order. If include_outside is true, the outer borders
      of the first three dimensions of the output correspond to portions of the polyhedron
      that protruded outside the provided grid.

    Args:
        poly: Polyhedron to voxelize.
        planes: List of coordinate lists, specifying the axis-aligned planes
            which form the voxel grid:
            `[[x0, x1, ..., xX], [y0, y1, ..., yY], [z0, z1, ..., zZ]]`
        include_outside: Whether to include cells corresponding to portions of the
            polyhedron that fall outside of the grid. Default `False`.
        order: Polynomial order of moments to calculate. Default `0`.

    Returns:
        (X - 1) x (Y - 1) x (Z - 1) x N (`include_outside` False) or
        (X + 1) x (Y + 1) x (Z + 1) x N (`include_outside` True) ndarray.
        If include_outside is True, the outer borders of the first three dimensions
        correspond to portions of the polyhedron that protruded outside the outermost
        planes. N is `number_of_moments(order)`.
    """
    aplanes = [numpy.asarray(p) for p in planes]

    num_planes = numpy.array([e.size for e in aplanes], dtype=int)
    if (num_planes < 2).any():
        raise AdzeError(f'Need at least two planes per dimension. Got {num_planes} planes.')

    if include_outside:
        grid_shape = num_planes + 1
    if not include_outside:
        grid_shape = num_planes - 1
        for face in planes_from_box([[p[0] for p in aplanes],
                                     [p[-1] for p in aplanes]]):
            poly = clip(poly, face)

    grid = numpy.zeros((*grid_shape, number_of_moments(order)), dtype=float)

    if poly['vertices'].shape[0] == 0:
        return grid

    slices = numpy.array([(0, e.size) for e in aplanes], dtype=int)
    stack = [(poly, slices)]
    while stack:
        poly, slices = stack.pop()

        # Base case 1: No vertices in this region, moments are 0
        if poly['vertices'].shape[0] == 0:
            continue

        num_planes_remaining = numpy.diff(slices, axis=1)

        # Base case 2: calculate moments for single voxel
        if not num_planes_remaining.any():
            moments = get_moments(poly, order)
            i, j, k = slices[:, 0] - 1
            grid[i, j, k, :] = moments
            continue

        # Recursion case: split along longest side
        axis = num_planes_remaining.argmax()
        plane_ind = (num_planes_remaining[axis] // 2 + slices[axis, 0])[0]
        plane_pos = aplanes[axis][plane_ind]

        plane = (numpy.roll([-1, 0, 0], axis), plane_pos)
        poly_left, poly_right = split(poly, plane)

        slices_left = slices
        slices_right = slices.copy()
        slices_left[axis, 1] = plane_ind
        slices_right[axis, 0] = plane_ind + 1

        stack.append((poly_left, slices_left))
        stack.append((poly_right, slices_right))
    return grid

