from typing import overload, Literal
import numpy

from . import poly_t, plane_t
from .util import build_empty, _get_map


def clip(poly: poly_t, plane: plane_t) -> poly_t:
    """
    Clip a polyhedron with a plane, keeping only the part which is on
      the same side as the plane's normal vector.

    This function is equivalent to calling _split(poly, plane, same_only=True).

    Args:
        poly: Polyhedron to clip, in chiral Schlegel representation.
        plane: Plane to clip against.

    Returns:
        Clipped polyhedron.
    """
    left_poly = _split(poly, plane, same_only=True)
    return left_poly


def split(poly: poly_t, plane: plane_t) -> tuple[poly_t, poly_t]:
    """
    Clip a polyhedron with a plane, keeping both parts.

    This function is equivalent to calling _split(poly, plane, same_only=False).

    Args:
        poly: Polyhedron to clip, in chiral Schlegel representation.
        plane: Plane to clip against.
    Returns:
        same_side_poly, other_side_poly
        The first polyhedron is on from the same side as the plane's normal vector.
    """
    return _split(poly, plane, same_only=False)


@overload
def _split(poly: poly_t, plane: plane_t, same_only: Literal[True]) -> poly_t:
    ...


@overload
def _split(poly: poly_t, plane: plane_t, same_only: Literal[False]) -> tuple[poly_t, poly_t]:
    ...


@overload
def _split(poly: poly_t, plane: plane_t, same_only: bool) -> tuple[poly_t, poly_t] | poly_t:
    ...


def _split(poly: poly_t, plane: plane_t, same_only: bool = False) -> tuple[poly_t, poly_t] | poly_t:
    """
    Clip a polyhedron with a plane.

    If same_only is False (default), returns the tuple (same_side_poly, other_side_poly),
      where same_side_poly is on the same side as the plane's normal vector. Otherwise,
      returns only same_side_poly (somewhat faster).

    Args:
        poly: Polyhedron to clip, in chiral Schlegel representation.
        plane: Plane to clip against.
        same_only: If True, only returns the clipped poly from the same side as the
            plane's normal vector. Default False.
    Returns:
        (same_side_poly, other_side_poly) if same_only is False (default), otherwise
            only returns same_side_poly.
    """
    vertices = poly['vertices']
    neighbors = poly['neighbors']
    num_start = neighbors.shape[0]

    dists = plane[1] + (vertices @ plane[0])
    left = dists > 0
    right = numpy.logical_not(left)

    num_left = numpy.count_nonzero(left)
    num_right = num_start - num_left

    #
    # if the poly lies entirely on one side of the plane, just return it
    #
    if num_left == 0:
        # if all on right or touching plane
        ret = build_empty(), poly
        return ret[0] if same_only else ret
    if dists.min() >= 0:
        # if all on left or touching plane
        # Can't reuse 'left' because <= vs <
        ret = poly, build_empty()
        return ret[0] if same_only else ret

    right_inds = numpy.where(right)[0]
    next_vertex = neighbors[right_inds, :].ravel()

    # remove edges which connect two same-side vertices
    far_vertex_left = left[next_vertex]

    if not far_vertex_left.any():
        #
        # No edges cross the plane, but components exist on either side
        #
        # r2l_edges = numpy.empty((0, 3), dtype=int)
        target_edge_inds = numpy.empty((0, 1), dtype=int)
        new_vertices = numpy.empty((0, 3), dtype=float)
        src_pns = target_edge_inds.copy()
        num_new_vertices = 0
        rverts = numpy.empty(0, dtype=int)
        lverts = rverts.copy()
    else:
        #
        # Some edges cross the plane
        #
        # remove edges which don't also touch the left half-plane
        which_edges_cross, rl_edge_inds = numpy.divmod(numpy.where(far_vertex_left)[0], 3)
        rverts = right_inds[which_edges_cross]
        lverts = next_vertex[far_vertex_left]

        num_new_vertices = rverts.size

        #
        # figure out new vertex positions
        #
        d_right = dists[rverts][:, None]
        d_left = dists[lverts][:, None]
        new_vertices = (d_right * vertices[lverts] - d_left * vertices[rverts]) / (d_right - d_left)

        #
        # walk to next crossing edge
        #
        prev_verts = rverts
        cur_verts = lverts
        edge_walk_inds = numpy.arange(num_new_vertices)
        edge_walk_results = numpy.empty((2, num_new_vertices), dtype=int)
        src_pns = None
        while cur_verts.size > 0:
            # Get the list of our current neighbors, find which one points to the
            #  vertex we came from, and choose the next (ccw) one
            cur_links = neighbors[cur_verts]
            row, src_pn = numpy.where(cur_links == prev_verts[:, None])
            new_pn = (src_pn + 1) % 3

            if src_pns is None:
                src_pns = src_pn

            next_verts = cur_links[(row, new_pn)]

            # Save edges that cross back to right, and remove them from the list of verts
            done = right[next_verts]
            edge_walk_results[:, edge_walk_inds[done]] = (next_verts[done], cur_verts[done])

            # Save the current vertices as previous, and our chosen neighbors as current
            not_done = numpy.logical_not(done)
            prev_verts = cur_verts[not_done]
            cur_verts = next_verts[not_done]
            edge_walk_inds = edge_walk_inds[not_done]

        # now edge_walk_results is list of [[target clipped adjacent vertex, target connected vertex], ...]

        # figure out the index of each target edge using row-wise _get_map
        dims = [num_start, num_start]
        a1d = numpy.ravel_multi_index((rverts, lverts), dims)
        b1d = numpy.ravel_multi_index(tuple(edge_walk_results), dims)
        target_edge_inds = _get_map(a1d, b1d)


    #
    # map from old vertex ind to new
    #
    ind_map_left = numpy.zeros(num_start, dtype=int)
    # current side vertices get new (equal or lower) indices from delete operation, remain in same order
    ind_map_left[left] = numpy.arange(num_left)
    # Hops across the boundary depend on (origin, destination) pair since that determines final vertex

    # use argsort to generate link from target edge to current edge
    target_order = numpy.argsort(target_edge_inds)
    new_neighbors_left = numpy.column_stack((
        ind_map_left[lverts],                         # update left vertices based on new indexing
        target_order + num_left,                      # new vertex indices are same as edge indices + offset
        target_edge_inds + num_left))

    old_vertices_left = vertices[left]

    old_neighbors_left = neighbors.copy()
    old_neighbors_left[left] = ind_map_left[old_neighbors_left[left]]   # map vertices on left side, wrongly mapping any right-side vertices to 0
    old_neighbors_left[(lverts, src_pns)] = num_left + numpy.arange(num_new_vertices)
    old_neighbors_left = old_neighbors_left[left]

    left_poly = {
        'vertices': numpy.vstack((old_vertices_left, new_vertices)),
        'neighbors': numpy.vstack((old_neighbors_left, new_neighbors_left)),
        }

    if same_only:
        return left_poly

    ind_map_right = numpy.zeros(num_start, dtype=int)
    ind_map_right[right] = numpy.arange(num_right)

    new_neighbors_right = numpy.column_stack((
        ind_map_right[rverts],                        # update right vertices based on new indexing
        target_edge_inds + num_right,                 # new vertex indices are same as edge indices + offset
        target_order + num_right))

    old_vertices_right = vertices[right]

    old_neighbors_right = neighbors.copy()
    old_neighbors_right[right] = ind_map_right[old_neighbors_right[right]]
    old_neighbors_right[(rverts, rl_edge_inds)] = num_right + numpy.arange(num_new_vertices)
    old_neighbors_right = old_neighbors_right[right]

    right_poly = {
        'vertices': numpy.vstack((old_vertices_right, new_vertices)),
        'neighbors': numpy.vstack((old_neighbors_right, new_neighbors_right)),
        }

    return left_poly, right_poly

