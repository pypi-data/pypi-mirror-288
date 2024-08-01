from typing import TYPE_CHECKING
from collections.abc import Sequence
import numpy
from numpy.typing import NDArray

if TYPE_CHECKING:
    import stl


plane_t = tuple[NDArray[numpy.floating], float | numpy.floating]
poly_t = dict[str, NDArray]


class AdzeError(Exception):
    """ Custom error for Adze """
    pass


def build_empty() -> poly_t:
    """
    Build an empty Schlegel representation (containing no vertices).

    Returns:
        Empty Schelegel representation.
    """
    return {
        'vertices': numpy.empty((0, 3), dtype=float),
        'neighbors': numpy.empty((0, 3), dtype=int),
        }


def find_components(neighbors: NDArray[numpy.integer]) -> NDArray[numpy.integer]:
    """
    Given an adjacency list, flood-fill to find and label connected components.

    Args:
        neighbors: NxM adjacency list. Each of the N vertices is assumed
            to have the same number of neighbors, which are specified by their
            indices.

    Returns:
        1D ndarray with N entries. Entries are integer labels denoting
        which connected component the vertex belongs to.
    """
    num_vertices = neighbors.shape[0]
    current_component = 1
    component = numpy.zeros(num_vertices, dtype=int)
    for v_start in range(num_vertices):
        if component[v_start] != 0:
            continue

        verts = numpy.array([v_start], dtype=int)
        while verts.size > 0:
            component[verts] = current_component
            next_verts = numpy.unique(neighbors[verts])
            verts = next_verts[component[next_verts] == 0]

        current_component += 1
    return component - 1


def find_faces(neighbors: NDArray[numpy.integer]) -> list[NDArray[numpy.intp]]:
    """
    Traverse the Schlegel diagram to find chordless cycles
      (i.e., faces of the polyhedron). Assumes 3-vertex-connected
      graph with exactly 3 neighbors per vertex. Neighbors are ordered
      counter-clockwise.

    Args:
        neighbors: Nx3 adjacency list. Neighbors are specified by their
            indices.

    Returns:
        List of ndarrays, each of which contains the indices in a given
        face, starting with the lowest index in the face.
    """
    num_verts = neighbors.shape[0]

    edge_id = numpy.arange(3 * num_verts)
    v_start, nxt_edge = numpy.divmod(edge_id, 3)    # arange % 3 is faster than tile
    v_current = v_start.copy()
    v_next = neighbors[v_current, nxt_edge]

    """
    Choose a method for storing the face info based on expected
      runtime vs unnecessary memory allocation
    """
    if num_verts < 1000:
        # ~3n^2 in memory, but much faster in cases where n isn't prohibitively large
        faces_arr = numpy.full((3 * num_verts, num_verts - 1), -1, dtype=int)
        faces_arr[:, 0] = v_current

        def add_edges(edge_id: NDArray[numpy.intp], v_nxt: NDArray[numpy.intp], kk: int) -> None:
            faces_arr[edge_id, kk] = v_nxt

        def cleaned_faces(remove: NDArray[numpy.int8], kk: int) -> list[NDArray[numpy.intp]]:
            faces_set = []
            for row in faces_arr[~remove, :kk]:
                faces_set.append(row[row >= 0])
            return faces_set
    else:
        # Alternative approach, less memory-intensive but slower
        faces_list = [[vv] for vv in v_current]

        def add_edges(edge_id: NDArray[numpy.intp], v_nxt: NDArray[numpy.intp], kk: int) -> None:       # noqa: ARG001
            for ii, vn in zip(edge_id, v_nxt, strict=True):
                faces_list[ii].append(vn)

        def cleaned_faces(remove: NDArray[numpy.int8], kk: int) -> list[NDArray[numpy.intp]]:           # noqa: ARG001
            faces_set = []
            for ii in numpy.where(~remove)[0]:
                faces_set.append(numpy.asarray(faces_list[ii], dtype=numpy.intp))
            return faces_set

    """
    Starting at all vertices, take a step along all edges.
    If the vertex index decreases, stop traversal and mark the path for removal.
    Otherwise, continue stepping along the _next_ edge each time, until
      a) the vertex index decreases (stop and mark for removal)
      b) we reach the original vertex (stop, done with this path)
    """
    kk = 1
    mask = v_next > v_current
    vv = numpy.vstack((edge_id, v_start, v_current, v_next))[:, mask]
    remove = numpy.logical_not(mask)

    while mask.any():
        add_edges(vv[0], vv[3], kk)

        prv_edge = (neighbors[vv[3], :] == vv[2][:, None]).argmax(axis=1)
        nxt_edge = (prv_edge + 1) % 3
        vv[2:4] = vv[3], neighbors[vv[3], nxt_edge]

        remove_mask = vv[2] < vv[1]
        remove[vv[0][remove_mask]] = True

        mask = numpy.logical_and(vv[3] != vv[1], ~remove_mask)
        vv = vv[:, mask]
        kk += 1

    return cleaned_faces(remove, kk)


def _get_map(a: NDArray, b: NDArray) -> NDArray[numpy.intp]:
    """
    Returns m such that a[m] == b
    Assumes that all elements appear exactly once in each array
    """
    if a.size == 0:
        return numpy.array((), dtype=numpy.intp)
    sa = a.argsort()
    sb = b.argsort()
    r = numpy.empty_like(sa)
    r[sb] = numpy.arange(sa.size)
    return sa[r]


def _get_map_rows(a: NDArray, b: NDArray) -> NDArray[numpy.intp]:
    """
    Row-wise _get_map
    """
    dims = numpy.maximum(a.max(0), b.max(0)) + 1
    a1d = numpy.ravel_multi_index(a.T, dims)        # type: ignore
    b1d = numpy.ravel_multi_index(b.T, dims)        # type: ignore
    return _get_map(a1d, b1d)


def _get_maps(a: NDArray, b: NDArray) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
    """
    Returns m, n such that a[m] == b, b[n] == a
    Assumes that all elements appear exactly once in each array
    """
    if a.size == 0:
        return numpy.array((), dtype=numpy.intp), numpy.array((), dtype=numpy.intp)
    sa = a.argsort()
    sb = b.argsort()
    r = numpy.empty_like(sa)
    r[sb] = numpy.arange(sa.size)
    m = sa[r]
    r[sa] = numpy.arange(sa.size)
    n = sb[r]
    return m, n


def _get_maps_rows(a: NDArray, b: NDArray) -> tuple[NDArray[numpy.intp], NDArray[numpy.intp]]:
    """
    Row-wise _get_maps
    """
    dims = numpy.maximum(a.max(0), b.max(0)) + 1
    a1d = numpy.ravel_multi_index(a.T, dims)        # type: ignore
    b1d = numpy.ravel_multi_index(b.T, dims)        # type: ignore
    return _get_maps(a1d, b1d)


def _argsort_rows(a: NDArray) -> NDArray[numpy.intp]:
    """
    Row-wise argsort
    """
    dims = a.max(0) + 1
    a1d = numpy.ravel_multi_index(a.T, dims)        # type: ignore
    return numpy.argsort(a1d)


def _searchsorted_rows(a: NDArray, b: NDArray) -> NDArray[numpy.intp]:
    """
    Row-wise searchsorted
    """
    dims = numpy.maximum(a.max(0), b.max(0)) + 1
    a1d = numpy.ravel_multi_index(a.T, dims)        # type: ignore
    b1d = numpy.ravel_multi_index(b.T, dims)        # type: ignore
    return numpy.searchsorted(a1d, b1d)


def check_poly(poly: poly_t, check_connectivity: bool = True) -> None:
    """
    Verify that the polyhedron
        - has no out-of-bounds neighbors
        - has no duplicate neighbors
        - has exactly 3 edges per vertex
        - is 3-vertex-connected (if check_connectivity is True; slow!)

    Args:
        poly: Polyhedron to check.
        check_connectivity: Whether to check for 3-vertex-connectedness.
            This is slow! Default `True`.

    Raises:
        AdzeError if the polyhedron fails a check
    """
    neighbors = poly['neighbors']
    vertices = poly['vertices']
    num_vertices = vertices.shape[0]

    out_of_bounds = numpy.logical_or(neighbors >= vertices.shape[0], neighbors < 0)
    if numpy.any(out_of_bounds):
        which_vertices = numpy.where(out_of_bounds)[0]
        raise AdzeError(f'Vertices {which_vertices} have out-of-bounds neighbors')

    repeated_neighbors = neighbors == numpy.roll(neighbors, 1, axis=1)
    if numpy.any(repeated_neighbors):
        which_vertices = numpy.where(repeated_neighbors)[0]
        raise AdzeError(f'Vertices {which_vertices} have duplicate neighbors')

    vertex_uses = numpy.bincount(neighbors.ravel())
    if numpy.any(vertex_uses != 3):
        which_vertices = numpy.where(vertex_uses != 3)[0]
        raise AdzeError(f'Vertices {which_vertices} are referenced {vertex_uses[which_vertices]} times,'
                        ' should be exactly 3')

    # check for 3-vertex-connectedness (~n^3 because need bfs for each removed vertex pair)
    if check_connectivity:
        components = find_components(neighbors)

        vert_ids = numpy.arange(num_vertices, dtype=int)
        visited = numpy.empty(num_vertices, dtype=bool)
        for part_id in numpy.unique(components):
            part_mask = components == part_id
            part_verts = vert_ids[part_mask]

            vcs = set(part_verts[:3])
            for ia in range(part_verts.size):
                va = part_verts[ia]
                for vb in part_verts[ia + 1:]:
                    # pick vc != {va, vb}
                    vc = (vcs - {va, vb}).pop()

                    # flood-fill from vc without passing through va, vb
                    visited.fill(False)
                    visited[[va, vb]] = True

                    nums = numpy.array([vc], dtype=int)
                    while nums.size > 0:
                        visited[nums] = True
                        new_nums = numpy.unique(neighbors[nums])
                        nums = new_nums[~visited[new_nums]]

                    # Make sure we touched all vertices in the component
                    if not visited[components == part_id].all():
                        raise AdzeError('Vertex graph is not 3-vertex-connected')


def plot_brep(brep: Sequence[dict[str, NDArray]]) -> None:
    """
    Plot a boundary representation
    """
    from matplotlib import pyplot
    from mpl_toolkits import mplot3d

    meshes = brep_to_stls(brep)

    figure = pyplot.figure()
    axes = mplot3d.Axes3D(figure)
    scales = []
    for mesh in meshes:
        coll = mplot3d.art3d.Poly3DCollection(mesh.vectors)
        coll.set_edgecolors('black')
        axes.add_collection3d(coll)
        scales.append(mesh.points.flatten())
    scale = numpy.hstack(scales)
    axes.auto_scale_xyz(scale, scale, scale)
    pyplot.show()


def brep_to_stls(brep: Sequence[dict[str, NDArray]]) -> list['stl.mesh.Mesh']:
    import stl

    meshes = []
    for component in brep:
        tri_list = []
        for face in component['faces']:
            for ii in range(1, len(face) - 1):
                tri_list.append([face[0], face[ii], face[ii + 1]])
        triangles = numpy.asarray(tri_list, dtype=int)

        mm = stl.mesh.Mesh(numpy.empty(triangles.shape[0], dtype=stl.mesh.Mesh.dtype))
        for ii, ff in enumerate(triangles):
            for jj in range(3):
                mm.vectors[ii, jj] = component['vertices'][ff[jj], :]

#        mm.save('pyr.stl')
        meshes.append(mm)
    return meshes
