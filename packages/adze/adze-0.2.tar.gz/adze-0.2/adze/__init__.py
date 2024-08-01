"""
adze is a library for accurate polyhedron clipping and anti-aliased voxelization.
Written with python + numpy.

Most operations are performed using an ordered adjacency-list polyhedron represenation,
  capable of holding multiple unconnected possibly non-convex components.

To convert from a boundary representation, use
    poly = build_polyhedron(vertex_list, face_list)
To convert back to a boundary representation, use
    list_of_boundaries = boundary_from_poly(poly)
    vertex_list_0 = list_of_boundaries[0]['vertices']
    face_list_0 = list_of_boundaries[0]['faces']

Basic operations include
    plane = (normal_vector, signed_distance_to_origin)
    same_side_as_normal, other_side = split(poly, plane)
    same_side_as_normal = clip(poly, plane)

    volume = get_volume(poly)
    volume, m_x, m_y, m_z = get_moments(poly, order=1)

Anti-aliased voxelization is done on a non-uniform rectangular grid, specified by the cell
  edge coordinates:
    x_planes = numpy.linspace(-5, 5, 100)
    y_planes = numpy.linspace(-10, 10, 5)
    z_planes = [-3, 0, 1, 2, 3]
    voxel_weights = voxelize(poly, [x_planes, y_planes, z_planes], order=0)


Helper functions include
     poly = build_box(box_corners)
     poly = build_tetrahedron(vertices)
     plane_list = planes_from_box(box_corners)
     plane_list = planes_from_tetrahedron(vertices)

     n = number_of_moments(order=3)

--------------------------

In the polyhedron representation returned by the build_* functions and accepted by
  most other functions (split, clip, get_volume, get_moments, voxelize), the
  polyhedron is stored as a 3-vertex-connected, triply-linked graph, with each vertex's
  neighbors listed in counterclockwise order when viewed from outside the polyhedron.    TODO
  Each graph-vertex (g-vertex) is connected to exactly 3 other g-vertices; polygon-
  vertices (p-vertices) are


  TODO
  This representation looks like
    poly = {'neighbors': ndarray[Px3, int], 'vertices': ndarray[Px3, float]}
  where poly['neighbors'] contains

"""

from .util import (
    poly_t as poly_t,
    plane_t as plane_t,
    AdzeError as AdzeError,
    )

from .split import (
    split as split,
    clip as clip,
    )
from .moments import (
    get_volume as get_volume,
    get_moments as get_moments,
    number_of_moments as number_of_moments,
    )
from .boundary import (
    build_polyhedron as build_polyhedron,
    boundary_from_poly as boundary_from_poly,
    )
from .shapes import (
    build_tetrahedron as build_tetrahedron,
    build_box as build_box,
    planes_from_tetrahedron as planes_from_tetrahedron,
    planes_from_box as planes_from_box,
    )
from .voxel import voxelize as voxelize

__author__ = 'Jan Petykiewicz'
__version__ = '0.2'
