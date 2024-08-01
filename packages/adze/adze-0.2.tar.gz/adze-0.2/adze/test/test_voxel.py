from typing import TYPE_CHECKING
import logging
import warnings
from time import perf_counter

import numpy
from numpy.typing import NDArray
from numpy.testing import assert_allclose

import adze
import adze.util

from .utils import TOL_FAIL, TOL_WARN, rand_tetrahedron_vertices
#from .utils import PRNG, MIN_VOLUME, flip_plane, tetrahedron_volume
#from .utils import build_rand_tetrahedron, gen_plane_through_centroid, plane_generators, gen_torus_brep

if TYPE_CHECKING:
    import matplotlib


logger = logging.getLogger(__name__)


def test_voxelization(poly_order: int, grid_resolution: int | None = None) -> None:
    """
    Test that the voxelized moments sum to those of the original input
    """
    if grid_resolution is None:
        grid_resolution = 250 if poly_order == 0 else 50

    verts = 1.5 * (numpy.array(rand_tetrahedron_vertices()) + 1)
    poly = adze.build_tetrahedron(verts)
    moments = adze.get_moments(poly, poly_order)

    edges = [numpy.linspace(-1, 3, grid_resolution) for _ in range(3)]
    logger.info(f'Voxelizing a tetrahedron to a grid with moments of order {poly_order}')
    t0 = perf_counter()
    grid = adze.voxelize(poly, edges, order=poly_order)
    logger.info(f'voxel time: {perf_counter() - t0}')

    #visualize_isosurface(grid[:, :, :, 0], edges)

    voxsum = numpy.sum(grid, axis=(0, 1, 2))

    assert_allclose(moments, voxsum, atol=TOL_FAIL)
    if not numpy.allclose(moments, voxsum, atol=TOL_WARN):
        warnings.warn('Moments failed tolerance in voxels', stacklevel=1)


def visualize_isosurface(
        grid: NDArray[numpy.float64],
        edges: NDArray[numpy.int64],
        level: float | None = None,
        show_edges: bool = True,
        finalize: bool = True,
        ) -> tuple['matplotlib.Figure', 'matplotlib.Axes']:
    """
    Draw an isosurface plot of the device.

    Args:
        level: Value at which to find isosurface. Default (None) uses mean value in grid.
        show_edges: Whether to draw triangle edges. Default True
        finalize: Whether to call pyplot.show() after constructing the plot. Default True
    """
    from matplotlib import pyplot
    import skimage.measure
    # Claims to be unused, but needed for subplot(projection='3d')
    from mpl_toolkits.mplot3d import Axes3D
    del Axes3D  # imported for side-effects only

    if level is None:
        level = grid.mean()

    # Find isosurface with marching cubes
    verts, faces, _normals, _values = skimage.measure.marching_cubes(grid, level)

    xs, ys, zs = (edges[aa][verts[:, aa].astype(int)] for aa in range(3))

    # Draw the plot
    fig = pyplot.figure()
    ax = fig.add_subplot(111, projection='3d')
    if show_edges:
        ax.plot_trisurf(xs, ys, faces, zs)
    else:
        ax.plot_trisurf(xs, ys, faces, zs, edgecolor='none')

    # Add a fake plot of a cube to force the axes to be equal lengths
    max_range = numpy.array([xs.max() - xs.min(),
                             ys.max() - ys.min(),
                             zs.max() - zs.min()], dtype=float).max()
    mg = numpy.mgrid[-1:2:2, -1:2:2, -1:2:2]
    xbs = 0.5 * max_range * mg[0].flatten() + 0.5 * (xs.max() + xs.min())
    ybs = 0.5 * max_range * mg[1].flatten() + 0.5 * (ys.max() + ys.min())
    zbs = 0.5 * max_range * mg[2].flatten() + 0.5 * (zs.max() + zs.min())
    # Comment or uncomment following both lines to test the fake bounding box:
    for xb, yb, zb in zip(xbs, ybs, zbs, strict=True):
        ax.plot([xb], [yb], [zb], 'w')

    if finalize:
        pyplot.show()

    return fig, ax
