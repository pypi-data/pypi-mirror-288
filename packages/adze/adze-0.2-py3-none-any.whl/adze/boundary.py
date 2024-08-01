from typing import Any
from collections.abc import Iterable
import numpy
from numpy.linalg import norm
from numpy.typing import ArrayLike, NDArray

from . import poly_t, plane_t
from .util import _get_maps, find_components, find_faces, AdzeError


def planes_from_boundary(
        vertices: ArrayLike,
        faces: list[ArrayLike]
        ) -> list[plane_t]:
    """
    Generate a list of planes (normal, signed distance) from the faces of a boundary-
      representation polyhedron.

    Args:
        vertices: Nx3 ndarray specifying the polyhedron's vertex positions.
        faces: List of 1d ndarrays. Each ndarray is a list of vertex indices,
            specifying a face.

    Returns:
        List of planes, represented by (normal vector, signed distance to origin) tuples.
    """
    vertices = numpy.asarray(vertices)
    afaces = [numpy.asarray(ff) for ff in faces]
    planes = []
    for face in afaces:
        face_verts = vertices[face]

        n = numpy.cross(numpy.diff(face_verts, n=1, axis=0),
                        numpy.diff(face_verts, n=2, axis=0))
        n /= norm(n)
        centroid = numpy.sum(face_verts, axis=0) / len(face)
        d = -n @ centroid
        planes.append((n, d))
    return planes


def build_polyhedron(vertices: ArrayLike, faces: Iterable[ArrayLike]) -> poly_t:
    """
    Generate a 3-verted-connected Schlegel diagram representation
      corresponding to the provided boundary-representation polyhedron.

    Args:
        vertices: Nx3 ndarray specifying the polyhedron's vertex positions.
        faces: List of 1d ndarrays. Each ndarray is a list of vertex indices,
            specifying a face.

    Returns:
        Schelgel-representation polyhedron
    """
    vertices = numpy.array(vertices, dtype=float)
    afaces = [numpy.array(face, dtype=int) for face in faces]

    edges_per_vertex = numpy.bincount(numpy.hstack(afaces))

    if edges_per_vertex.min() < 3:
        raise AdzeError(f'Vertex {edges_per_vertex.argmin()} has < 3 edges')

    if edges_per_vertex.max() == 3:
        #
        # In this case, we don't need to duplicate any vertices to make a 3-vertex-connected graph
        #
        neighbors = numpy.full_like(vertices, vertices.size, dtype=int)
        for face in afaces:
            # Check if each vertex in this face is already linked to its next or previous face-neighbor
            prev_vert = numpy.roll(face, 1)
            next_vert = numpy.roll(face, -1)
            neighbor_rows = neighbors[face, :]
            has_prev = (neighbor_rows == prev_vert).any(axis=1)
            has_next = (neighbor_rows == next_vert).any(axis=1)

            # Each vertex touches 3 faces; each vertex triplet (neighbor_row) is a triangle on a face.
            #  Thus, we will never encounter a situation in which prev == next.

            # If the vertex hasn't been linked to anything yet, set its first two
            #  polyhedron-neighbors to its face-neighbors
            empty = numpy.logical_not(numpy.logical_or(has_prev, has_next))
            neighbors[face[empty], 0] = next_vert[empty]
            neighbors[face[empty], 1] = prev_vert[empty]

            # If the vertex has already been linked to something (by a different face),
            #  fill in the third neighbor
            # Note that this causes excess writes; it might improve performace to check
            #  if the third neighbor is already filled (maybe? TODO)
            neighbors[face[has_prev], 2] = next_vert[has_prev]
            neighbors[face[has_next], 2] = prev_vert[has_next]

        return {'vertices': vertices, 'neighbors': neighbors}

    """
    Some vertices link more than three edges.
    We only allow three edges per vertex in the graph, so we need to make
      degenerate copies of those vertices.

    For convenience, duplicate each vertex as many times as it has edges.
    This creates 2 'excess' duplicates of each vertex (e.g. a vertex with
      3 edges will turn into 3 vertices, even though it was fine as-is).

    Link the "duplicate" vertices together, as follows:
      - Each set of duplicates becomes a doubly-linked ring.
      - Each duplicate has an additional, "third" pointer, pointing to one
         of the duplicates created for a _different_ original vertex (i.e., this
         pointer and its counterpart both correspond to the edge which caused
         these two duplicates to be created).

    We perform this linkage by creating a list of 3 entries per duplicate, aiming
      to eventually fill each row with the indices
        [next_row, third_row, prev_row]
      corresponding to the linked duplicates.

    We begin by filling columns (1, 2) with the (next, prev) _original_ vertex indices
      for each face. The subset of the list corresponding to a single original vertex
      thus looks like

        [???, f0_next, f0_prev]  <-- (i.e., the angle fromed by the three points
        [???, f3_next, f3_prev]       [..., prev, me, next, ...], where 'me' is the
        [???, f7_next, f7_prev]       (original) vertex index corresponding to this row
                ...                   and prev, next are original vertex indices as listed
                                      in face 0's vertex list)
        and so on, with a row and f# for each face the original vertex participates in.
        The full list is just
            [ rows for
              original vertex 0
              ...
              rows for
              original vertex 1
              ...
              etc
            ]
        (note that each original vertex takes as many rows as it has edges)

    Next, note that the newly filled columns will hold the same sets of numbers, just permuted.
      Each row specifies two edges (an angle), and each edge is shared by two faces, and appears
      once as a "previous" pointer and once as a "next" pointer.

    So, we can set column 0 to the (new) index of the row whose f_prev matches our row's f_next.
      In other words, pick column 0 to ensure dn[i, 1] == dn[dn[i, 0], 2]. Our columns become
        [next_row, f#_next, f#_prev]
    Then, replace f#_prev with a back-pointer based on next_row,
        [next_row, f#_next, prev_row]
      which completes our doubly-linked duplicate vertex rings.

    To complete the linkage, we need to link to 'third_row'. We can do this by,
      For each set of rows (corresponding to an original vertex V0),
       - searching the sets of rows Vi corresponding to the listed f#_next values
           for rows whose f#_next == V0
       - doubly linking each row (i) in V0 with its 'found' row in Vi

    Finally, we can remove the first two ('excess') duplicate vertices in each ring, and update
      the links to reflect their removal.
    """

    # starting row for each original vertex
    start = numpy.roll(numpy.cumsum(edges_per_vertex), 1)
    start[0] = 0

    # number of input vertices (v) and duplicates (d)
    num_vertices = vertices.shape[0]
    num_duplicates = edges_per_vertex.sum()

    neighbors = numpy.empty((num_duplicates, 3), dtype=int)

    #
    # Fill columns (1, 2) with original vertex inds (f#_next, f#_prev)
    #
    num_filled_rows = numpy.zeros(num_duplicates, dtype=int)
    for face in afaces:
        # assume a face can't use the same vertex twice
        v_inds = start[face] + num_filled_rows[face]
        neighbors[v_inds, 1] = numpy.roll(face, -1)
        neighbors[v_inds, 2] = numpy.roll(face, 1)
        num_filled_rows[face] += 1

    #
    # Fill columns (0, 2) with new vertex inds (next_row, prev_row)
    #   to complete doubly-linked rings
    #
    for v in range(num_vertices):
        v0 = start[v]
        s = slice(v0, v0 + edges_per_vertex[v])
        m, n = _get_maps(neighbors[s, 2], neighbors[s, 1])
        neighbors[s, 0] = n + v0
        neighbors[s, 2] = m + v0

    #
    # for each pair of original vertices,
    #   find subvertices whose f#_next pointers point to each other's original vertices,
    #     and link them using column 1 (i.e. set their third_row pointers to each other)
    #
    # Mapping from row to original vertex index
    v0s = numpy.repeat(numpy.arange(len(edges_per_vertex)), edges_per_vertex)

    # Copy column 1 to save target info
    target_vert = neighbors[:, 1].copy()

    # Preallocate mask arrays
    src_mask = numpy.empty(num_duplicates, dtype=bool)
    dst_mask = numpy.empty(num_duplicates, dtype=bool)

    for v in range(num_vertices):
        ss = start[v]
        ee = ss + edges_per_vertex[v]

        src_mask.fill(False)
        src_mask[ee:] = target_vert[ee:] == v  # find rows which reference us
        src_vert = v0s[src_mask]             # figure out their original vertex numbers

        if src_vert.size == 0:
            continue

        dst_mask.fill(False)
        dst_mask[ss:ee] = target_vert[ss:ee] > v  # mask out any references to verts >= current
        dst_vert = target_vert[dst_mask]

        ma, mb = _get_maps(dst_vert, src_vert)
        neighbors[dst_mask, 1] = numpy.where(src_mask)[0][mb]
        neighbors[src_mask, 1] = numpy.where(dst_mask)[0][ma]

    """
    Remove first two duplicates of each vertex (they aren't needed)
    """
    nxt, third, prv = neighbors[start, :].T
    nxt_nxt, nxt_third, _nxt_prv = neighbors[nxt, :].T

    # Which vertex to link to
    dest_map = numpy.arange(num_duplicates, dtype=int)  # default maps to itself
    dest_map[start] = prv                        # first maps to previous
    dest_map[nxt] = nxt_nxt                             # second maps to next

    # Which backreference to modify
    back_map = numpy.full_like(dest_map, 1)  # default is 'third'
    back_map[start] = 0    # if we mapped from a first vertex to its previous, set to 'next'
    back_map[nxt] = 2             # if we mapped from a second vertex to its next, set to 'previous'

    # Map 'third' to where it should point to. 'dm'~'dest_map'
    dm_third = dest_map[third]
    dm_nxt_third = dest_map[nxt_third]

    neighbors[prv, 0] = dm_third          # previous's next reference points to third
    neighbors[nxt_nxt, 2] = dm_nxt_third  # next-next's previous reference points to next-third

    neighbors[dm_third, back_map[third]] = prv              # third's backreference points to previous
    neighbors[dm_nxt_third, back_map[nxt_third]] = nxt_nxt  # next-third's backreference points to next-next

    # Mark for removal
    keep_map = num_filled_rows    # reuse to avoid reallocating
    keep_map.fill(1)
    keep_map[start] = 0
    keep_map[nxt] = 0

    neighbors = neighbors[keep_map != 0]
    keep_map[keep_map != 0] = numpy.arange(neighbors.shape[0])
    neighbors[:] = keep_map[neighbors]

    final_vertices = numpy.repeat(vertices, edges_per_vertex - 2, axis=0)

    return {'vertices': final_vertices, 'neighbors': neighbors}


def boundary_from_poly(poly: poly_t) -> list[dict[str, Any]]:
    """
    Generate a boundary represeentation corresponding to the provided
      3-vertex-connected Schlegel diagram.

    Args:
        poly: Polyhedron to convert, in Schlegel representation.

    Returns:
        Dict containing 'vertices' (Nx3 ndarray of vertex locations)
        and 'faces' (list of ndarrays specifying the indices of vertices
        used for constructing each face).
    """
    neighbors = poly['neighbors']
    vertices = poly['vertices']

    owning_component = find_components(neighbors)
    faces = find_faces(neighbors)
    num_components = owning_component.max() + 1

    components: list[list[NDArray[numpy.integer]]] = [[] for _ in range(num_components)]
    for face in faces:
        component_ind = owning_component[face[0]]
        components[component_ind].append(face)

    unique_verts, unique_vertex_map = numpy.unique(vertices, axis=0, return_inverse=True)
    umap = numpy.empty(unique_verts.shape[0], dtype=int)
    boundary_map = numpy.empty(vertices.shape[0], dtype=int)
    boundaries = []
    for i, component in enumerate(components):
        mask = owning_component == i
        umask = unique_vertex_map[mask]
        used_uverts = numpy.unique(umask)

        umap[used_uverts] = numpy.arange(used_uverts.size)  # map to account for deletion of unique verts not used in this component
        boundary_map[mask] = umap[umask]    # map from non-unique verts in face to unique, in-use verts

        boundary = {
            'vertices': unique_verts[used_uverts],
            'faces': [boundary_map[face] for face in component],
            }
        boundaries.append(boundary)

    return boundaries

