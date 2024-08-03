import numpy as np
import gdist
from matplotlib import pyplot as plt
from scipy.spatial.transform import Rotation as rot

import pynibs


def geodesic_dist(nodes, tris, source, source_is_node=True):
    """
    Returns geodesic distance in mm from all nodes to source node (or triangle).
    This is just a wrapper for the gdist package.

    Example
    -------

    .. code-block:: python

        with h5py.File(fn,'r') as f:
            tris = f['/mesh/elm/triangle_number_list'][:]
            nodes = f['/mesh/nodes/node_coord'][:]
        nodes_dist_ged, tris_dist_ged = geodesic_dist(nodes, tris, 3017)

        pynibs.write_data_hdf5(data_fn,
                            data=[tris_dist_ged, nodes_dist_ged],
                            data_names=["tris_dist_ged", "nodes_dist_ged"])
        pynibs.write_xdmf(data_fn,hdf5_geo_fn=fn)

    Parameters
    ----------
    nodes : np.ndarray
        (n_nodes,3) The nodes, determined by their x-y-z-coordinates.
    tris : np.ndarray
        (n_tris,3) Every triangle, determined by the node indices (vertices) that form it.
    source : np.ndarray(int) or int
        Geodesic distances of all nodes (or triangles) to this one will be computed.
    source_is_node : bool
        Whether source is a node idx or a triangle idx.

    Returns
    -------
    nodes_dist : np.ndarray
        (n_nodes,) Geodesic distance between source and all nodes in mm.
    tris_dist : np.ndarray
        (n_tris,) Geodesic distance between source and all triangles in mm.
    """
    if source_is_node:
        if type(source) is not np.ndarray:
            source = np.array([source])
        nodes_dist = gdist.compute_gdist(nodes.astype(np.float64),
                                         tris.astype(np.int32),
                                         source_indices=source.astype(np.int32))

    else:
        nodes = nodes.astype(np.float64)
        tris = tris.astype(np.int32)
        source = tris[source].astype(np.int32)
        nodes_dist = gdist.compute_gdist(nodes,
                                         tris,
                                         source_indices=source)
        # l = []
        # for n in source:
        #     l.append(np.mean(gdist.compute_gdist(nodes,
        #                                  tris,
        #                                  source_indices=np.array([n]).astype(np.int32))[tris],axis=1))
        # # a = np.array(l)
        # nodes_dist = np.mean(l,axis=0)
        # a.shape
    tris_dist = np.mean(nodes_dist[tris], axis=1)

    return nodes_dist, tris_dist


def euclidean_dist(nodes, tris, source, source_is_node=True):
    """
    Returns euclidean distance of all nodes to source node (triangle).
    This is just a wrapper for the gdist package.

    Example
    -------
    .. code-block:: python

        with h5py.File(fn,'r') as f:
            tris = f['/mesh/elm/triangle_number_list'][:]
            nodes = f['/mesh/nodes/node_coord'][:]
        nodes_dist_euc, tris_dist_euc = euclidean_dist(nodes, tris, 3017)

        pynibs.write_data_hdf5(data_fn,
                            data=[tris_dist_euc, nodes_dist_euc],
                            data_names=["tris_dist_euc", "nodes_dist_euc", "])
        pynibs.write_xdmf(data_fn,hdf5_geo_fn=fn)

    Parameters
    ----------
    nodes : np.ndarray
        (n_nodes,3) The nodes, determined by their x-y-z-coordinates.
    tris : np.ndarray
        (n_tris,3) Every triangle, determined by the node indices (vertices) that form it.
    source : np.ndarray(int) or int
        Euclidean distances of all nodes (or triangles) to this one will be computed.
    source_is_node : bool
        Whether source is a node idx or a triangle idx.

    Returns
    -------
    nodes_dist : np.ndarray
        (n_nodes,) Geodesic distance between source and all nodes in mm.
    tris_dist : np.ndarray
        (n_tris,) Geodesic distance between source and all triangles in mm.
    """
    if source_is_node:
        nodes_dist = np.linalg.norm(nodes - nodes[source], axis=1)
    else:
        nodes_dist = np.zeros(nodes.shape[0], )
        for node in nodes[tris[source]]:
            nodes_dist += np.linalg.norm(nodes - node, axis=1)
        nodes_dist /= 3
    tris_dist = np.mean(nodes_dist[tris], axis=1)

    return nodes_dist, tris_dist


def nrmsd(array, array_ref, error_norm="relative", x_axis=False):
    """
    Determine the normalized root-mean-square deviation between input data and reference data.

    Notes
    -----
    nrmsd = np.sqrt(1.0 / n_points * np.sum((data - data_ref) ** 2)) / (max(array_ref) - min(array_ref))

    Parameters
    ----------
    array : np.ndarray
        input data [ (x), y0, y1, y2 ... ].
    array_ref : np.ndarray
        reference data [ (x_ref), y0_ref, y1_ref, y2_ref ... ].
        if array_ref is 1D, all sizes have to match.
    error_norm : str, optional, default="relative"
        Decide if error is determined "relative" or "absolute".
    x_axis : bool, default: False
        If True, the first column of array and array_ref is interpreted as the x-axis, where the data points are
        evaluated. If False, the data points are assumed to be at the same location.

    Returns
    -------
    normalized_rms : np.ndarray of float
        ([array.shape[1]]) Normalized root-mean-square deviation between the columns of array and array_ref.
    """

    n_points = array.shape[0]

    if x_axis:
        # handle different array lengths
        if len(array_ref.shape) == 1:
            array_ref = array_ref[:, None]
        if len(array.shape) == 1:
            array = array[:, None]

        # determine number of input arrays
        if array_ref.shape[1] == 2:
            n_data = array.shape[1] - 1
        else:
            n_data = array.shape[1]

        # interpolate array on array_ref data if necessary
        if array_ref.shape[1] == 1:
            data = array
            data_ref = array_ref
        else:
            # crop reference if it is longer than the axis of the data
            data_ref = array_ref[(array_ref[:, 0] >= min(array[:, 0])) & (array_ref[:, 0] <= max(array[:, 0])), 1]
            array_ref = array_ref[(array_ref[:, 0] >= min(array[:, 0])) & (array_ref[:, 0] <= max(array[:, 0])), 0]

            data = np.zeros([len(array_ref), n_data])
            for i_data in range(n_data):
                data[:, i_data] = np.interp(array_ref, array[:, 0], array[:, i_data + 1])
    else:
        data_ref = array_ref
        data = array

    # determine "absolute" or "relative" error
    if error_norm == "relative":
        # max_min_idx = np.isclose(np.max(data_ref, axis=0), np.min(data_ref, axis=0))
        delta = np.max(data_ref, axis=0) - np.min(data_ref, axis=0)

        # if max_min_idx.any():
        #     delta[max_min_idx] = max(data_ref[max_min_idx])
    elif error_norm == 'absolute':
        delta = 1
    else:
        raise NotImplementedError

    # determine normalized rms deviation and return
    normalized_rms = np.sqrt(1.0 / n_points * np.sum((data - data_ref) ** 2, axis=0)) / delta

    return normalized_rms


def nrmse(array, array_ref, x_axis=False):
    """
    Determine the normalized root-mean-square deviation between input data and reference data.

    nrmse = np.linalg.norm(array - array_ref) / np.linalg.norm(array_ref)

    Parameters
    ----------
    array : np.ndarray
        input data [ (x), y0, y1, y2 ... ].
    array_ref : np.ndarray
        reference data [ (x_ref), y0_ref, y1_ref, y2_ref ... ].
        if array_ref is 1D, all sizes have to match.
    error_norm : str, optional, default="relative"
        Decide if error is determined "relative" or "absolute".
    x_axis : bool, default: False
        If True, the first column of array and array_ref is interpreted as the x-axis, where the data points are
        evaluated. If False, the data points are assumed to be at the same location.

    Returns
    -------
    nrmse: np.ndarray of float
        ([array.shape[1]]) Normalized root-mean-square deviation between the columns of array and array_ref.
    """

    n_points = array.shape[0]

    if x_axis:
        # handle different array lengths
        if len(array_ref.shape) == 1:
            array_ref = array_ref[:, None]
        if len(array.shape) == 1:
            array = array[:, None]

        # determine number of input arrays
        if array_ref.shape[1] == 2:
            n_data = array.shape[1] - 1
        else:
            n_data = array.shape[1]

        # interpolate array on array_ref data if necessary
        if array_ref.shape[1] == 1:
            data = array
            data_ref = array_ref
        else:
            # crop reference if it is longer than the axis of the data
            data_ref = array_ref[(array_ref[:, 0] >= min(array[:, 0])) & (array_ref[:, 0] <= max(array[:, 0])), 1]
            array_ref = array_ref[(array_ref[:, 0] >= min(array[:, 0])) & (array_ref[:, 0] <= max(array[:, 0])), 0]

            data = np.zeros([len(array_ref), n_data])
            for i_data in range(n_data):
                data[:, i_data] = np.interp(array_ref, array[:, 0], array[:, i_data + 1])
    else:
        data_ref = array_ref
        data = array

    # determine normalized rms deviation and return
    nrmse = np.linalg.norm(data - data_ref, axis=0) / np.linalg.norm(data_ref, axis=0)

    return nrmse


def c_map_comparison(c1, c2, t1, t2, nodes, tris):
    """
    Compares two c-maps in terms of NRMSD and calculates the geodesic distance between the hotspots.

    Parameters
    ----------
    c1 : np.ndarray of float
        (n_ele) First c-map.
    c2 : np.ndarray of float
        (n_ele) Second c-map (reference).
    t1 : np.ndarray of float
        (3) Coordinates of the hotspot in the first c-map.
    t2 : np.ndarray of float
        Coordinates of the hotspot in the second c-map.
    nodes : np.ndarray of float
        (n_nodes, 3) Node coordinates
    tris : np.ndarray of float
        (n_tris, 3) Connectivity of ROI elements

    Returns
    -------
    nrmsd : float
        Normalized root-mean-square deviation between the two c-maps in (%).
    gdist : float
        Geodesic distance between the two hotspots in (mm).
    """
    # determine NRMSD between two c-maps
    nrmsd_ = nrmsd(array=c1, array_ref=c2, error_norm="relative", x_axis=False) * 100

    # determine geodesic distance between hotspots
    tris_center = np.mean(nodes[tris,], axis=1)

    t1_idx = np.argmin(np.linalg.norm(tris_center - t1, axis=1))
    t2_idx = np.argmin(np.linalg.norm(tris_center - t2, axis=1))
    gdists = geodesic_dist(nodes=nodes, tris=tris, source=t2_idx, source_is_node=False)[1]
    gdist_ = gdists[t1_idx]

    return nrmsd_, gdist_


def calc_tms_motion_params(coil_positions, reference=None):
    """
    Computes motion parameters for a set of ``coil_positions``, i.e., coil shifts in [mm] in RAS coordinate system and
    rotations (pitch, roll, yaw) in [°].
    Motion is computed w.r.t. the first ('absolute') and to the previous ('relative') stimulation.

    Position shifts are quantified with respect to the subject/nifti-specific RAS coordinate system.
    Rorational changes are quantified with respect to the coil axes as follows:

        * pitch: rotation around left/right axis of coil
        * roll: rotation around coil handle axis
        * yaw: rotation around axis from center of coil towards head
    Motion parameters for first coil position are set to 0.

    Parameters
    ----------
    coil_positions : np.ndarray of float
        (4, 4, n_pulses).
    reference : np.ndarray of float, optional
        (4, 4) Reference coil placement. If None (default), the first placement from ``coil_positions`` is used.

    Returns
    -------
    pos_diff_abs : np.ndarray
        (3, n_pulses) Absolute position differences (R, A, S).
    euler_rots_abs : np.ndarray
        (3, n_pulses) Absolute rotation angles in euler angles (alpha, beta, gamma).
    pos_diff_rel : np.ndarray
        (3, n_pulses) Relative position differences (R, A, S).
    euler_rots_rel : np.ndarray
        (3, n_pulses) Relative rotation angles in euler angles (alpha, beta, gamma).
    """
    np.set_printoptions(suppress=True)
    if reference is None:
        i_ref = 0
        while np.isnan(coil_positions[:, :, i_ref]).any():
            i_ref += 1
        reference_pos = coil_positions[0:3, 3, i_ref].T
        reference_rot = coil_positions[0:3, 0:3, i_ref]

        # first rotation is zero because it is the reference
        euler_rots_abs = [[0, 0, 0]]
    else:
        reference = np.squeeze(reference)
        reference_pos = reference[0:3, 3].T
        reference_rot = reference[0:3, 0:3]

        # compute first rotation towards reference
        rotmat_abs = pynibs.bases2rotmat(reference_rot, coil_positions[0:3, 0:3, 0])
        if np.isnan(rotmat_abs).any():
            euler_rots_abs = [[np.nan, np.nan, np.nan]]
        else:
            euler_rots_abs = [rot.from_matrix(rotmat_abs).as_euler('xyz', degrees=True).tolist()]

    # compute absolute and relative position differences
    pos_diff_abs = (reference_pos - coil_positions[0:3, 3, :].T).T
    pos_diff_rel = np.diff(coil_positions[0:3, 3, :], 1, axis=1, prepend=coil_positions[0:3, 3, 0, np.newaxis])

    # bring position differences into reference coordinate system
    pos_diff_abs_rot = reference_rot.T @ pos_diff_abs
    pos_diff_rel_rot = reference_rot.T @ pos_diff_rel

    n_coilpos = coil_positions.shape[2]
    euler_rots_rel = [[0, 0, 0]]
    for i in range(0, n_coilpos - 1):
        rotmat_abs = pynibs.bases2rotmat(reference_rot, coil_positions[0:3, 0:3, i + 1])
        if np.isnan(rotmat_abs).any():
            euler_abs = [np.nan, np.nan, np.nan]
        else:
            euler_abs = rot.from_matrix(rotmat_abs).as_euler('xyz', degrees=True).tolist()
        euler_rots_abs.append(euler_abs)

        rotmat_rel = pynibs.bases2rotmat(coil_positions[0:3, 0:3, i], coil_positions[0:3, 0:3, i + 1])
        if np.isnan(rotmat_rel).any():
            euler_rel = [np.nan, np.nan, np.nan]
        else:
            euler_rel = rot.from_matrix(rotmat_rel).as_euler('xyz', degrees=True).tolist()
        euler_rots_rel.append(euler_rel)

    euler_rots_rel = np.array(euler_rots_rel)
    euler_rots_abs = np.array(euler_rots_abs)

    return pos_diff_abs_rot, euler_rots_abs.T, pos_diff_rel_rot, euler_rots_rel.T


def plot_tms_motion_parameter(pos_diff, euler_rots, pcd=None, fname=None):
    """
    Plots TMS coil motion parameters.

    .. figure:: ../../doc/images/pcd.png
       :scale: 80 %
       :alt: TMS motion parameters and PCD

       Pulsewise Coil Displacement (PCD) is a compound metric to quantify TMS coil movements. Data for a double (space)
       cTBS400 protocol is shown (with a break after 200 bursts).

    Parameters
    ----------
    pos_diff : np.ndarray
        (3, n_pulses) Position differences (R, A, S).
    euler_rots : np.ndarray
        (3, n_pulses) Rotation angles in euler angles (alpha, beta, gamma).
    pcd : np.ndarray, optional
        (n_pulses,) pulsewise coil displacements.
    fname : str, optional
        Filename to save plot.

    Returns
    -------
    axes : matplotlib.pyplot.axes
        Figure axes.
    """
    if pcd is not None:
        n_plot_rows = 3
    else:
        n_plot_rows = 2
    n_coilpos = pos_diff.shape[1]
    fig, axes = plt.subplots(n_plot_rows, 2)

    fig.suptitle('TMS coil displacement')

    # let's order the plotting based on the data to have the dimension with the fewest changes on top
    order_pos = np.argsort(np.std(pos_diff, axis=1))[::-1]
    order_rot = np.argsort(np.std(euler_rots, axis=1))[::-1]
    colors_pos = ['#12263A', '#50858B', '#99EDCC']
    colors_rot = ['#725752', '#F2A541', '#F8DF8C']
    labels_pos = ['X', 'Y', 'Z']
    labels_rot = ['yaw', 'pitch', 'roll']

    for i in order_pos:
        axes[0, 0].plot(range(0, n_coilpos), pos_diff[i, :], c=colors_pos[i], label=labels_pos[i], linewidth=1)
        axes[0, 1].plot(range(0, n_coilpos), np.nancumsum(pos_diff[i, :]), c=colors_pos[i], label=labels_pos[i],
                        linewidth=1)
    for i in order_rot:
        axes[1, 0].plot(range(0, n_coilpos), euler_rots[i, :], c=colors_rot[i], label=labels_rot[i], linewidth=1)
        axes[1, 1].plot(range(0, n_coilpos), np.nancumsum(euler_rots[i, :]), c=colors_rot[i], label=labels_rot[i],
                        linewidth=1)
    np.set_printoptions(suppress=True)
    axes[0, 0].set_title('Relative movement [mm]')
    axes[1, 0].set_title('Relative rotation [°]')
    axes[0, 1].set_title('Cumulative movement [mm]')
    axes[1, 1].set_title('Cumulative rotation [°]')
    fig.delaxes(axes[2, 1])
    if pcd is not None:
        axes[2, 0].plot(range(0, n_coilpos), pcd, c='#843E84', label='PCD',
                        linewidth=1)
        axes[2, 0].set_title('Pulsewise coil displacement [AU]')

        # add some stats to plot
        plt.figtext(0.505, 0.09, f"       PCD\n"
                                 f"   Max: {np.nanmax(pcd).round(2):6.2f}\n"
                                 f"  Mean: {np.nanmean(pcd).round(2):6.2f}\n"
                                 f"Median: {np.nanmedian(pcd).round(2):6.2f}\n"
                                 f"    SD: {np.nanstd(pcd).round(2):6.2f}\n"
                                 f"n stim: {(~np.isnan(pcd)).sum(): >6}\n"
                                 f"untracked: {(np.isnan(pcd)).sum(): >3}",
                    family='monospace'
                    )

    fig.tight_layout()
    handles_tmp, labels_tmp = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles_tmp, labels_tmp, ncols=1, loc=[0.7, 0.08], title='Shift')

    handles_tmp, labels_tmp = axes[1, 0].get_legend_handles_labels()
    fig.legend(handles_tmp, labels_tmp, ncols=1, loc=[0.83, 0.08], title='Rotation')

    # handles_tmp, labels_tmp = axes[2, 0].get_legend_handles_labels()
    # fig.legend(handles_tmp, labels_tmp, ncols=1, loc=[0.85, 0.12], title='PCD')

    if fname is not None:
        plt.savefig(fname)

    return axes


def compute_pcd(delta_pos, delta_rot, skin_cortex_distance=20):
    """
    Computes _P_ulsewise _C_oil _D_isplacements (PCD) based on 3 position parameters (``delta_pos``) and
    3 rotation parmeters (``delta_rot``).

    The coil rotations (in euler angles) are transformed into a positional change projected on the cortex based on
    ``skin_cortex_distance`` as a proxy for the (local) change of the stimulation.
    ``delta_pos`` and ``delta_rot`` are expected to quantify motion w.r.t. the target coil position/roation, for example
    the absolute deltas to the first stimulation.

    Axes definitions
    ----------------
    ``delta_pos`` and ``delta_rot`` are supposed to follow this axes definition (SimNIBS):

    - delta_pos
        - X and Y: coil movement tangential to head surface
        - Z: coil movement perpendicular to head surface

    - delta_rot
        * pitch: rotation around left/right axis of coil
        * roll: rotation around coil handle axis
        * yaw: rotation around axis from center of coil towards head

    .. figure:: ../../doc/images/coil_axes_definition.png
       :scale: 80 %
       :alt: Coil axes definition, following SimNIBS conventions.


    Example
    -------
    .. code-block:: python

        # get TriggerMarkers from a Localite session
        mats = pynibs.read_triggermarker_localite(tm_fn)[0]

        # calculate absolute and relative coil displacements
        delta_pos_abs, delta_rot_abs, delta_pos_rel, delta_rot_rel = pynibs.calc_tms_motion_params(mats)

        # compute PCD
        pcd, delta_pos, delta_rot = pynibs.compute_pcd(delta_pos_abs, delta_rot_abs)

        # plot movement
        axes = pynibs.plot_tms_motion_parameter(pos_diff_rel, euler_rots_rel, pcd)
        matplotlib.pyplot.show()

    Parameters
    ----------
    delta_pos : np.ndarray
        (3, n_pulses) Absolute position differences (R, A, S).
    delta_rot : np.ndarray
        (3, n_pulses) Absolute rotation angles in euler angles (alpha, beta, gamma).
    skin_cortex_distance : int, default: 20
        Cortical depth of target to adjust coil rotations for.

    Returns
    -------
    pcd : np.ndarray
        Pulsewise coil displacements.
    delta_pos : np.ndarray
        (n_pulses, ) sum(abs(delta_pos)) per pulse.
    delta_rot : np.ndarray
        (n_pulses, ) sum(abs(delta_rot projected by skin_cortex_distance)) per pulse.
    """
    # delta_pos_summed = np.sum(np.abs(delta_pos[:2, :]), axis=0)
    delta_pos_summed = np.sqrt(np.sum(delta_pos[: 2, :] ** 2, axis=0))
    delta_pos_summed = np.squeeze(delta_pos_summed + delta_pos[2, :] ** 2 * np.sign(delta_pos[2, :]))

    plane_n = np.array([0, 0, 1])
    plane_p = np.array([0, 0, skin_cortex_distance])  # Any point on the plane

    # compute shift of the center of coil ray
    ray_origin = np.array([0, 0, 0])  # Any point along the ray
    delta_rot_a = []
    for idx, rots in enumerate(delta_rot.T):
        # apply x and y rotation to [0,0,1]
        # rots[2] = 0
        r = rot.from_rotvec(rots, degrees=True)
        ray_dir = r.apply([0, 0, 1])
        intersec = pynibs.intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p, eps=1e-6)

        # compute distance from new intersection with [0, 0, scd]
        delta_rot_a.append(np.linalg.norm(plane_p - intersec))

    # ray shift based on orientation doesn't include any rotations around z axis.
    z_rotation_deltas = np.abs((skin_cortex_distance) * np.sin(np.deg2rad(delta_rot[2, :])))
    delta_rot = np.array(delta_rot_a) + z_rotation_deltas
    return delta_pos_summed + delta_rot, delta_pos_summed, delta_rot
