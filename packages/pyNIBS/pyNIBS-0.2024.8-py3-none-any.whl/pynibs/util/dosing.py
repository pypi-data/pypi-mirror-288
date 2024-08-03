"""
Functions used in our perspective on e-field based TMS dosing[1]_

References
----------
.. [1] Numssen, O., Kuhnke, P., Weise, K., & Hartwigsen, G. (2024).
   Electric-field-based dosing for TMS. Imaging Neuroscience, 2, 1-12.
   DOI: 10.1162/imag_a_00106
"""
import os
import h5py
import numpy as np
import pynibs


def get_intensity_e(e1, e2, target1, target2, radius1, radius2, headmesh,
                    rmt=1, roi='midlayer_lh_rh', verbose=False):
    """
    Computes the stimulator intensity adjustment factor based on the electric field.

    Parameters
    ----------
    e1 : str
        .hdf5 e field with midlayer.
    e2 : str
        .hdf5 e field with midlayer.
    target1 : np.ndarray (3,)
        Coordinates of cortical site of MT.
    target2 : np.ndarray (3,)
        Coordinates of cortical target site.
    radius1 : float
        Electric field of field1 is averaged over elements inside this radius around target1.
    radius2 : float
        Electric field of field2 is averaged over elements inside this radius around target2.
    headmesh : str
        .hdf5 headmesh.
    rmt : float, default: 1
        Resting motor threshold to be corrected.
    roi : str, default: 'midlayer_lh_rh'
        Name of roi. Expected to sit in ``mesh['/data/midlayer/roi_surface/']``.
    verbose : bool, default: False
        Flag indicating verbosity.

    Returns
    -------
    rmt_e_corr : float
        Adjusted stimulation intensity for target2.
    """

    with h5py.File(headmesh, 'r') as f:
        tris = f[f'/roi_surface/{roi}/tri_center_coord_mid'][:]

    idx, e_avg_target, e_target, t_idx_sphere = [], [], [], []
    for field, target, radius in zip([e1, e2], [target1, target2], [radius1, radius2]):
        idx.append(np.argmin(np.linalg.norm(tris - target, axis=1)))
        t_idx_sphere.append(np.where(np.linalg.norm(tris - tris[idx[-1]], axis=1) < radius)[0])
        with h5py.File(field, 'r') as e:
            e_avg_target.append(np.mean(e[f'/data/midlayer/roi_surface/{roi}/E_mag'][t_idx_sphere[-1]]))
            e_target.append(e[f'/data/midlayer/roi_surface/{roi}/E_mag'][idx[-1]])

    # determine scaling factor
    e_fac_avg = e_avg_target[0] / e_avg_target[1]
    e_fac = e_target[0] / e_target[1]
    rmt_e_corr = rmt * e_fac_avg

    if verbose:
        print(f"Target1: {target1}->{tris[idx[0]]}. E: {e_target[0]:2.4f}, {len(t_idx_sphere[0])} elms")
        print(f"Target2: {target2}->{tris[idx[1]]}. E: {e_target[1]:2.4f}, {len(t_idx_sphere[0])} elms")
        print(f"Efield normalization factor: {e_fac_avg:2.4f} ({e_fac:2.4f} for single elm).")
        # print(f"Center: {target} { tris_center[t_idx, ]}.")
        print(f"Given intensity {rmt}% is normalized to {rmt * e_fac_avg:2.4f}%.")

    return rmt_e_corr


def get_intensity_e_old(mesh1, mesh2, target1, target2, radius1, radius2, rmt=1, verbose=False):
    """
    Computes the stimulator intensity adjustment factor based on the electric field.
    Something weird is going on here - check simnibs coordinates of midlayer before usage.

    Parameters
    ----------
    mesh1 : str or simnibs.msh.mesh_io.Msh
        Midlayer mesh containing results of the optimal coil position of MT in the midlayer
        (e.g.: .../subject_overlays/00001.hd_fixed_TMS_1-0001_MagVenture_MCF_B65_REF_highres.ccd_scalar_central.msh)
    mesh2 : str or simnibs.msh.mesh_io.Msh
        Midlayer mesh containing results of the optimal coil position of the target in the midlayer
        (e.g.: .../subject_overlays/00001.hd_fixed_TMS_1-0001_MagVenture_MCF_B65_REF_highres.ccd_scalar_central.msh)
    target1 : np.ndarray
        (3,) Coordinates of cortical site of MT.
    target2 : np.ndarray
        (3,) Coordinates of cortical target site.
    radius1 : float
        Electric field in target 1 is averaged over elements inside this radius.
    radius2 : float
        Electric field in target 2 is averaged over elements inside this radius.
    rmt : float, default: 1
        Resting motor threshold, which will be corrected.
    verbose : bool, default: False
        Flag indicating verbosity.

    Returns
    -------
    rmt_e_corr : float
        Adjusted stimulation intensity for target2.
    """
    from simnibs.msh.mesh_io import read_msh

    # load mesh1 (MT) if filename is provided
    if isinstance(mesh1, str):
        if os.path.splitext(mesh1)[1] == ".msh":
            mesh1 = read_msh(mesh1)
        elif os.path.splitext(mesh1)[1] == ".hdf5":
            mesh1 = pynibs.load_mesh_hdf5(mesh1)

    # load mesh2 (target) if filename is provided
    if isinstance(mesh2, str):
        if os.path.splitext(mesh2)[1] == ".msh":
            mesh2 = read_msh(mesh2)
        elif os.path.splitext(mesh2)[1] == ".hdf5":
            mesh2 = pynibs.load_mesh_hdf5(mesh2)

    # load electric fields in midlayer and average electric field around sphere in targets
    e_avg_target = []
    for mesh, target, radius in zip([mesh1, mesh2], [target1, target2], [radius1, radius2]):
        nodes = mesh.nodes.node_coord
        tris = mesh.elm.node_number_list[:, :-1] - 1
        tris_center = np.mean(nodes[tris,], axis=1)

        e_norm_nodes = None
        for nodedata in mesh.nodedata:
            if nodedata.field_name == "E_norm":
                e_norm_nodes = nodedata.value

        e_norm_tris = np.mean(e_norm_nodes[tris], axis=1)

        # project targets to midlayer
        t_idx = np.argmin(np.linalg.norm(tris_center - target, axis=1))

        # get indices of surrounding elements in some radius
        t_idx_sphere = np.where(np.linalg.norm(tris_center - tris_center[t_idx,], axis=1) < radius)[0]

        # average e-field in this area
        e_avg_target.append(np.mean(e_norm_tris[t_idx_sphere]))

        print(f"Center: {target} {tris_center[t_idx,]}.")

    # determine scaling factor
    e_fac = e_avg_target[0] / e_avg_target[1]
    rmt_e_corr = rmt * e_fac

    if verbose:
        print(f"Efield normalized factor is: {e_fac:2.4f}.")
        # print(f"Center: {target} { tris_center[t_idx, ]}.")
        print(f"Given stimulatior intensity {rmt}% is normalized to new intensity {rmt * e_fac:2.4f}%.")

    return rmt_e_corr


def get_intensity_stokes(mesh, target1, target2, spat_grad=3, rmt=0, scalp_tag=1005, roi=None, verbose=False):
    """
    Computes the stimulator intensity adjustment factor according to Stokes et al. 2005
    (doi:10.1152/jn.00067.2005).
    Adjustment is based on target-scalp distance differences:
    adj = (Dist2-Dist1)*spat_grad

    Parameters
    ----------
    mesh : str or simnibs.msh.mesh_io.Msh
        Mesh of the head model.
    target1 : np.ndarray
        (3,) Coordinates of cortical site of MT.
    target2 : np.ndarray
        (3,) Coordinates of cortical target site.
    spat_grad : float, default: 3
        Spatial gradient.
    rmt : float, default: 0
        Resting motor threshold, which will be corrected.
    scalp_tag: int, default: 1005
        Tag in the mesh where the scalp is to be set.
    roi: np.ndarray, optional
        (3,N) Array of nodes to project targets onto.
    verbose : bool, default: False
        Print verbosity information.

    Returns
    -------
    rmt_stokes : float
        Adjusted stimulation intensity for target2.
    """
    from simnibs.msh.mesh_io import read_msh
    from pynibs.mesh import project_on_scalp

    # load mesh if filename is provided
    if isinstance(mesh, str):
        if os.path.splitext(mesh)[1] == ".msh":
            mesh = read_msh(mesh)
        elif os.path.splitext(mesh)[1] == ".hdf5":
            mesh = pynibs.load_mesh_hdf5(mesh)

    t1_proj = project_on_scalp(target1, mesh, scalp_tag=scalp_tag)
    t2_proj = project_on_scalp(target2, mesh, scalp_tag=scalp_tag)

    if roi is not None:
        t1_idx = np.argmin(np.linalg.norm(roi - target1, axis=1))
        t2_idx = np.argmin(np.linalg.norm(roi - target2, axis=1))
        t1_on_roi = roi[t1_idx]
        t2_on_roi = roi[t2_idx]

        if verbose:
            print("Projecting targets on ROI:\n"
                  "T1: [{0:+06.2f}, {1:+06.2f}, {2:+06.2f}] -> [{3:+06.2f}, {4:+06.2f}, {5:+06.2f}] Dist: {6:05.2f}mm"
                  "\n".format(*target1, *t1_on_roi, np.linalg.norm(target1 - t1_on_roi)) + \
                  "T2: [{0:+06.2f}, {1:+06.2f}, {2:+06.2f}] -> [{3:+06.2f}, {4:+06.2f}, {5:+06.2f}] Dist: {6:05.2f}mm"
                  "".format(*target2, *t2_on_roi, np.linalg.norm(target2 - t2_on_roi)))
        target1 = t1_on_roi
        target2 = t2_on_roi

    t1_dist = np.linalg.norm(target1 - t1_proj)
    t2_dist = np.linalg.norm(target2 - t2_proj)

    stokes_factor = (t2_dist - t1_dist) * spat_grad
    rmt_stokes = rmt + stokes_factor

    if verbose:
        print("Target 1: [{0:+06.2f}, {1:+06.2f}, {2:+06.2f}] ->"
              " [{3:+06.2f}, {4:+06.2f}, {5:+06.2f}] Dist: {6:05.2f}mm ".format(*target1, *t1_proj.flatten(), t1_dist))
        print("Target 2: [{0:+06.2f}, {1:+06.2f}, {2:+06.2f}] ->"
              " [{3:+06.2f}, {4:+06.2f}, {5:+06.2f}] Dist: {6:05.2f}mm ".format(*target2, *t2_proj.flatten(), t2_dist))
        print(f"Dist1 - Dist2: {t1_dist - t2_dist:05.2f} mm")
        print(f"rMT Stokes corrected: {rmt_stokes:05.2f} %MSO")

    return rmt_stokes
