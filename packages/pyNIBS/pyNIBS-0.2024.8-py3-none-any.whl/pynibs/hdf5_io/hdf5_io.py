"""This module contains functions to read and write .hdf5 files."""
import os
import re
import h5py
import nibabel
import datetime
import warnings
import numpy as np
import pandas as pd
import multiprocessing
from subprocess import call
from functools import partial
import pynibs


def split_hdf5(hdf5_in_fn, hdf5_geo_out_fn='', hdf5_data_out_fn=None):
    """
    Splits one hdf5 into one with spatial data and one with statistical data.
    If coil data is present in ``hdf5_in``, it is saved in ``hdf5Data_out``.
    If new spatial data is added to file (curve, inflated, whatever), add this to the geogroups variable.

    Parameters
    ----------
    hdf5_in_fn : str
        Filename of .hdf5 input file.
    hdf5_geo_out_fn : str
        Filename of .hdf5 .geo output file.
    hdf5_data_out_fn : str
        Filename of .hdf5 .data output file (ff none, remove data from hdf5_in).

    Returns
    -------
    <File> : .hdf5 file
        hdf5Geo_out_fn (spatial data).
    <File> : .hdf5 file
        hdf5Data_out_fn (data).
    """
    hdf5_in = h5py.File(hdf5_in_fn, 'r+')

    if hdf5_data_out_fn is not None:
        hdf5_geo_out = None
        hdf5_data_out = None
        try:
            hdf5_geo_out = h5py.File(hdf5_geo_out_fn, 'x')
            hdf5_data_out = h5py.File(hdf5_data_out_fn, 'x')
        except IOError:
            print((hdf5_geo_out_fn + " or " + hdf5_data_out_fn + " already exists. Quitting."))
            quit()

        print(("Writing " + hdf5_geo_out_fn))
        geogroups = ["/mesh/", "/nodes/"]
        for group in geogroups:
            if group in hdf5_in:
                hdf5_in.copy(group, hdf5_geo_out)
            else:
                print((group + "not found in " + hdf5_in_fn))

        print(("Writing " + hdf5_data_out_fn))
        datagroups = ["/data/", "/fields/", "/coil/"]
        for group in datagroups:
            if group in hdf5_in:
                hdf5_in.copy(group, hdf5_data_out)
            else:
                print((group + "not found in " + hdf5_in_fn))

        # sometimes there is /mesh/field. move to /field/
        if "/mesh/fields" in hdf5_geo_out:
            print(("Moving datarrays " +
                   os.path.basename(hdf5_geo_out_fn) + "/mesh/fields/* to " +
                   os.path.basename(hdf5_data_out_fn) + "/data/fields*"))
            if "/data/" not in hdf5_data_out:
                hdf5_data_out.create_group("/data/")
            hdf5_geo_out.copy("/mesh/fields/", hdf5_data_out)
            del (hdf5_geo_out['/mesh/fields/'])
            for field in hdf5_data_out['/fields/']:
                hdf5_data_out.move('/fields/' + field, '/data/' + field)
            del (hdf5_data_out['/fields'])

    else:  # remove spatial data from hdf5_in
        if "/mesh/fields" in hdf5_in:
            if "/data/" not in hdf5_in:
                hdf5_in.create_group("/data/")
            for dataset in hdf5_in["/mesh/fields"]:
                hdf5_in.move("/mesh/fields/" + dataset, "/data/" + dataset)
        for group in hdf5_in['/']:
            if group != "data" and group != "coil":
                del (hdf5_in['/' + group])
        hdf5_in.close()
        print("repacking .hdf5")
        os.rename(hdf5_in_fn, hdf5_in_fn + '_temp')
        # call("ptrepack -o --chunkshape=auto --propindexes " + hdf5_in_fn + '_temp ' + hdf5_in_fn)

        command = ["ptrepack", "-o", "--chunkshape=auto", "--propindexes",
                   hdf5_in_fn + '_temp',
                   hdf5_in_fn]
        call(command)
        os.remove(hdf5_in_fn + '_temp')


def read_data_hdf5(fname):
    """
    Reads phi and dA/dt data from .hdf5 file (phi and dAdt are given in the nodes).

    Parameters
    ----------
    fname : str
        Filename of .hdf5 data file.

    Returns
    -------
    phi : np.ndarray of float [N_nodes]
        Electric potential in the nodes of the mesh.
    da_dt : np.ndarray of float [N_nodesx3]
        Magnetic vector potential in the nodes of the mesh.
    """
    with h5py.File(fname, 'r') as f:
        phi = np.array(f['data/potential'])  # [N_nodes]
        # [3*N_nodes x 1]
        da_dt = np.array(f['data/dAdt'])
        da_dt = np.reshape(da_dt, (phi.shape[0], 3), order='c')  # [N_nodes x 3]
    return phi, da_dt


def load_mesh_msh(fname):
    """
    Loading mesh from .msh file and return :py:class:`~pynibs.mesh.mesh_struct.TetrahedraLinear` object.

    Parameters
    ----------
    fname : str
        .msh filename (incl. path)

    Returns
    -------
    obj : pynibs.mesh.mesh_struct.TetrahedraLinear
    """
    import simnibs
    msh_msh = simnibs.read_msh(fname)

    points = msh_msh.nodes.node_coord
    triangles = msh_msh.elm.node_number_list[msh_msh.elm.elm_type == 2, 0:3]
    tetrahedra = msh_msh.elm.node_number_list[msh_msh.elm.elm_type == 4, 0:4]

    if tetrahedra.shape[0] == 0:
        offset_idx = np.min(triangles)
        tetrahedra_regions, tetrahedra = np.array(()), np.array(())
        triangles = triangles - offset_idx  # set start index to 0
    elif triangles.shape[0] == 0:
        triangles_regions, triangles = np.array(()), np.array(())
        tetrahedra_regions = msh_msh.elm.tag2[msh_msh.elm.elm_type == 4]
    else:
        offset_idx = np.min(np.array([np.min(triangles), np.min(tetrahedra)]))
        tetrahedra = tetrahedra - offset_idx  # set start index to 0
        tetrahedra_regions = msh_msh.elm.tag2[msh_msh.elm.elm_type == 4]
        triangles = triangles - offset_idx  # set start index to 0

    triangles_regions = msh_msh.elm.tag2[msh_msh.elm.elm_type == 2]

    obj = pynibs.mesh_struct.TetrahedraLinear(points, triangles, triangles_regions, tetrahedra, tetrahedra_regions)

    return obj


def load_mesh_hdf5(fname):
    """
    Loading mesh from .hdf5 file and setting up :py:class:`~pynibs.mesh.mesh_struct.TetrahedraLinear` class.

    Parameters
    ----------
    fname : str
        Name of .hdf5 file (incl. path)

    Returns
    -------
    obj : pynibs.mesh.mesh_struct.TetrahedraLinear
        :py:class:`~pynibs.mesh.mesh_struct.TetrahedraLinear` object

    Example
    -------
    .hdf5 file format and contained groups. The content of .hdf5 files can be shown using the tool HDFView
    (https://support.hdfgroup.org/products/java/hdfview/)

    .. code-block:: sh

        mesh
        I---/elm
        I    I--/elm_number          [1,2,3,...,N_ele]           Running index over all elements starting at 1,
                                                                    triangles and tetrahedra
        I    I--/elm_type            [2,2,2,...,4,4]             Element type: 2 triangles, 4 tetrahedra
        I    I--/node_number_list    [1,5,6,0;... ;1,4,8,9]      Connectivity of triangles [X, X, X, 0] and tetrahedra
                                                                            [X, X, X, X]
        I    I--/tag1                [1001,1001, ..., 4,4,4]     Surface (100X) and domain (X) indices with 1000 offset
                                                                             for surfaces
        I    I--/tag2                [   1,   1, ..., 4,4,4]     Surface (X) and domain (X) indices w/o offset
        I
        I---/nodes
        I    I--/node_coord          [1.254, 1.762, 1.875;...]   Node coordinates in (mm)
        I    I--/node_number         [1,2,3,...,N_nodes]         Running index over all points starting at 1
        I    I--/units               ["mm"]                      .value is unit of geometry
        I
        I---/fields
        I    I--/E/value             [E_x_1, E_y_1, E_z_1;...]   Electric field in all elms, triangles and tetrahedra
        I    I--/J/value             [J_x_1, J_y_1, J_z_1;...]   Current density in all elms, triangles and tetrahedra
        I    I--/normE/value         [normE_1,..., normE_N_ele]  Magnitude of electric field in all elements,
                                                                            triangles and tetrahedra
        I    I--/normJ/value         [normJ_1,..., normJ_N_ele]  Magnitude of current density in all elements,
                                                                            triangles and tetrahedra

        /data
        I---/potential               [phi_1, ..., phi_N_nodes]   Scalar electric potential in nodes (size N_nodes)
        I---/dAdt                    [A_x_1, A_y_1, A_z_1,...]   Magnetic vector potential (size 3xN_nodes)
    """
    with h5py.File(fname, 'r') as f:
        if 'mesh' in f.keys():
            points = np.array(f['mesh/nodes/node_coord'])
            # node_number_list = np.array(f['mesh/elm/node_number_list'])
            # elm_type = np.array(f['mesh/elm/elm_type'])
            # regions = np.array(f['mesh/elm/tag1'])
            triangles = np.array(f['mesh/elm/triangle_number_list'])  # node_number_list[elm_type == 2, 0:3]
            tetrahedra = np.array(f['mesh/elm/tetrahedra_number_list'])  # node_number_list[elm_type == 4, ]
            triangles_regions = np.array(f['mesh/elm/tri_tissue_type'])
            tetrahedra_regions = np.array(f['mesh/elm/tet_tissue_type'])
        else:
            points = np.array(f['nodes/node_coord'])
            # node_number_list = np.array(f['elm/node_number_list'])
            # elm_type = np.array(f['elm/elm_type'])
            # regions = np.array(f['elm/tag1'])
            triangles = np.array(f['elm/triangle_number_list'])  # node_number_list[elm_type == 2, 0:3]
            tetrahedra = np.array(f['elm/tetrahedra_number_list'])  # node_number_list[elm_type == 4, ]
            triangles_regions = np.array(f['elm/tri_tissue_type'])
            tetrahedra_regions = np.array(f['elm/tet_tissue_type'])
    obj = pynibs.mesh_struct.TetrahedraLinear(points, triangles, triangles_regions, tetrahedra, tetrahedra_regions)
    return obj


def write_geo_hdf5(out_fn, msh, roi_dict=None, hdf5_path='/mesh'):
    """
    Creates a .hdf5 file with geometry data from mesh including region of interest(s).

    Parameters
    ----------
    out_fn : str
        Output hdf5 filename for mesh' geometry information.
    msh: pynibs.mesh.mesh_struct.TetrahedraLinear
        Mesh to write to file.
    roi_dict : dict of (:py:class:`~pynibs.roi.RegionOfInterestSurface` or :py:class:`~pynibs.RegionOfInterestVolume`)
        Region of interest (surface and/or volume) information.
    hdf5_path : str, default: '/mesh'
        Path in output file to store geometry information.

    Returns
    -------
    <File> : .hdf5 file
        File containing the geometry information

    Example
    -------
    File structure of .hdf5 geometry file

    .. code-block:: sh

        mesh
        I---/elm
        I    I--/elm_number             [1,2,3,...,N_ele]        Running index over all elements starting at 1
                                                                    (triangles and tetrahedra)
        I    I--/elm_type               [2,2,2,...,4,4]          Element type: 2 triangles, 4 tetrahedra
        I    I--/tag1                [1001,1001, ..., 4,4,4]     Surface (100X) and domain (X) indices with 1000
                                                                            offset for surfaces
        I    I--/tag2                [   1,   1, ..., 4,4,4]     Surface (X) and domain (X) indices w/o offset
        I    I--/triangle_number_list   [1,5,6;... ;1,4,8]       Connectivity of triangles [X, X, X]
        I    I--/tri_tissue_type        [1,1, ..., 3,3,3]        Surface indices to differentiate between surfaces
        I    I--/tetrahedra_number_list [1,5,6,7;... ;1,4,8,12]  Connectivity of tetrahedra [X, X, X, X]
        I    I--/tet_tissue_type        [1,1, ..., 3,3,3]        Volume indices to differentiate between volumes
        I    I--/node_number_list       [1,5,6,0;... ;1,4,8,9]   Connectivity of triangles [X, X, X, 0] and
                                                                    tetrahedra [X, X, X, X]
        I
        I---/nodes
        I    I--/node_coord          [1.254, 1.762, 1.875;...]   Node coordinates in (mm)
        I    I--/node_number         [1,2,3,...,N_nodes]         Running index over all points starting at 1
        I    I--/units               ['mm']                      .value is unit of geometry

        roi_surface
        I---/0                                                           Region of Interest number
        I    I--/node_coord_up              [1.254, 1.762, 1.875;...]    Coordinates of upper surface points
        I    I--/node_coord_mid             [1.254, 1.762, 1.875;...]    Coordinates of middle surface points
        I    I--/node_coord_low             [1.254, 1.762, 1.875;...]    Coordinates of lower surface points
        I    I--/tri_center_coord_up        [1.254, 1.762, 1.875;...]    Coordinates of upper triangle centers
        I    I--/tri_center_coord_mid       [1.254, 1.762, 1.875;...]    Coordinates of middle triangle centers
        I    I--/tri_center_coord_low       [1.254, 1.762, 1.875;...]    Coordinates of lower triangle centers
        I    I--/node_number_list           [1,5,6,0;... ;1,4,8,9]       Connectivity of triangles [X, X, X]
        I    I--/delta                      0.5                          Distance parameter between GM and WM surface
        I    I--/tet_idx_tri_center_up      [183, 913, 56, ...]          Tetrahedra indices where triangle center of
                                                                            upper surface are lying in
        I    I--/tet_idx_tri_center_mid     [185, 911, 58, ...]          Tetrahedra indices where triangle center of
                                                                            middle surface are lying in
        I    I--/tet_idx_tri_center_low     [191, 912, 59, ...]          Tetrahedra indices where triangle center of
                                                                            lower surface are lying in
        I    I--/tet_idx_node_coord_mid     [12, 15, 43, ...]            Tetrahedra indices where the node_coords_mid
                                                                            are lying in
        I    I--/gm_surf_fname              .../surf/lh.pial             Filename of GM surface from segmentation
        I    I--/wm_surf_fname              .../surf/lh.white            Filename of WM surface from segmentation
        I    I--/layer                      3                            Number of layers
        I    I--/fn_mask                    .../simnibs/mask.mgh         Filename of region of interest mask
        I    I--/X_ROI                      [-10, 15]                    X limits of region of interest box
        I    I--/Y_ROI                      [-10, 15]                    Y limits of region of interest box
        I    I--/Z_ROI                      [-10, 15]                    Z limits of region of interest box
        I
        I---/1
        I    I ...

        roi_volume
        I---/0                                                           Region of Interest number
        I    I--/node_coord                 [1.254, 1.762, 1.875;...]    Coordinates (x,y,z) of ROI nodes
        I    I--/tet_node_number_list       [1,5,6,7;... ;1,4,8,9]       Connectivity matrix of ROI tetrahedra
        I    I--/tri_node_number_list       [1,5,6;... ;1,4,8]           Connectivity matrix of ROI triangles
        I    I--/tet_idx_node_coord         [183, 913, 56, ...]          Tetrahedra indices where ROI nodes are
        I    I--/tet_idx_tetrahedra_center  [12, 15, 43, ...]            Tetrahedra indices where center points of
                                                                            ROI tetrahedra are
        I    I--/tet_idx_triangle_center    [12, 15, 43, ...]            Tetrahedra indices where center points of
                                                                            ROI triangles are

        I---/1
        I    I ...
    """
    if os.path.exists(out_fn):
        os.remove(out_fn)

    with h5py.File(out_fn, 'w') as f:
        f.create_dataset(hdf5_path + '/elm/elm_number', data=np.arange(msh.N_tet + msh.N_tri) + 1)
        f.create_dataset(hdf5_path + '/elm/elm_type', data=np.array([2] * msh.N_tri + [4] * msh.N_tet))
        f.create_dataset(hdf5_path + '/elm/tag1',
                         data=np.hstack((msh.triangles_regions + 1000, msh.tetrahedra_regions)).flatten())
        f.create_dataset(hdf5_path + '/elm/tag2',
                         data=np.hstack((msh.triangles_regions, msh.tetrahedra_regions)).flatten())
        f.create_dataset(hdf5_path + '/elm/triangle_number_list', data=msh.triangles)
        f.create_dataset(hdf5_path + '/elm/tri_tissue_type', data=msh.triangles_regions.flatten())
        f.create_dataset(hdf5_path + '/elm/tetrahedra_number_list', data=msh.tetrahedra)
        f.create_dataset(hdf5_path + '/elm/tet_tissue_type', data=msh.tetrahedra_regions.flatten())
        if msh.tetrahedra.size != 0:
            if msh.triangles.size != 0:
                f.create_dataset(hdf5_path + '/elm/node_number_list', data=np.vstack(
                        (np.hstack((msh.triangles, np.zeros((msh.N_tri, 1)))),
                         msh.tetrahedra)).astype(int))
            else:
                f.create_dataset(hdf5_path + '/elm/node_number_list', data=msh.tetrahedra).astype(int)
        else:
            f.create_dataset(hdf5_path + '/elm/node_number_list', data=np.vstack(
                    (np.hstack((msh.triangles, np.zeros((msh.N_tri, 1)))),
                     )).astype(int))
        f.create_dataset(hdf5_path + '/nodes/node_coord', data=msh.points)
        f.create_dataset(hdf5_path + '/nodes/node_number', data=np.arange(msh.N_points) + 1)
        # f.create_dataset(hdf5_path + '/nodes/units', data=['mm'])
        f.create_dataset(hdf5_path + '/elm/tet_elm_type', data=np.array([4] * msh.N_tet))
        f.create_dataset(hdf5_path + '/elm/tri_elm_type', data=np.array([2] * msh.N_tri))

        if roi_dict is not None:
            for roi_key in roi_dict.keys():
                # save roi surface information
                if roi_dict[roi_key].__class__.__name__ == 'RegionOfInterestSurface':

                    f.create_dataset(f'roi_surface/{roi_key}/node_coord_up',
                                     data=np.array(roi_dict[roi_key].node_coord_up))
                    f.create_dataset(f'roi_surface/{roi_key}/node_coord_mid',
                                     data=np.array(roi_dict[roi_key].node_coord_mid))
                    f.create_dataset(f'roi_surface/{roi_key}/node_coord_low',
                                     data=np.array(roi_dict[roi_key].node_coord_low))
                    f.create_dataset(f'roi_surface/{roi_key}/tri_center_coord_up',
                                     data=np.array(roi_dict[roi_key].tri_center_coord_up))
                    f.create_dataset(f'roi_surface/{roi_key}/tri_center_coord_mid',
                                     data=np.array(roi_dict[roi_key].tri_center_coord_mid))
                    f.create_dataset(f'roi_surface/{roi_key}/tri_center_coord_low',
                                     data=np.array(roi_dict[roi_key].tri_center_coord_low))
                    f.create_dataset(f'roi_surface/{roi_key}/node_number_list',
                                     data=np.array(roi_dict[roi_key].node_number_list))
                    f.create_dataset(f'roi_surface/{roi_key}/delta',
                                     data=np.array(roi_dict[roi_key].delta))

                    if roi_dict[roi_key].tet_idx_tri_center_up is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/tet_idx_tri_center_up',
                                         data=np.array(roi_dict[roi_key].tet_idx_tri_center_up).astype(int))

                    f.create_dataset(f'roi_surface/{roi_key}/tet_idx_tri_center_mid',
                                     data=np.array(roi_dict[roi_key].tet_idx_tri_center_mid).astype(int))

                    if roi_dict[roi_key].tet_idx_tri_center_low is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/tet_idx_tri_center_low',
                                         data=np.array(roi_dict[roi_key].tet_idx_tri_center_low).astype(int))

                    f.create_dataset(f'roi_surface/{roi_key}/tet_idx_node_coord_mid',
                                     data=np.array(roi_dict[roi_key].tet_idx_node_coord_mid).astype(int))
                    f.create_dataset(f'roi_surface/{roi_key}/gm_surf_fname',
                                     data=np.array(roi_dict[roi_key].gm_surf_fname).astype("S"))
                    f.create_dataset(f'roi_surface/{roi_key}/wm_surf_fname',
                                     data=np.array(roi_dict[roi_key].wm_surf_fname).astype("S"))
                    f.create_dataset(f'roi_surface/{roi_key}/midlayer_surf_fname',
                                     data=np.array(roi_dict[roi_key].midlayer_surf_fname).astype("S"))
                    f.create_dataset(f'roi_surface/{roi_key}/layer',
                                     data=roi_dict[roi_key].layer)
                    f.create_dataset(f'roi_surface/{roi_key}/refine',
                                     data=roi_dict[roi_key].refine)

                    if roi_dict[roi_key].fn_mask is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/fn_mask',
                                         data=np.array(roi_dict[roi_key].fn_mask).astype("S"))

                    if roi_dict[roi_key].X_ROI is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/X_ROI',
                                         data=np.array(roi_dict[roi_key].X_ROI))

                    if roi_dict[roi_key].Y_ROI is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/Y_ROI',
                                         data=np.array(roi_dict[roi_key].Y_ROI))

                    if roi_dict[roi_key].Z_ROI is not None:
                        f.create_dataset(f'roi_surface/{roi_key}/Z_ROI',
                                         data=np.array(roi_dict[roi_key].Z_ROI))

                    if roi_dict[roi_key].layers is not None:
                        for layer in roi_dict[roi_key].layers:
                            f.create_dataset(f'roi_surface/{roi_key}/layers/{layer.id}/node_coord',
                                             data=np.array(layer.surface.nodes.node_coord))
                            f.create_dataset(f'roi_surface/{roi_key}/layers/{layer.id}/node_number_list',
                                             data=np.array(layer.surface.elm.node_number_list[:, :3] - 1))

                # save roi volume information
                if roi_dict[roi_key].__class__.__name__ == 'RegionOfInterestVolume':

                    f.create_dataset(f'roi_volume/{roi_key}/node_coord',
                                     data=np.array(roi_dict[roi_key].node_coord))
                    f.create_dataset(f'roi_volume/{roi_key}/tet_node_number_list',
                                     data=np.array(roi_dict[roi_key].tet_node_number_list))
                    f.create_dataset(f'roi_volume/{roi_key}/tri_node_number_list',
                                     data=np.array(roi_dict[roi_key].tri_node_number_list))

                    if roi_dict[roi_key].tet_idx_node_coord is not None:
                        f.create_dataset(f'roi_volume/{roi_key}/tet_idx_node_coord',
                                         data=np.array(roi_dict[roi_key].tet_idx_node_coord))

                    f.create_dataset(f'roi_volume/{roi_key}/tet_idx_tetrahedra_center',
                                     data=np.array(roi_dict[roi_key].tet_idx_tetrahedra_center))
                    f.create_dataset(f'roi_volume/{roi_key}/tet_idx_triangle_center',
                                     data=np.array(roi_dict[roi_key].tet_idx_triangle_center))


def write_geo_hdf5_surf(out_fn, points, con, replace=False, hdf5_path='/mesh'):
    """
    Creates a .hdf5 file with geometry data from midlayer.

    Parameters
    ----------
    out_fn : str
        Filename of output .hdf5 file containing the geometry information.
    points : np.ndarray
        (N_points, 3) Coordinates of nodes (x,y,z).
    con : np.ndarray
        (N_tri, 3) Connectivity list of triangles.
    replace : bool
        Replace .hdf5 geometry file (True / False).
    hdf5_path : str, default: '/mesh'
        Folder in .hdf5 geometry file, where the geometry information is saved in.

    Returns
    -------
    <File> : .hdf5 file
        File containing the geometry information.

    Example
    -------
    File structure of .hdf5 geometry file:

    .. code-block:: sh

        mesh
        |---/elm
        |    |--/triangle_number_list   [1,5,6;... ;1,4,8]      Connectivity of triangles [X, X, X]
        |    |--/tri_tissue_type        [1,1, ..., 3,3,3]       Surface indices to differentiate between surfaces
        |
        |---/nodes
        |    |--/node_coord             [1.2, 1.7, 1.8; ...]    Node coordinates in (mm)
    """
    assert out_fn.endswith('.hdf5') or out_fn.endswith('.h5')
    os.makedirs(os.path.split(out_fn)[0], exist_ok=True)

    if os.path.exists(out_fn):
        os.remove(out_fn)

    if not con.min() == 0:
        warnings.warn("Minunum connectivity is not 0.")

    with h5py.File(out_fn, 'w') as h5:
        h5.create_dataset(hdf5_path + '/nodes/' + 'node_coord',
                          data=points)
        h5.create_dataset(hdf5_path + '/elm/triangle_number_list',
                          data=con)
        h5.create_dataset(hdf5_path + '/elm/tri_tissue_type',
                          data=np.zeros((points.shape[0], 1)).astype(int))


def write_geo_hdf5_vol(out_fn, points, con, replace=False, hdf5_path='/mesh'):
    """
    Creates a .hdf5 file with geometry data from midlayer.

    Parameters
    ----------
    out_fn : str
        Filename of output .hdf5 file containing the geometry information.
    points : np.ndarray
        (N_points, 3) Coordinates of nodes (x,y,z).
    con : np.ndarray
        (N_tri, 3) Connectivity list of triangles.
    replace : bool
        Replace .hdf5 geometry file (True / False).
    hdf5_path : str, default: '/mesh'
        Folder in .hdf5 geometry file, where the geometry information is saved in.

    Returns
    -------
    <File> : .hdf5 file
        File containing the geometry information.

    Example
    -------
    File structure of .hdf5 geometry file:

    .. code-block:: sh

        mesh
        |---/elm
        |    |--/triangle_number_list   [1,5,6;... ;1,4,8]      Connectivity of triangles [X, X, X]
        |    |--/tri_tissue_type        [1,1, ..., 3,3,3]       Surface indices to differentiate between surfaces
        |
        |---/nodes
        |    |--/node_coord             [1.2, 1.7, 1.8; ...]    Node coordinates in (mm)
    """
    if os.path.exists(out_fn):
        os.remove(out_fn)

    with h5py.File(out_fn, 'w') as h5:
        h5.create_dataset(hdf5_path + '/nodes/' + 'node_coord',
                          data=points)
        h5.create_dataset(hdf5_path + '/elm/tetrahedra_number_list',
                          data=con)
        h5.create_dataset(hdf5_path + '/elm/tet_tissue_type',
                          data=np.zeros((points.shape[0], 1)).astype(int))


def write_data_hdf5(out_fn, data, data_names, hdf5_path='/data', mode="a"):
    """
    Creates a .hdf5 file with data.

    Parameters
    ----------
    out_fn : str
        Filename of output .hdf5 file containing the geometry information.
    data : np.ndarray or list of nparrays of float
        Data to save in hdf5 data file.
    data_names : str or list of str
        Labels of data.
    hdf5_path : str, default: '/data'
        Folder in .hdf5 geometry file, where the data is saved in.
    mode : str, default: "a"
        Mode: "a" append, "w" write (overwrite).

    Returns
    -------
    <File> : .hdf5 file
        File containing the stored data.

    Example
    -------
    File structure of .hdf5 data file

    .. code-block:: sh

        data
        |---/data_names[0]          [data[0]]           First dataset
        |---/    ...                   ...                  ...
        |---/data_names[N-1]        [data[N-1]]         Last dataset
    """
    if type(data) is not list:
        data = [data]

    if type(data_names) is not list:
        data_names = [data_names]

    assert len(data_names) == len(data), f"Different number of data_names {len(data_names)} and data ({len(data)}."
    with h5py.File(out_fn, mode) as f:
        for i, data_name in enumerate(data_names):
            if isinstance(data[i], np.ndarray):
                f.create_dataset(hdf5_path + '/' + data_name, data=data[i], dtype="float64")
            else:
                f.create_dataset(hdf5_path + '/' + data_name, data=data[i])


def write_data_hdf5_surf(data, data_names, data_hdf_fn_out, geo_hdf_fn,
                         replace=False, replace_array_in_file=True, datatype='tris'):
    """
    Saves surface data to .hdf5 data file and generates corresponding .xdmf file linking both.
    The directory of data_hdf_fn_out and geo_hdf_fn should be the same, as only basenames of files are stored
    in the .xdmf file.

    Parameters
    ----------
    data : np.ndarray or list
        (N_points_ROI, N_components) Data to map on surfaces.
    data_names : str or list
        Names for datasets.
    data_hdf_fn_out : str
        Filename of .hdf5 data file.
    geo_hdf_fn : str
        Filename of .hdf5 geo file containing the geometry information (has to exist).
    replace : bool, default: False
        Replace existing .hdf5 and .xdmf file completely.
    replace_array_in_file : bool, default: True
        Replace existing array in file.
    datatype : str, default: 'tris'
        Triangle or node data.

    Returns
    -------
    <File> : .hdf5 file
        data_hdf_fn_out.hdf5 containing data
    <File> : .xdmf file
        data_hdf_fn_out.xdmf containing information about .hdf5 file structure for Paraview

    Example
    -------
    File structure of .hdf5 data file

    .. code-block:: sh

        /data
        |---/tris
        |      |---dataset_0    [dataset_0]    (size: N_dataset_0 x M_dataset_0)
        |      |---   ...
        |      |---dataset_K   [dataset_K]     (size: N_dataset_K x M_dataset_K)
    """
    assert datatype in ['tris', 'nodes']

    # Check if files already exists
    try:
        if data_hdf_fn_out[-4:] != 'hdf5':
            data_hdf_fn_out += '.hdf5'
    except IndexError:
        data_hdf_fn_out += '.hdf5'

    data_xdmf_fn = data_hdf_fn_out[:-4] + 'xdmf'
    if os.path.exists(data_hdf_fn_out):
        if replace:
            os.remove(data_hdf_fn_out)
        elif not replace and replace_array_in_file:
            pass
        else:
            raise FileExistsError(data_hdf_fn_out + " already exists")
    if os.path.exists(data_xdmf_fn):
        if replace:
            os.remove(data_xdmf_fn)
        elif not replace and replace_array_in_file:
            pass
        else:
            raise FileExistsError(data_xdmf_fn + " already exists")

    # Check for correct data and data_names
    if type(data) is np.ndarray:
        data = [data]
    elif type(data) is list:
        for dat in data:
            if type(dat) is not np.ndarray:
                raise NotImplementedError
    else:
        raise NotImplementedError

    if type(data_names) is str:
        data_names = [data_names]
    elif type(data_names) is not list:
        raise NotImplementedError

    if len(data) != len(data_names):
        raise ValueError(f'Dimension mismatch, data (len: {len(data)}) <-> data_names (len: {len(data_names)})')

    with h5py.File(data_hdf_fn_out, 'a') as h5_data:

        # write data
        only_data_replaced = True  # keep .xdmf if some data is only replaced in .hdf5 file and no new data is added

        for idx, dat in enumerate(data):
            if replace_array_in_file:
                try:
                    del h5_data[f'/data/{datatype}/' + data_names[idx]]
                except KeyError:
                    only_data_replaced = False

            else:
                only_data_replaced = False

            h5_data.create_dataset(f'/data/{datatype}/' + data_names[idx], data=data[idx])

    if not only_data_replaced:
        data_dims = [dat.shape[1] if dat.ndim > 1 else 1 for dat in data]
        pynibs.write_xdmf_surf(data_hdf_fn_out, data_names, data_xdmf_fn, geo_hdf_fn, data_dims)


def write_data_hdf5_vol(data, data_names, data_hdf_fn_out, geo_hdf_fn, replace=False, replace_array_in_file=True):
    """
    Saves surface data to .hdf5 data file and generates corresponding .xdmf file linking both.
    The directory of data_hdf_fn_out and geo_hdf_fn should be the same, as only basenames of files are stored
    in the .xdmf file.

    Parameters
    ----------
    data : np.ndarray or list
        (N_points_ROI, N_components) Data to map on surfaces.
    data_names : str or list
        Names for datasets.
    data_hdf_fn_out : str
        Filename of .hdf5 data file.
    geo_hdf_fn : str
        Filename of .hdf5 geo file containing the geometry information (has to exist).
    replace : bool, default: False
        Replace existing .hdf5 and .xdmf file completely.
    replace_array_in_file : bool, default: True
        Replace existing array in file.

    Returns
    -------
    <File> : .hdf5 file
        data_hdf_fn_out.hdf5 containing data
    <File> : .xdmf file
        data_hdf_fn_out.xdmf containing information about .hdf5 file structure for Paraview.

    Example
    -------
    File structure of .hdf5 data file

    .. code-block:: sh

        /data
        |---/tris
        |      |---dataset_0    [dataset_0]    (size: N_dataset_0 x M_dataset_0)
        |      |---   ...
        |      |---dataset_K   [dataset_K]     (size: N_dataset_K x M_dataset_K)
    """
    # Check if files already exists
    try:
        if data_hdf_fn_out[-4:] != 'hdf5':
            data_hdf_fn_out += '.hdf5'
    except IndexError:
        data_hdf_fn_out += '.hdf5'

    data_xdmf_fn = data_hdf_fn_out[:-4] + 'xdmf'
    if os.path.exists(data_hdf_fn_out):
        if replace:
            os.remove(data_hdf_fn_out)
        elif not replace and replace_array_in_file:
            pass
        else:
            warnings.warn(data_hdf_fn_out + " already exists. Quitting")
            return
    if os.path.exists(data_xdmf_fn):
        if replace:
            os.remove(data_xdmf_fn)
        elif not replace and replace_array_in_file:
            pass
        else:
            warnings.warn(data_xdmf_fn + " already exists. Quitting")
            return

    # Check for correct data and data_names
    if type(data) == np.ndarray:
        data = [data]
    elif type(data) == list:
        for dat in data:
            if type(dat) is not np.ndarray:
                raise NotImplementedError
    else:
        raise NotImplementedError

    if type(data_names) is str:
        data_names = [data_names]
    elif type(data_names) is not list:
        raise NotImplementedError

    if len(data) != len(data_names):
        raise ValueError(f'Dimension mismatch, data (len: {len(data)}) <-> data_names (len: {len(data_names)})')

    with h5py.File(data_hdf_fn_out, 'a') as h5_data, \
            h5py.File(geo_hdf_fn, 'r') as h5_geo:

        # if geo file exists in same folder than data file only use relative path
        if os.path.split(data_hdf_fn_out) == os.path.split(geo_hdf_fn):
            geo_hdf_fn = os.path.basename(geo_hdf_fn)

        # write data
        only_data_replaced = True  # keep .xdmf if some data is only replaced in .hdf5 file and no new data is added

        for idx, dat in enumerate(data):
            if replace_array_in_file:
                try:
                    del h5_data['/data/tris/' + data_names[idx]]
                except KeyError:
                    only_data_replaced = False

            else:
                only_data_replaced = False

            h5_data.create_dataset('/data/tets/' + data_names[idx], data=data[idx])

        if not only_data_replaced:
            with open(data_xdmf_fn, 'w') as xdmf:
                # write xdmf file linking the data to the surfaces in geo_hdf_fn
                xdmf.write('<?xml version="1.0"?>\n')
                xdmf.write('<!DOCTYPE Xdmf SYSTEM "Xdmf.dtd" []>\n')
                xdmf.write('<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
                xdmf.write('<Domain>\n')

                # one collection grid
                xdmf.write('<Grid\nCollectionType="Spatial"\nGridType="Collection"\nName="Collection">\n')

                # read all available surfaces
                volume = []
                lookup_str = 'tetrahedra_number_list_'
                lookup_str_node = 'node_coord_'
                lookup_str_tri = 'tet_tissue_type_'

                keys = list(h5_geo['mesh/elm/'].keys())
                for key in keys:
                    idx = key.find(lookup_str)
                    if idx >= 0:
                        volume.append(key[(idx + len(lookup_str)):])

                if not volume:
                    volume = []
                    lookup_str = 'tetrahedra_number_list'
                    lookup_str_node = 'node_coord'
                    lookup_str_tri = 'tet_tissue_type'
                    keys = list(h5_geo['mesh/elm/'].keys())
                    for key in keys:
                        idx = key.find(lookup_str)
                        if idx >= 0:
                            volume.append(key[(idx + len(lookup_str)):])

                data_written = False

                for vol in volume:

                    n_tets = len(h5_geo['/mesh/elm/' + lookup_str + vol][:])
                    n_nodes = len(h5_geo['/mesh/nodes/' + lookup_str_node + vol][:])
                    assert n_tets, n_nodes

                    # one grid for triangles...
                    ###########################
                    xdmf.write('<Grid Name="tris" GridType="Uniform">\n')
                    xdmf.write('<Topology NumberOfElements="' + str(n_tets) +
                               '" TopologyType="Tetrahedron" Name="' + vol + '_Tet">\n')
                    xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_tets) + ' 4">\n')
                    xdmf.write(geo_hdf_fn + ':' + '/mesh/elm/' + lookup_str + vol + '\n')
                    xdmf.write('</DataItem>\n')
                    xdmf.write('</Topology>\n')

                    # nodes
                    xdmf.write('<Geometry GeometryType="XYZ">\n')
                    xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_nodes) + ' 3">\n')
                    xdmf.write(geo_hdf_fn + ':' + '/mesh/nodes/' + lookup_str_node + vol + '\n')
                    xdmf.write('</DataItem>\n')
                    xdmf.write('</Geometry>\n')

                    # data
                    for idx, dat in enumerate(data):
                        data_dim = dat.shape[1] if dat.ndim > 1 else 1

                        xdmf.write('<Attribute Name="' + data_names[idx] + '" AttributeType="Scalar" Center="Cell">\n')
                        xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_tets) + ' ' + str(data_dim) + '">\n')
                        xdmf.write(os.path.basename(data_hdf_fn_out) + ':' + '/data/tets/' + data_names[idx] + '\n')
                        xdmf.write('</DataItem>\n')
                        xdmf.write('</Attribute>\n')

                    # tissue_type
                    xdmf.write('<Attribute Name="tissue_type" AttributeType="Scalar" Center="Node">\n')
                    xdmf.write('<DataItem Format="HDF" Dimensions="' + str(n_nodes) + ' 1">\n')
                    xdmf.write(geo_hdf_fn + ':' + '/mesh/elm/' + lookup_str_tri + vol + '\n')
                    xdmf.write('</DataItem>\n')
                    xdmf.write('</Attribute>\n')
                    xdmf.write('</Grid>\n')

                xdmf.write('</Grid>\n')
                xdmf.write('</Domain>\n')
                xdmf.write('</Xdmf>\n')


def print_attrs(name, obj):
    """
    Helper function for :py:meth:`hdf_2_ascii()`. To be called from ``h5py.Group.visititems()``

    Parameters
    ----------
    name : str
        Name of structural element.
    obj : object
        Structural element.

    Returns
    -------
    <Print> : Structure of .hdf5 file.
    """
    import h5py

    if isinstance(obj, h5py.Dataset):
        print(('/' + name + '\t\t ' + str(obj.shape)))
    else:
        print(('\n/' + name))

    for key, val in obj.attrs.items():
        print("    %s: %s" % (key, val))


def hdf_2_ascii(hdf5_fn):
    """
    Prints out structure of given .hdf5 file.

    Parameters
    ----------
    hdf5_fn : str
        Filename of .hdf5 file.

    Returns
    -------
    h5 : items
        Structure of .hdf5 file.
    """
    print('/')
    h5 = h5py.File(hdf5_fn, 'r')
    h5.visititems(print_attrs)


def simnibs_results_msh2hdf5_workhorse(fn_msh, fn_hdf5, session, pos_tms_idx, pos_local_idx, subject, mesh_idx,
                                       mode_xdmf="r+",
                                       verbose=False, overwrite=False, mid2roi=False):
    """
    Converts simnibs .msh results file to .hdf5 (including midlayer data if desired)

    Parameters
    ----------
    fn_msh : list of str
        Filenames of .msh results files from SimNIBS.
    fn_hdf5 : str or list of str
        Filenames of .hdf5 results files.
    session : Simnibs Session object
        Simnibs session the simulations were conducted with.
    pos_tms_idx : list of int
        Index of the simulation w.r.t. to the simnibs TMSList (inside ``session``).
        For every coil a separate TMSList exists, which contains multiple coil positions.
    pos_local_idx : list of int
        Index of the simulation w.r.t. to the simnibs POSlist in the TMSList (inside ``session``).
        For every coil a separate TMSList exists, which contains multiple coil positions.
    subject : Subject object
        pynibs.Subject.
    mesh_idx : int or str
        Mesh index or id.
    mode_xdmf : str, default: "r+"
        Mode to open hdf5_geo file to write xdmf. If hdf5_geo is already separated in tets and tris etc.,
        the file is not changed, use "r" to avoid IOErrors in case of parallel computing.
    verbose : bool, default: False
        Print output messages.
    overwrite: bool, default: False
        Overwrite .hdf5 file if existing.
    mid2roi : bool, list of string, or string, default: False
        If the mesh contains ROIs and the e-field was calculated in the midlayer using SimNIBS
        (``S.map_to_surf = True``), the midlayer results will be mapped from the simnibs midlayer to the ROIs
        (takes some time for large ROIs).

    Returns
    -------
    <File> : .hdf5 file
        .hdf5 file containing the results. An .xdmf file is also created to link the results with the mesh .hdf5 file
        of the subject.
    """
    import simnibs
    if type(fn_msh) is not list:
        fn_msh = [fn_msh]

    if type(fn_hdf5) is not list:
        fn_hdf5 = [fn_hdf5]

    if type(mid2roi) is str:
        mid2roi = [mid2roi]

    # Save results in .hdf5 format
    regex = r"[\d]-[\d]{4}"

    idx = np.hstack((np.array(pos_tms_idx)[:, None], np.array(pos_local_idx)[:, None]))

    for f_msh in fn_msh:
        indices = np.array(re.findall(regex, f_msh)[0].split("-")).astype(int) - 1
        f_tms_idx = indices[0]
        f_local_idx = indices[1]
        f_global_idx = np.where((idx == indices).all(axis=1))[0][0]

        if os.path.exists(fn_hdf5[f_global_idx] + ".hdf5") and not overwrite:
            if verbose:
                print(f"Skipping {f_msh} --> {fn_hdf5[f_global_idx]}.hdf5")
            continue

        if verbose:
            print(f"Transforming {f_msh} --> {fn_hdf5[f_global_idx]}.hdf5")

        # read dipole position and magnitude
        fn_coil_geo = os.path.join(session.pathfem,
                                   os.path.splitext(os.path.split(session.fnamehead)[1])[0] +
                                   "_TMS_" +
                                   str(f_tms_idx + 1) + "-" + str(f_local_idx + 1).zfill(4) + "_" +
                                   os.path.splitext(
                                           os.path.splitext(os.path.split(session.poslists[f_tms_idx].fnamecoil)[1])[
                                               0])[0] +
                                   "_nii_coil_pos.geo")

        # for some reason, the .geo file of the simulation was not saved ...
        try:
            dipole_position, dipole_moment_mag = pynibs.read_coil_geo(fn_coil_geo)
        except FileNotFoundError:
            dipole_position = np.array([[0, 0, 0]])
            dipole_moment_mag = np.array([[0]])
            Warning(f"Coil .geo file not found... Skipping coil positions ({fn_coil_geo})")

        # read .msh results file from SimNIBS
        msh = simnibs.read_msh(f_msh)

        # collect data
        data = [dipole_position, dipole_moment_mag]
        data_names = ["coil/dipole_position", "coil/dipole_moment_mag"]

        for i in range(len(msh.nodedata)):
            data_names.append("data/nodes/" + msh.nodedata[i].field_name)
            data.append(msh.nodedata[i].value)

        for i in range(len(msh.elmdata)):
            data_names.append("data/tris/" + msh.elmdata[i].field_name)
            data.append(msh.elmdata[i].value[msh.elm.elm_type == 2,])

            data_names.append("data/tets/" + msh.elmdata[i].field_name)
            data.append(msh.elmdata[i].value[msh.elm.elm_type == 4,])

            # save dadt also in nodes (does require TBs of RAM because of inversion,
            # there is maybe a more elegant way using SimNIBS directly)
            # if msh.elmdata[i].field_name == "D":
            #    data_names.append("data/nodes/D")
            #    con_tets = msh.elm.node_number_list[msh.elm.elm_type == 4, ]
            #    data.append(pynibs.mesh.data_elements2nodes(msh.elmdata[i].value[msh.elm.elm_type == 4, ], con_tets))

        # write .hdf5 file data
        write_data_hdf5(out_fn=os.path.splitext(fn_hdf5[f_global_idx])[0] + ".hdf5",
                        data=data,
                        data_names=data_names,
                        hdf5_path='',
                        mode="w")

        # write .xdmf markup file for paraview
        pynibs.write_xdmf(hdf5_fn=os.path.splitext(fn_hdf5[f_global_idx])[0] + ".hdf5",
                   hdf5_geo_fn=subject.mesh[mesh_idx]["fn_mesh_hdf5"],
                   overwrite_xdmf=True,
                   verbose=False,
                   mode=mode_xdmf)

        # if calculated from Simnibs copy and crop midlayer results to ROIs
        if session.map_to_surf and mid2roi is not False:
            try:

                # load rois
                if verbose:
                    print(f"Loading ROIs")

                roi = pynibs.load_roi_surface_obj_from_hdf5(fname=subject.mesh[mesh_idx]["fn_mesh_hdf5"])
                mesh_folder = os.path.join(subject.subject_folder,
                                           'mesh', str(mesh_idx),
                                           subject.mesh[mesh_idx]["mesh_folder"])

                for roi_idx in roi.keys():
                    # skip rois that are not wanted
                    if isinstance(mid2roi, list) and roi_idx not in mid2roi:
                        continue
                    # load freesurfer surface
                    if type(roi[roi_idx].gm_surf_fname) is not list:
                        roi[roi_idx].gm_surf_fname = [roi[roi_idx].gm_surf_fname]

                    points_gm = [None for _ in range(len(roi[roi_idx].gm_surf_fname))]
                    con_gm = [None for _ in range(len(roi[roi_idx].gm_surf_fname))]

                    max_idx_gm = 0

                    if (type(roi[roi_idx].gm_surf_fname) is list and roi[roi_idx].gm_surf_fname[0] is not None) or \
                            (type(roi[roi_idx].gm_surf_fname) is str):
                        if type(roi[roi_idx].gm_surf_fname) is str:
                            fn_surface = [roi[roi_idx].gm_surf_fname]
                        else:
                            fn_surface = roi[roi_idx].gm_surf_fname

                    elif (type(roi[roi_idx].midlayer_surf_fname) is list and
                          roi[roi_idx].gm_surf_fname is not None) or \
                            (type(roi[roi_idx].midlayer_surf_fname) is str):
                        if type(roi[roi_idx].midlayer_surf_fname) is str:
                            fn_surface = [roi[roi_idx].midlayer_surf_fname]
                        else:
                            fn_surface = roi[roi_idx].midlayer_surf_fname

                    for i in range(len(fn_surface)):
                        if fn_surface[i].endswith('.gii') or fn_surface[i].endswith('.gii.gz'):
                            gii_obj = nibabel.load(os.path.join(mesh_folder, fn_surface[i]))
                            points_gm[i] = gii_obj.darrays[0].data
                            con_gm[i] = gii_obj.darrays[1].data
                        else:
                            points_gm[i], con_gm[i] = nibabel.freesurfer.read_geometry(
                                    os.path.join(mesh_folder, fn_surface[i]))

                        con_gm[i] = con_gm[i] + max_idx_gm
                        max_idx_gm = max_idx_gm + points_gm[i].shape[0]

                    # points_gm = np.vstack(points_gm)
                    con_gm = np.vstack(con_gm)

                    if verbose:
                        print(f"Processing data to ROI #{roi_idx}")

                    if roi[roi_idx].fn_mask is None or roi[roi_idx].fn_mask == []:
                        if roi[roi_idx].X_ROI is None or roi[roi_idx].X_ROI == []:
                            roi[roi_idx].X_ROI = [-np.inf, np.inf]
                        if roi[roi_idx].Y_ROI is None or roi[roi_idx].Y_ROI == []:
                            roi[roi_idx].Y_ROI = [-np.inf, np.inf]
                        if roi[roi_idx].Z_ROI is None or roi[roi_idx].Z_ROI == []:
                            roi[roi_idx].Z_ROI = [-np.inf, np.inf]

                        roi_mask_bool = (roi[roi_idx].node_coord_mid[:, 0] > min(roi[roi_idx].X_ROI)) & (
                                roi[roi_idx].node_coord_mid[:, 0] < max(roi[roi_idx].X_ROI)) & \
                                        (roi[roi_idx].node_coord_mid[:, 1] > min(roi[roi_idx].Y_ROI)) & (
                                                roi[roi_idx].node_coord_mid[:, 1] < max(roi[roi_idx].Y_ROI)) & \
                                        (roi[roi_idx].node_coord_mid[:, 2] > min(roi[roi_idx].Z_ROI)) & (
                                                roi[roi_idx].node_coord_mid[:, 2] < max(roi[roi_idx].Z_ROI))
                        roi_mask_idx = np.where(roi_mask_bool)

                    else:
                        if type(roi[roi_idx].fn_mask) is np.ndarray:
                            if roi[roi_idx].fn_mask.ndim == 0:
                                roi[roi_idx].fn_mask = roi[roi_idx].fn_mask.astype(str).tolist()

                        # read mask from freesurfer mask file
                        mask = nibabel.freesurfer.mghformat.MGHImage.from_filename(
                                os.path.join(mesh_folder, roi[roi_idx].fn_mask)).dataobj[:]
                        roi_mask_idx = np.where(mask > 0.5)

                    # read results data
                    if verbose:
                        print("Reading SimNIBS midlayer data")
                    e_normal = []
                    e_tan = []

                    for fn_surf in fn_surface:
                        fn_msh_base = os.path.splitext(os.path.split(f_msh)[1])[0]

                        if "lh" in os.path.split(fn_surf)[1]:
                            fname_base = os.path.join(os.path.split(f_msh)[0], "subject_overlays", "lh." + fn_msh_base)

                        if "rh" in os.path.split(fn_surf)[1]:
                            fname_base = os.path.join(os.path.split(f_msh)[0], "subject_overlays", "rh." + fn_msh_base)

                        e_normal.append(
                                nibabel.freesurfer.read_morph_data(fname_base + ".central.E.normal").flatten()[:,
                                np.newaxis])
                        e_tan.append(
                                nibabel.freesurfer.read_morph_data(fname_base + ".central.E.tangent").flatten()[:,
                                np.newaxis])

                    e_normal = np.vstack(e_normal)
                    e_tan = np.vstack(e_tan)

                    # transform point data to element data
                    if verbose:
                        print("Transforming point data to element data")
                    e_normal = pynibs.data_nodes2elements(data=e_normal, con=con_gm)
                    e_tan = pynibs.data_nodes2elements(data=e_tan, con=con_gm)

                    # crop results data to ROI
                    # if not roi_mask_bool.all():
                    if roi_mask_idx:
                        if verbose:
                            print("Cropping data to ROI")

                        # get row index where all points are lying inside ROI
                        con_row_idx = [i for i in range(con_gm.shape[0]) if
                                       len(np.intersect1d(con_gm[i,], roi_mask_idx)) == 3]

                        e_normal = e_normal[con_row_idx, :].flatten()
                        e_tan = e_tan[con_row_idx, :].flatten()

                    e_mag = np.linalg.norm(np.vstack([e_normal, e_tan]).transpose(), axis=1).flatten()

                    if verbose:
                        print("Writing data to .hdf5")

                    with h5py.File(os.path.splitext(fn_hdf5[f_global_idx])[0] + ".hdf5", 'a') as f:
                        try:
                            del f['data/midlayer/roi_surface/{}/E_mag'.format(roi_idx)]
                            del f['data/midlayer/roi_surface/{}/E_tan'.format(roi_idx)]
                            del f['data/midlayer/roi_surface/{}/E_norm'.format(roi_idx)]
                        except KeyError:
                            pass

                        f.create_dataset('data/midlayer/roi_surface/{}/E_mag'.format(roi_idx), data=e_mag)
                        f.create_dataset('data/midlayer/roi_surface/{}/E_tan'.format(roi_idx), data=e_tan)
                        f.create_dataset('data/midlayer/roi_surface/{}/E_norm'.format(roi_idx), data=e_normal)

                    del e_mag, e_normal, e_tan
            except KeyError as e:
                warnings.warn(f"Could not map2surf: {e}")

        # Write info in .hdf5 file
        #######################################################################
        with h5py.File(os.path.splitext(fn_hdf5[f_global_idx])[0] + ".hdf5", 'a') as f:
            try:
                del f["info"]
            except KeyError:
                pass

            f.create_dataset("info/date", data=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            f.create_dataset("info/sigma_WM", data=session.poslists[f_tms_idx].cond[0].value)
            f.create_dataset("info/sigma_GM", data=session.poslists[f_tms_idx].cond[1].value)
            f.create_dataset("info/sigma_CSF", data=session.poslists[f_tms_idx].cond[2].value)
            f.create_dataset("info/sigma_Skull", data=session.poslists[f_tms_idx].cond[3].value)
            f.create_dataset("info/sigma_Scalp", data=session.poslists[f_tms_idx].cond[4].value)
            if len(session.poslists[f_tms_idx].cond) > 5:
                f.create_dataset("info/sigma_EyeBalls", data=session.poslists[f_tms_idx].cond[5].value)
            f.create_dataset("info/fn_coil", data=session.poslists[f_tms_idx].fnamecoil)
            if session.poslists[f_tms_idx].pos[f_local_idx].matsimnibs is not None:
                f.create_dataset("info/matsimnibs", data=session.poslists[f_tms_idx].pos[f_local_idx].matsimnibs)
            f.create_dataset("info/dIdt", data=session.poslists[f_tms_idx].pos[f_local_idx].didt)
            f.create_dataset("info/anisotropy_type", data=session.poslists[f_tms_idx].anisotropy_type)
            f.create_dataset("info/fn_mesh_msh", data=session.fnamehead)

        del f_global_idx


def simnibs_results_msh2hdf5(fn_msh, fn_hdf5, S, pos_tms_idx, pos_local_idx, subject, mesh_idx, mode_xdmf="r+",
                             n_cpu=4, verbose=False, overwrite=False, mid2roi=False):
    """
    Converts simnibs .msh results file(s) to .hdf5 / .xdmf tuple.

    Parameters
    ----------
    fn_msh : str list of str
        Filenames (incl. path) of .msh results files from SimNIBS.
    fn_hdf5 : str or list of str
        Filenames (incl. path) of .hdf5 results files.
    S : Simnibs Session object
        Simnibs Session object the simulations are conducted with.
    pos_tms_idx : list of int
        Index of the simulation w.r.t. to the simnibs TMSList (inside Session object S).
        For every coil a separate TMSList exists, which contains multiple coil positions.
    pos_local_idx : list of int
        Index of the simulation w.r.t. to the simnibs POSlist in the TMSList (inside Session object S)
        For every coil a separate TMSList exists, which contains multiple coil positions.
    subject : pynibs.subject.Subject
        Subject object.
    mesh_idx : int or str
        Mesh id.
    mode_xdmf : str, default: "r+"
        Mode to open hdf5_geo file to write xdmf. If hdf5_geo is already separated in tets and tris etc.,
        the file is not changed, use "r" to avoid IOErrors in case of parallel computing.
    n_cpu : int
        Number of processes.
    verbose : bool, default: False
        Print output messages.
    overwrite: bool, default: False
        Overwrite .hdf5 file if existing.
    mid2roi : bool or string, default: False
        If the mesh contains ROIs and the e-field was calculated in the midlayer using simnibs
        (``S.map_to_surf = True``),
        the midlayer results will be mapped from the simnibs midlayer to the ROIs (takes some time for large ROIs).

    Returns
    -------
    <File> : .hdf5 file
        .hdf5 file containing the results. An .xdmf file is also created to link the results with the mesh .hdf5 file
        of the subject.
    """
    n_cpu_available = multiprocessing.cpu_count()
    n_cpu = min(n_cpu, n_cpu_available, len(fn_msh))
    pool = multiprocessing.Pool(n_cpu)
    save_hdf5_partial = partial(simnibs_results_msh2hdf5_workhorse,
                                fn_hdf5=fn_hdf5,
                                session=S,
                                pos_tms_idx=pos_tms_idx,
                                pos_local_idx=pos_local_idx,
                                subject=subject,
                                mesh_idx=mesh_idx,
                                mode_xdmf="r",
                                verbose=verbose,
                                overwrite=overwrite,
                                mid2roi=mid2roi)

    filenames_chunks = pynibs.compute_chunks(fn_msh, n_cpu)
    pool.map(save_hdf5_partial, filenames_chunks)
    pool.close()
    pool.join()


def msh2hdf5(fn_msh=None, skip_roi=False, skip_layer=True, include_data=False,
             approach="mri2mesh", subject=None, mesh_idx=None):
    """
    Transforms mesh from .msh to .hdf5 format. Mesh is read from subject object or from fn_msh.

    Parameters
    ----------
    fn_msh : str, optional
        Filename of .msh file.
    skip_roi : bool, default: False
        Skip generating ROI in .hdf5
    skip_layer : bool, default: True
        Don't create gm layers.
    include_data : bool, default: False
        Also convert data in .msh file to .hdf5 file
    subject : pynibs.Subject, optional
        Subject information, must be set to use skip_roi=False.
    mesh_idx : int or list of int or str or list of str, optional
        Mesh index, the conversion from .msh to .hdf5 is conducted for.
    approach : str
        Approach the headmodel was created with ("mri2mesh" or "headreco").

        .. deprecated:: 0.0.1
            Not supported anymore.


    Returns
    -------
    <File> : .hdf5 file
        .hdf5 file with mesh information
    """
    import simnibs

    if approach is not None:
        warnings.warn("'approach' parameter is depreciated.", category=DeprecationWarning)

    if subject is not None:
        mesh_folder = subject.mesh[mesh_idx]["mesh_folder"]

    # load mesh from .msh file and generate mesh object
    if fn_msh is not None:
        msh = load_mesh_msh(fn_msh)
        print("Loading mesh from file: {}".format(fn_msh))
        out_fn = os.path.splitext(fn_msh)[0] + ".hdf5"

    else:
        print("Loading mesh #{} from .msh file: {}".format(mesh_idx, subject.mesh[mesh_idx]['fn_mesh_msh']))
        msh = load_mesh_msh(subject.mesh[mesh_idx]['fn_mesh_msh'])
        out_fn = subject.mesh[mesh_idx]['fn_mesh_hdf5']

    roi_passed = None
    if not skip_roi:
        assert subject is not None, f"'msh2hdf5(skip_roi=False)': Must provide subject object to write out ROIs. " \
                                    f"Or set 'skip_roi=True'"
        roi = dict()

        if mesh_idx in subject.roi.keys():

            roi[mesh_idx] = dict()

            for roi_idx in subject.roi[mesh_idx].keys():

                print(("\t Initializing ROI #{} {} (type: {})".format(roi_idx,
                                                                      subject.roi[mesh_idx][roi_idx]['info'],
                                                                      subject.roi[mesh_idx][roi_idx]['type'])))
                # surface ROIs
                if subject.roi[mesh_idx][roi_idx]['type'] == 'surface':
                    print("\t\t Generating ROI")
                    # generate RegionOfInterestSurface object instance
                    roi[mesh_idx][roi_idx] = pynibs.RegionOfInterestSurface()
                    # generate the region
                    refine = False
                    try:
                        refine = subject.roi[mesh_idx][roi_idx]['refine']
                    except KeyError:
                        pass
                    roi[mesh_idx][roi_idx].make_GM_WM_surface(
                            gm_surf_fname=subject.roi[mesh_idx][roi_idx]['gm_surf_fname'],
                            wm_surf_fname=subject.roi[mesh_idx][roi_idx]['wm_surf_fname'],
                            midlayer_surf_fname=subject.roi[mesh_idx][roi_idx]['midlayer_surf_fname'],
                            mesh_folder=mesh_folder,
                            delta=subject.roi[mesh_idx][roi_idx]['delta'],
                            x_roi=subject.roi[mesh_idx][roi_idx]['X_ROI'],
                            y_roi=subject.roi[mesh_idx][roi_idx]['Y_ROI'],
                            z_roi=subject.roi[mesh_idx][roi_idx]['Z_ROI'],
                            layer=subject.roi[mesh_idx][roi_idx]['layer'],
                            fn_mask=subject.roi[mesh_idx][roi_idx]['fn_mask'],
                            refine=refine)
                    volmesh = simnibs.read_msh(subject.mesh[mesh_idx]['fn_mesh_msh'])

                    if not skip_layer:
                        try:
                            print("\t\t Generating cortical layers")
                            roi[mesh_idx][roi_idx].generate_cortical_laminae(volmesh)

                            # write .geo files of layers
                            for layer in roi[mesh_idx][roi_idx].layers:
                                fn_geo = os.path.join(subject.mesh[mesh_idx]["mesh_folder"], "roi", roi_idx,
                                                      f"geo_{layer.id}.hdf5")
                                print(f"\t\t Writing layer {layer.id} to {fn_geo}")
                                points = layer.surface.nodes.node_coord
                                con = layer.surface.elm.node_number_list[:, :3] - 1

                                pynibs.write_geo_hdf5_surf(out_fn=fn_geo,
                                                           points=points,
                                                           con=con,
                                                           replace=True,
                                                           hdf5_path='/mesh')
                                pynibs.write_xdmf(hdf5_fn=fn_geo, hdf5_geo_fn=None, overwrite_xdmf=True,
                                                  overwrite_array=True,
                                                  verbose=False, mode="r+")

                            # find tet_idx for roi in triangle_center of all 3 layers
                            print("\t\t Determining tetrahedra indices of triangle centers of midlayer")
                            roi[mesh_idx][roi_idx].determine_element_idx_in_mesh(msh=msh)
                        except ValueError:
                            print("[WARN] Layer creation requested but no white matter found in ROI bounding box."
                                  "Cannot create cortical layers without the white matter boundary surface."
                                  "Layer creation will be skipped...")
                    else:
                        print("\t\t Skipping creation of cortical layers.")

                # volume ROIs
                if subject.roi[mesh_idx][roi_idx]['type'] == 'volume':
                    print("\t\t Generating ROI")
                    # TODO generate ROI here
                    roi[mesh_idx].append(pynibs.RegionOfInterestVolume())
                    # TODO: include make_roi_volume_from_points
                    # generate the region
                    roi[mesh_idx][roi_idx].make_roi_volume_from_msh(msh=msh,
                                                                    volume_type=subject.roi[mesh_idx][roi_idx][
                                                                        'volume_type'],
                                                                    x_roi=subject.roi[mesh_idx][roi_idx]['X_ROI'],
                                                                    y_roi=subject.roi[mesh_idx][roi_idx]['Y_ROI'],
                                                                    z_roi=subject.roi[mesh_idx][roi_idx]['Z_ROI'])

                roi_passed = roi[mesh_idx]

    # save mesh with roi information in .hdf5 format
    write_geo_hdf5(out_fn=out_fn,
                   msh=msh,
                   roi_dict=roi_passed,
                   hdf5_path='/mesh')

    hdf5_geo_fn = None
    if include_data:
        # load mesh in .msh format
        msh_simnibs = simnibs.read_msh(fn_msh)

        for field in msh_simnibs.field:

            # write node data
            if isinstance(msh_simnibs.field[field], simnibs.mesh_io.NodeData):

                data = msh_simnibs.field[field].value

                with h5py.File(out_fn, "a") as f:
                    f.create_dataset("data/nodes/" + field, data=data, dtype="float64")

            # write tet and tri data
            elif isinstance(msh_simnibs.field[field], simnibs.mesh_io.ElementData):
                data_tris = msh_simnibs.field[field].value[msh_simnibs.elm.elm_type == 2,]
                data_tets = msh_simnibs.field[field].value[msh_simnibs.elm.elm_type == 4,]

                with h5py.File(out_fn, "a") as f:
                    f.create_dataset("data/tets/" + field, data=data_tets)
                    f.create_dataset("data/tris/" + field, data=data_tris)
        hdf5_geo_fn = out_fn

    pynibs.write_xdmf(hdf5_fn=out_fn,
               hdf5_geo_fn=hdf5_geo_fn,
               overwrite_xdmf=True,
               verbose=False)


def write_arr_to_hdf5(fn_hdf5, arr_name, data, overwrite_arr=True, verbose=False, check_file_exist=False):
    """
    Takes an array and adds it to an hdf5 file.

    If data is list of dict, ``write_dict_to_hdf5()`` is called for each dict with adapted hdf5-folder name
    Otherwise, data is casted to np.ndarray and dtype of unicode data casted to ``'|S'``.

    Parameters
    ----------
    fn_hdf5 : str
        Filename of .hdf5 file.
    arr_name : str
        Complete path in .hdf5 file with array name.
    data : ndarray, list or dict
        Data to write.
    overwrite_arr : bool, default: True
        Overwrite existing array.
    verbose : bool, default: False
        Print information.
    """
    # dictionary
    if isinstance(data, dict):
        write_dict_to_hdf5(fn_hdf5=fn_hdf5,
                           data=data,
                           folder=f"{arr_name}",
                           verbose=verbose,
                           check_file_exist=check_file_exist)
        return

    # list of dictionaries:
    elif isinstance(data, list) and len(data) > 0 and isinstance(data[0], dict):
        for idx, lst in enumerate(data):
            write_dict_to_hdf5(fn_hdf5=fn_hdf5,
                               data=lst,
                               folder=f"{arr_name}/{idx}",
                               verbose=verbose,
                               check_file_exist=check_file_exist)
        return
    elif not isinstance(data, np.ndarray):
        data = np.array(data)

    # do some type casting from numpy/pd -> h5py
    # date column from experiment.csv is O
    # plotsetting["view"] is O list of list of different length
    # coil1 and coil2 columns names from experiment.csv is <U8
    # coil_mean column name from experiment.csv is <U12
    if data.dtype == 'O' or data.dtype.kind == 'U':
        data = data.astype('|S')
        if verbose:
            warnings.warn(f"Converting array '{arr_name}'' to string")

    try:
        key = os.path.split(arr_name)[1]
        if key.endswith('fname') or key.startswith('fn'):
            if data.dtype.type == np.bytes_:
                data_l = np.char.decode(data, 'UTF-8').tolist()
                if not isinstance(data_l, list):
                    data_l = [data_l]
                for d in data_l:
                    if d and d != 'None':
                        if isinstance(d, list):
                            for d_sublist in d:
                                if not os.path.exists(d_sublist) and check_file_exist:
                                    warnings.warn(f'Key: {arr_name}: file {d_sublist} does not exist.')
                        else:
                            if not os.path.exists(d) and check_file_exist:
                                warnings.warn(f'Key: {arr_name}: file {d} does not exist.')
    except OSError:
        pass

    with h5py.File(fn_hdf5, 'a') as f:
        # create data_set
        if overwrite_arr:
            try:
                del f[arr_name]
            except KeyError:
                pass
        f.create_dataset(arr_name, data=data)


def write_dict_to_hdf5(fn_hdf5, data, folder, check_file_exist=False, verbose=False):
    """
    Takes dict (from subject.py) and passes its keys to write_arr_to_hdf5()

    .. code-block:: python

        fn_hdf5:folder/
                      |--key1
                      |--key2
                      |...

    Parameters
    ----------
    fn_hdf5 : str
    data : dict or pynibs.Mesh
    folder : str
    verbose : bool
    check_file_exist : bool

    """
    for key in data.keys():
        write_arr_to_hdf5(fn_hdf5=fn_hdf5,
                          arr_name=f"{folder}/{key}",
                          data=data[key],
                          verbose=verbose,
                          check_file_exist=check_file_exist)


def read_dict_from_hdf5(fn_hdf5, folder):
    """
    Read all arrays from from hdf5 file and return them as dict

    Parameters
    ----------
    fn_hdf5: str
        Filename of .hdf5 file
    folder: str
        Folder inside .hdf5 file to read

    Returns
    -------
    d : dict
        Dictionary from .hdf5 file folder
    """
    d = dict()
    with h5py.File(fn_hdf5, 'r') as f:
        for key in f[folder].keys():

            # read datasets contained hdf5 folder
            if isinstance(f[folder][key], h5py.Dataset):

                # converting strings saved as np.bytes_ in hdf5 to str and converting 'None' to None
                if type(f[folder][key][()]) == np.bytes_:

                    d[key] = str(f[folder][key][()].astype(str))

                    # setting None values correctly
                    if d[key] == 'None':
                        d[key] = None

                # reading np.ndarray and looking for strings and None
                elif type(f[folder][key][()]) == np.ndarray:
                    d[key] = read_arr_from_hdf5(fn_hdf5, folder + '/' + key)

                else:
                    d[key] = f[folder][key][()]

            # read datasets contained in (multiple) hdf5 sub-folder
            else:
                # d[key] = list()
                # d[key].append(read_dict_from_hdf5(fn_hdf5, f"{folder}/{key}"))
                d[key] = read_dict_from_hdf5(fn_hdf5, f"{folder}/{key}")

    return d


def read_arr_from_hdf5(fn_hdf5, folder):
    """
    Reads array from and .hdf5 files and returns as list:
    Strings are returned as `np.bytes_ to str` and 'None' to None

    Parameters
    ----------
    fn_hdf5: str
        Filename of .hdf5 file.
    folder: str
        Folder inside .hdf5 file to read.

    Returns
    -------
    data_from_hdf5 : list
        List containing data from .hdf5 file.
    """
    arr_1d = False

    with h5py.File(fn_hdf5, 'r') as f:
        a = f[folder][:]

    if a.size == 0:
        return []

    else:
        if a.ndim == 1:
            arr_1d = True
            a = a[np.newaxis, :]

        df = pd.DataFrame(a.tolist())

        with np.nditer(a, op_flags=['readwrite'], flags=["multi_index"]) as it:
            for x in it:
                if type(x[np.newaxis][0]) == np.bytes_:
                    df.iat[it.multi_index] = str(x.astype(str))

                    try:
                        df.iat[it.multi_index] = float(df.iat[it.multi_index])
                    except ValueError:
                        pass

                    if df.iat[it.multi_index] == 'None':
                        df.iat[it.multi_index] = None

        data_from_hdf5 = df.values.tolist()

        if arr_1d:
            data_from_hdf5 = data_from_hdf5[0]

        return data_from_hdf5


def create_fibre_geo_hdf5(fn_fibres_hdf5, overwrite=True):
    """
    Reformats geometrical fibre data and adds a /plot subfolder containing geometrical fibre data including connectivity

    Parameters
    ----------
    fn_fibres_hdf5 : str
        Path to fibre.hdf5 file containing the original fibre data.
    overwrite : bool
        Overwrites existing /plot subfolder in .hdf5 file.
    """
    fibres = []
    # read fibre data from parent folder
    with h5py.File(fn_fibres_hdf5, "a") as f:
        for key in f.keys():
            if key == "plot" and overwrite:
                print("/plot subfolder exists but will be overwritten (overwrite=True)")
                del f[key]
            elif key == "plot" and not overwrite:
                print("/plot subfolder already exists and will not be overwritten (overwrite=False)")
                return None
            else:
                tmp = f[key][:]
                if type(tmp) is np.ndarray and tmp.shape[1] == 3:
                    fibres.append(tmp)

    # concatenate all points
    fibre_points = np.vstack(fibres)

    # create connectivity list
    fibre_con = np.hstack(
            (np.arange(fibre_points.shape[0])[:, np.newaxis], np.arange(fibre_points.shape[0])[:, np.newaxis] + 1))

    # delete connectivities between fibres
    fibre_con = np.delete(fibre_con, np.cumsum([len(fib) for fib in fibres]) - 1, 0)

    # append data to .hdf5
    with h5py.File(fn_fibres_hdf5, "a") as f:
        f.create_dataset(name="plot/fibre_points", data=fibre_points, dtype=float)
        f.create_dataset(name="plot/fibre_con", data=fibre_con, dtype=int)

    # create .xdmf file for plotting
    pynibs.create_fibre_xdmf(fn_fibre_geo_hdf5=fn_fibres_hdf5, overwrite=overwrite)


def write_coil_hdf5(tms_coil, fn):
    """
    Creates .hdf5/.xdmf file tuples with information to visualize SimNIBS .tcd coil information.

    Can be visualized with ParaView (use Glyph plugin to view wires).

    .. figure:: ../doc/images/two_stimulator_coil.png
       :scale: 80 %
       :alt: Example coil visualization

       SimNIBS .tcd coil model from create_two_stimulator_coil.py visualized with ParaView.

    Parameters
    ----------
    tms_coil : SimNIBS.simulation.tms_coil.tms_coil or str
        The coil (object or .tcd file) that shall be written to disk as an .hdf5 file.
    fn : str
        Filename where to write the files.

    Returns
    -------
    fn.hdf5/fn.xdmf : <file>
        Paraview file tuple with casing data.
    fn_wires.hdf5/fn_wires.xdmf : <file>
        Paraview file tuple with wiring data.
    """
    if isinstance(tms_coil, str):
        assert tms_coil.endswith('.tcd'), 'Only .tcd files are supported.'
        import simnibs
        tms_coil = simnibs.simulation.TmsCoil.from_file(tms_coil)

    # take care of output filenames
    folder, fn_coil = os.path.split(fn)
    if not fn_coil.endswith('.hdf5'):
        fn_coil = f"{os.path.splitext(fn_coil)[0]}.hdf5"
    fn_coil_wires = f"{os.path.splitext(fn_coil)[0]}_wires.hdf5"

    # write casing file
    casing_msh = tms_coil.get_mesh(apply_deformation=False,
                                   include_optimization_points=False,
                                   include_coil_elements=False, )

    pynibs.write_geo_hdf5_surf(f"{folder}/{fn_coil}",
                               casing_msh.nodes.node_coord,
                               casing_msh.elm.node_number_list - 1,
                               replace=False, hdf5_path='/mesh')
    pynibs.write_xdmf(f"{folder}/{fn_coil}", overwrite_xdmf=True)

    # write file with wiring information
    if isinstance(tms_coil.elements, list):
        wire_nodes = tms_coil.elements[0].points
        wire_data = tms_coil.elements[0].values
        coil_name = np.full((tms_coil.elements[0].points.shape[0]),
                            tms_coil.elements[0].name)
        stim_name = np.full((tms_coil.elements[0].points.shape[0]),
                            tms_coil.elements[0].stimulator.name)
        for idx in range(1, len(tms_coil.elements)):
            wire_nodes = np.vstack((wire_nodes, tms_coil.elements[idx].points))
            wire_data = np.vstack((wire_data, tms_coil.elements[idx].values))
            coil_name = np.concatenate((coil_name,
                                        np.full((tms_coil.elements[idx].points.shape[0]),
                                                tms_coil.elements[idx].name)))
            stim_name = np.concatenate((stim_name,
                                        np.full((tms_coil.elements[idx].points.shape[0]),
                                                tms_coil.elements[idx].stimulator.name)))


    else:
        wire_nodes = tms_coil.elements.points
        wire_data = tms_coil.elements.values
        coil_name = np.full((tms_coil.elements.points.shape[0]), tms_coil.elements.name)
        stim_name = np.full((tms_coil.elements.points.shape[0]), tms_coil.elements.stimulator.name)

    # Convert strings to their corresponding float values
    unique_strings = np.unique(coil_name)
    string_to_float_map = {string: i for i, string in enumerate(unique_strings)}
    coil_name = np.array([string_to_float_map[string] for string in coil_name])

    # Convert strings to their corresponding float values
    unique_strings = np.unique(stim_name)
    string_to_float_map = {string: i for i, string in enumerate(unique_strings)}
    stim_name = np.array([string_to_float_map[string] for string in stim_name])

    n_nodes = wire_nodes.shape[0]
    pynibs.write_arr_to_hdf5(f"{folder}/{fn_coil_wires}", arr_name='mesh/nodes/node_coord', data=wire_nodes)
    pynibs.write_arr_to_hdf5(f"{folder}/{fn_coil_wires}", arr_name='data/nodes/wire', data=wire_data)
    pynibs.write_arr_to_hdf5(f"{folder}/{fn_coil_wires}", arr_name='data/nodes/coil_name', data=coil_name)
    pynibs.write_arr_to_hdf5(f"{folder}/{fn_coil_wires}", arr_name='data/nodes/stim_name', data=stim_name)
    with open(f"{folder}/{fn_coil_wires.replace('.hdf5', '.xdmf')}", 'w') as f:
        f.writelines(f'<?xml version="1.0"?>\n')
        f.writelines(f'<!DOCTYPE Xdmf>\n')
        f.writelines(f'<Xdmf Version="2.0" xmlns:xi="http://www.w3.org/2001/XInclude">\n')
        f.writelines(f'<Domain>\n')
        f.writelines(f'<Grid CollectionType="Spatial" GridType="Collection" Name="Collection">\n')
        f.writelines(f'	<Grid Name="wire" GridType="Uniform">\n')
        f.writelines(f'		<Topology NumberOfElements="{n_nodes}" TopologyType="Polyvertex" Name="nodes"\n')
        f.writelines(f'                     NodesPerElement="1">\n')
        f.writelines(f'                     \n')
        f.writelines(f'		</Topology>\n')
        f.writelines(f'		<Geometry GeometryType="XYZ">\n')
        f.writelines(f'			<DataItem Format="HDF" Dimensions="{n_nodes} 3">\n')
        f.writelines(f'			{fn_coil_wires}:/mesh/nodes/node_coord\n')
        f.writelines(f'			</DataItem>\n')
        f.writelines(f'		</Geometry>\n')
        f.writelines(f'\n')
        f.writelines(f'		\n')
        f.writelines(f'		<Attribute Name="data" AttributeType="Vector" Center="Node">\n')
        f.writelines(f'			<DataItem Format="HDF" Dimensions="{n_nodes} 3">\n')
        f.writelines(f'				{fn_coil_wires}:/data/nodes/wire\n')
        f.writelines(f'        	</DataItem>\n')
        f.writelines(f'        </Attribute>\n')
        f.writelines(f'		<Attribute Name="coil_id" AttributeType="Scalar" Center="Node">\n')
        f.writelines(f'			<DataItem Format="HDF" Dimensions="{n_nodes}">\n')
        f.writelines(f'				{fn_coil_wires}:/data/nodes/coil_name\n')
        f.writelines(f'        	</DataItem>\n')
        f.writelines(f'        </Attribute>\n')
        f.writelines(f'		<Attribute Name="stim_id" AttributeType="Scalar" Center="Node">\n')
        f.writelines(f'			<DataItem Format="HDF" Dimensions="{n_nodes}">\n')
        f.writelines(f'				{fn_coil_wires}:/data/nodes/stim_name\n')
        f.writelines(f'        	</DataItem>\n')
        f.writelines(f'        </Attribute>\n')
        f.writelines(f'	</Grid>\n')
        f.writelines(f'\n')
        f.writelines(f'</Grid>\n')
        f.writelines(f'</Domain>\n')
        f.writelines(f'</Xdmf>')
