""" Functions to import data from Localite TMS Navigator """
import os
import h5py
import warnings
import datetime
import numpy as np
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
from xml.etree import ElementTree as xmlt, ElementTree as ET

import pynibs


def get_tms_elements(xml_paths, verbose=False):
    """
    Read needed elements out of the tms-xml-file.

    Parameters
    ----------
    xml_paths : list of str or str
        Paths to coil0-file and optionally coil1-file. If there is no coil1-file, use empty string.
    verbose : bool, default: False
        Flag indicating verbosity.

    Returns
    -------
    coils_array : np.ndarray of float
         (3, NX4, 4),  Coil0, coil1 and mean-value of N 4x4 coil-arrays.
    ts_tms_lst : list of int
        [N] Timestamps of valid tms-measurements.
    current_lst : list of int
        [N]  Measured currents.
    idx_invalid : list of int
        List of indices of invalid coil positions (w.r.t. all timestamps incl invalid).
    """
    if isinstance(xml_paths, str):
        xml_paths = [xml_paths]
    # handle case if there is no coil1
    if len(xml_paths) > 1 and not xml_paths[1]:
        xml_paths[1] = xml_paths[0]
    if len(xml_paths) == 1:
        xml_paths.append(xml_paths[0])

    # allocate new array and lists
    coils_array, ts_tms_lst, current_lst = np.empty([3, 0, 4, 4]), [], []

    # parse XML document
    coil0_tree, coil1_tree = xmlt.parse(xml_paths[0]), xmlt.parse(xml_paths[1])
    coil0_root, coil1_root = coil0_tree.getroot(), coil1_tree.getroot()

    # iterate over all 'TriggerMarker' tags
    i_stim = 0
    idx_invalid = []

    for coil0_tm, coil1_tm in zip(coil0_root.iter('TriggerMarker'), coil1_root.iter('TriggerMarker')):
        coil_array = np.empty([0, 1, 4, 4])

        # get tag were the matrix is
        coil0_ma, coil1_ma = coil0_tm.find('Matrix4D'), coil1_tm.find('Matrix4D')

        # get coil0
        coil_array = np.append(coil_array, read_coil(coil0_ma), axis=0)

        # if present, get coil1
        if xml_paths[0] == xml_paths[1]:
            coil_array = np.append(coil_array, np.identity(4)[np.newaxis, np.newaxis, :, :], axis=0)
        else:
            coil_array = np.append(coil_array, read_coil(coil1_ma), axis=0)

        # check for not valid coils and calculate mean value
        if not np.allclose(coil_array[0, 0, :, :], np.identity(4)) and \
                not np.allclose(coil_array[1, 0, :, :], np.identity(4)):
            coil_array = np.append(coil_array,
                                   np.expand_dims((coil_array[0, :, :, :] + coil_array[1, :, :, :]) / 2, axis=0),
                                   axis=0)
        elif np.allclose(coil_array[0, 0, :, :], np.identity(4)) and not np.allclose(coil_array[1, 0, :, :],
                                                                                     np.identity(4)):
            coil_array = np.append(coil_array, np.expand_dims(coil_array[1, :, :, :], axis=0), axis=0)
        elif np.allclose(coil_array[1, 0, :, :], np.identity(4)) and not np.allclose(coil_array[0, 0, :, :],
                                                                                     np.identity(4)):
            coil_array = np.append(coil_array, np.expand_dims(coil_array[0, :, :, :], axis=0), axis=0)
        else:
            idx_invalid.append(i_stim)
            if verbose:
                print("Removing untracked (and possibly accidental) coil position #{} (identity matrix)".format(i_stim))
            i_stim += 1
            continue

        # print(i_stim)
        i_stim += 1

        coils_array = np.append(coils_array, coil_array, axis=1)

        # get timestamp
        ts_tms_lst.append(int(coil0_tm.get('recordingTime')))

        # get current
        xml_rv = coil0_tm.find('ResponseValues')
        xml_va = xml_rv.findall('Value')

        # if valueA is NaN, compute dI/dt with amplitudeA
        if xml_va[0].get('response') == 'NaN':
            current_lst.append(str(round(float(xml_va[2].get('response')) * 1.4461)))  # was 1.38
        else:
            current_lst.append(xml_va[0].get('response'))

    return [coils_array, ts_tms_lst, current_lst, idx_invalid]


def read_coil(xml_ma):
    """
    Read coil-data from xml element.

    Parameters
    ----------
    xml_ma : xml-element
        Coil data.

    Returns
    -------
    coil : np.ndarray of float
        (4, 4) Coil elements.
    """
    # index2 for all coils from triggermarker
    coil = np.empty([1, 1, 4, 4])
    for coil_index1 in range(4):
        for coil_index2 in range(4):
            coil[0, 0, coil_index1, coil_index2] = (float(xml_ma.get('data' + str(coil_index1) + str(coil_index2))))
    return coil


def match_instrument_marker_file(xml_paths, im_path):
    """
    Assign right instrument marker condition to every triggermarker (get instrument marker out of file).

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string.
    im_path : str
        Path to instrument-marker-file.

    Returns
    -------
    coil_cond_lst : list of str
        Right conditions.
    drop_idx : list of int
        Indices of trigger markers that were dropped.
    """
    tm_array, tms_time_arr, tms_cur_arr, tms_idx_invalid = get_tms_elements(xml_paths)
    # get coil mean value
    tm_array = tm_array[2]
    im_array, im_cond_lst = get_marker(im_path, markertype='InstrumentMarker')[:2]

    # get indices of conditions
    im_index_lst, drop_idx = match_tm_to_im(tm_array, im_array, tms_time_arr, tms_cur_arr)

    # list to save conditions
    coil_cond_lst = []

    for cond_index in im_index_lst:
        coil_cond_lst.append(im_cond_lst[cond_index])
    return coil_cond_lst, drop_idx


def match_instrument_marker_string(xml_paths, condition_order):
    """
    Assign right instrument marker condition to every triggermarker (get instrument marker out of list of strings).

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string.
    condition_order : list of str
        Conditions in the right order.

    Returns
    -------
    coil_cond_lst : list of str
        Strings containing the right conditions.
     drop_idx : list of int
        Indices of trigger markers that were dropped.
    """
    drop_idx = []
    max_time_dif = 90000
    max_mep_dif = 7

    tm_pos_arr, tms_time_arr, tms_cur_arr, tms_idx_invalid = get_tms_elements(xml_paths)

    # get coil mean value
    tm_pos_arr = tm_pos_arr[2, :, :, :]

    # list for condition results
    conditions = []

    # index of instrument marker
    cond_idx = 0

    # iterate over all trigger marker
    for tm_index in range((tm_pos_arr.shape[0]) - 1):
        conditions.append(condition_order[cond_idx])
        if float(tms_cur_arr[tm_index]) == 0.:
            drop_idx.append(tm_index)
        tm_matrix_post = tm_pos_arr[tm_index + 1, :, :]
        tm_matrix = tm_pos_arr[tm_index, :, :]

        same_tm = arrays_similar(tm_matrix, tm_matrix_post)
        time_dif = tms_time_arr[tm_index + 1] - tms_time_arr[tm_index] > max_time_dif
        amp_dif = np.abs(float(tms_cur_arr[tm_index + 1]) - float(tms_cur_arr[tm_index])) > max_mep_dif
        if not same_tm and time_dif and amp_dif:
            arrays_similar(tm_matrix, tm_matrix_post)
            cond_idx += 1
            if cond_idx == len(condition_order):
                raise ValueError("Too many coil conditions found!")

    # assign last element to very last element
    conditions.append(conditions[-1])
    if cond_idx != len(condition_order) - 1:
        raise ValueError("Did not find all coil positions!")

    return conditions, drop_idx


def arrays_similar(tm_matrix, tm_matrix_post,  # , tm_mean_last,
                   pos_rtol=0, pos_atol=3.6, ang_rtol=.1, ang_atol=.1):
    """
    Compares angles and position for similarity.

    Splitting the comparison into angles and position is advisable, as the absolute tolerance (atol) should be
    different for angles (degree) and position (millimeter) comparisons.

    Parameters
    ----------
    tm_matrix : array-like
        (4, 4) TMS Navigator trigger marker or instrument marker array.
    tm_matrix_post : array-like
        (4, 4) TMS Navigator trigger marker or instrument marker array.
    pos_rtol : float, default: 0
        Relative tolerance for position comparison.
    pos_atol : float, default: 3.6
        Absolute tolerance for position comparison in millimeters.
    ang_rtol : float, default: 0.1
        Relative tolerance for angle comparison in degrees.
    ang_atol : float, default: 0.1
        Absolute tolerance for angle comparison in degrees.
        
    Returns
    -------
    next_same : bool 
        True if the position and angle differences between `tm_matrix` and `tm_matrix_post`
        are within the specified tolerances, False otherwise.
    """
    # position
    pos = np.allclose(tm_matrix[0:3, 3], tm_matrix_post[0:3, 3], rtol=pos_rtol, atol=pos_atol)

    # angles
    ang = np.allclose(tm_matrix[0:3, 0:2], tm_matrix_post[0:3, 0:2], rtol=ang_rtol, atol=ang_atol)

    # if tm_mean_last is not None:
    #     last_pos = np.allclose(tm_matrix[0:3, 3], tm_mean_last[0:3, 3], rtol=pos_rtol, atol=pos_atol)
    #     last_ang = np.allclose(tm_matrix[0:3, 0:2], tm_mean_last[0:3, 0:2], rtol=ang_rtol, atol=ang_atol)

    next_same = pos and ang
    # last_same = last_pos and last_ang
    return next_same


def match_tm_to_im(tm_array, im_array, tms_time_arr, tms_cur_arr):
    """
    Match triggermarker with instrumentmarker and get index of best fitting instrumentmarker.

    Parameters
    ----------
    tm_array : np.ndarray of float
        (N, 4, 4) Mean-value of Nx4x4 coil matrices.
    im_array : np.ndarray of float
        (M, 4, 4) Instrument-marker-matrices.
    tms_time_arr : np.ndarray
        Array of TMS times in seconds.
    tms_cur_arr : np.ndarray
        Array of TMS currents corresponding to ```tms_time_arr```.

    Returns
    -------
    im_index_lst : list of int
        Indices of best fitting instrument markers.
    drop_idx : list of int
        Indices of trigger markers that were dropped.
    """
    max_time_dif = (tms_time_arr[1] - tms_time_arr[0]) * 3
    # max_mep_dif = 9

    im_index_lst = []
    drop_idx = []

    for tm_index in range(tm_array.shape[0]):
        # after first zap, check time diff
        if tm_index > 0:
            if tms_time_arr[tm_index] - tms_time_arr[tm_index - 1] < max_time_dif:
                im_index_lst.append(im_index_lst[-1])
                continue

        allclose_index_lst = []
        diff_small = []

        atol_ori = 0.4
        atol_pos = 3
        repeat = False

        # tm = tm_array[tm_index, :, :]

        # proc_diffs = np.argmin[procrustes(tm, im_array[i])[2] for i in range(im_array.shape[0])]

        # diffs = np.abs(tm - im_array)
        # diffs[0:3, 0:3] /= np.max(diffs[:, 0:3, 0:4], axis=0)
        # best_fit = np.argmin(np.array([np.sum(diffs[i]) for i in range(len(diffs))]))
        # small_diff_ori = int(np.argmin(np.array([np.sum(diffs[i][0:3, 0:3]) for i in range(len(diffs))])))
        # small_diff_pos = int(np.argmin(np.array([np.sum(diffs[i][0:3, 3]) for i in range(len(diffs))])))
        # a = rot_to_quat(tm[:3,:3])[1:]
        # b = [quaternion_diff(a, rot_to_quat(im_array[i, :3, :3])[1:]) for i in range(im_array.shape[0])]

        while not allclose_index_lst:
            if repeat:
                print(('Warning: Trigger marker #{:0>4}: No matching instrument marker within '
                       'atol_ori={} and atol_pos={}! Increasing tolerances by 0.1 and 0.5.'
                       .format(tm_index, atol_ori, atol_pos)))

                atol_ori = atol_ori + 0.1
                atol_pos = atol_pos + 0.5

            for im_index in range(im_array.shape[0]):

                # # check if arrays are close
                # if np.allclose(tm_array[tm_index, :, :], im_array[im_index, :, :], rtol=rtol):
                #     allclose_index_lst.append(im_index)

                # check if arrays are close
                diff = np.abs(tm_array[tm_index, :, :] - im_array[im_index, :, :])

                if (diff[0:3, 0:3] < atol_ori).all() and (diff[0:3, 3] < atol_pos).all():
                    diff_small.append(diff)
                    allclose_index_lst.append(im_index)

            if not allclose_index_lst:
                allclose_index_lst.append(-1)
                # repeat = True

        # if multiple arrays are close, choose value, with the smallest difference
        if len(allclose_index_lst) > 1:
            smallest_value_index = int(np.argmin(np.array([np.sum(diff_small[i]) for i in range(len(diff_small))])))
            small_diff_ori = int(np.argmin(np.array([np.sum(diff_small[i][0:3, 0:3]) for i in range(len(diff_small))])))
            small_diff_pos = int(np.argmin(np.array([np.sum(diff_small[i][0:3, 3]) for i in range(len(diff_small))])))
            if not small_diff_ori == small_diff_pos:
                #     print allclose_index_lst
                print("Warning: Triggermarker #{:0>4}: "
                      "Cannot decide for instrument marker , dropping this one. ".format(tm_index))
                drop_idx.append(tm_index)
            # im_index_lst.append(im_index_lst[-1])
            # else:
            # assert best_fit == allclose_index_lst[smallest_value_index]
            im_index_lst.append(allclose_index_lst[smallest_value_index])

        else:
            # assert best_fit == allclose_index_lst[0]
            im_index_lst.append(allclose_index_lst[0])

            # # if multile arrays are close, choose value,
            # where the difference to the instrument marker has the smallest
            # # frobenius norm
            # if len(allclose_index_lst) > 1:
            #     smallest_value_index = int(np.argmin(np.linalg.norm(im_array[allclose_index_lst, :, :] -
            #                                                         tm_array[tm_index, :, :], axis=(1, 2))))
            #     im_index_lst.append(allclose_index_lst[smallest_value_index])
            # else:
            #     im_index_lst.append(allclose_index_lst[0])

    return im_index_lst, drop_idx


def get_marker(im_path, markertype):
    """
    Read instrument-marker and conditions from Neuronavigator .xml-file.

    Coil axes definition as defined by Localite.

    Parameters
    ----------
    im_path : str or list of str
        Path to instrument-marker-file.
    markertype : str
        One of ['TriggerMarker','InstrumentMarker'].

    Returns
    -------
    im_array : np.ndarray of float
        (M, 4, 4) Instrument marker matrices.
    marker_descriptions : list of str
        Labels of the marker conditions.
    marker_times : list of float
        Onset times.
    """
    assert markertype in ['TriggerMarker', 'InstrumentMarker']
    if isinstance(im_path, str):
        return get_single_marker_file(im_path, markertype)

    elif isinstance(im_path, list):
        # if multiple triggermarker files are provided, pick a marker with data
        matsimnibs, marker_descriptions, marker_times = [], [], []

        # get data from all files
        for im in im_path:
            im_array_t, marker_descriptions_t, marker_times_t = get_single_marker_file(im, markertype)
            matsimnibs.append(im_array_t)
            marker_descriptions.append(marker_descriptions_t)
            marker_times.append(marker_times_t)

        # get indices for all files where markers are empty
        # empty_arr = []
        # for arr in im_array:  # arr = im_array[0]
        #     empty_arr.append(markers_are_empty(arr))
        # # assert np.all(np.sum(np.array(empty_arr).astype(int), axis=0) == 1)
        #
        # # go through the zaps and pick a marker with data.
        # idx = []
        # tmp = 0
        # for i in range(len(im_array[0])):
        #     for j in range(len(im_array)):
        #         if not empty_arr[j][i]:
        #             tmp = j
        #         # if all are empty, just use the last value (is empty anyway)
        #     idx.append(tmp)  # append
        #
        # # build marker idx based on idx
        # final_arr = []
        # for it, i in enumerate(idx):
        #     final_arr.append(im_array[i][it])
        return np.array(matsimnibs), marker_descriptions, marker_times
    else:
        raise NotImplementedError(f"type {type(im_path)} not implemented.")


def markers_are_empty(arr):
    return [marker_is_empty(arr[i, :, :]) for i in range(arr.shape[0])]


def marker_is_empty(arr):
    return np.all(arr == np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]]))


def get_single_marker_file(im_path, markertype):
    """
    Read instrument-marker and conditions from Neuronavigator .xml-file.

    Parameters
    ----------
    im_path : str or list of str
        Path to instrument-marker-file.
    markertype : str
        One of ['TriggerMarker','InstrumentMarker'].

    Returns
    -------
    im_array : np.ndarray of float
        (M, 4, 4) Instrument marker matrices.
    marker_descriptions : list of str
        Labels of the marker conditions.
    marker_times : list of float
        Onset times.
    """
    im_array = np.empty([0, 4, 4])
    marker_descriptions = []
    marker_times = []
    # parse XML document
    im_tree = xmlt.parse(im_path)
    im_root = im_tree.getroot()

    # iterate over all 'InstrumentMarker' tags
    for marker_i in im_root.iter(markertype):
        marker_array = np.empty([1, 4, 4])
        # get tag were the matrix is
        if markertype == 'InstrumentMarker':
            marker_object = marker_i.find('Marker')
            marker_descriptions.append(marker_object.get('description'))
            matrix4d = marker_object.find('Matrix4D')

        elif markertype == 'TriggerMarker':
            matrix4d = marker_i.find('Matrix4D')
            marker_descriptions.append(marker_i.get('description'))
            marker_times.append(marker_i.get('recordingTime'))

        else:
            raise ValueError(f"markertype '{markertype}' unknown.")

        # get values
        for im_index1 in range(4):
            for im_index2 in range(4):
                marker_array[0, im_index1, im_index2] = (float(matrix4d.get('data' + str(im_index1) + str(im_index2))))
        im_array = np.append(im_array, marker_array, axis=0)

    return im_array, marker_descriptions, marker_times


def read_triggermarker_localite(fn_xml):
    warnings.warn("This function is deprecated. Use `read_triggermarker` instead.", DeprecationWarning)
    return read_triggermarker(fn_xml)


def read_triggermarker(fn_xml):
    """
    Read instrument-marker and conditions from neuronavigator .xml-file.

    Parameters
    ----------
    fn_xml : str
        Path to TriggerMarker.xml file
        (e.g. Subject_0/Sessions/Session_YYYYMMDDHHMMSS/TMSTrigger/TriggerMarkers_Coil1_YYYYMMDDHHMMSS.xml)

    Returns
    -------
    list of

        m_nnav : np.ndarray of float
            (4, 4, N) Neuronavigation coordinates of N stimuli (4x4 matrices).
        didt : np.ndarray of float
            (N) Rate of change of coil current in (A/us).
        stim_int : np.ndarray of float
            (N) Stimulator intensity in (% MSO).
        descr : list of str
            (N) Labels of the instrument-marker-conditions.
        rec_time : list of str
            (N) Recording time in ms.
    """
    m_nnav = np.empty([4, 4, 0])
    descr = []
    stim_int = []
    didt = []
    rec_time = []

    # parse XML document
    im_tree = xmlt.parse(fn_xml)
    im_root = im_tree.getroot()

    # iterate over all 'InstrumentMarker' tags
    for im_iter in im_root.iter('TriggerMarker'):
        m = np.empty([4, 4, 1])

        # read description
        descr.append(im_iter.get('description'))
        rec_time.append(im_iter.get('recordingTime'))

        # read di/dt and stimulator intensity
        im_rv = im_iter.find('ResponseValues').findall('Value')

        for _im_rv in im_rv:
            # di/dt
            if _im_rv.get('key') == "valueA":
                didt.append(float(_im_rv.get('response')))
            # stimulator intensity
            elif _im_rv.get('key') == "amplitudeA":
                stim_int.append(float(_im_rv.get('response')))

        # read matrix
        im_ma = im_iter.find('Matrix4D')

        for im_index1 in range(4):
            for im_index2 in range(4):
                m[im_index1, im_index2, 0] = (float(im_ma.get('data' + str(im_index1) + str(im_index2))))

        # check if coil position is untracked
        np.eye(4)
        if (m[:, :, 0] == np.eye(4)).all():
            print(f"Untracked coil position found for idx {m_nnav.shape[2]}.")
            m[:3, :4, 0] = np.nan

        m_nnav = np.append(m_nnav, m, axis=2)

    didt = np.array(didt)
    stim_int = np.array(stim_int)

    return [m_nnav, didt, stim_int, descr, rec_time]


def merge_exp_data_localite(subject, coil_outlier_corr_cond, remove_coil_skin_distance_outlier, coil_distance_corr,
                            exp_idx=0, mesh_idx=0, drop_mep_idx=None, mep_onsets=None, cfs_data_column=None,
                            channels=None, verbose=False, plot=False, start_mep=18, end_mep=35):
    """
    Merge the TMS coil positions (TriggerMarker) and the mep data into an experiment.hdf5 file.

    Parameters
    ----------
    subject : pynibs.subject.Subject
        Subject object.
    coil_outlier_corr_cond : bool
        Correct outlier of coil position and orientation (+-2 mm, +-3 deg) in case of conditions.
    remove_coil_skin_distance_outlier : bool
        Remove outlier of coil position lying too far away from the skin surface (+- 5 mm).
    coil_distance_corr : bool
        Perform coil <-> head distance correction (coil is moved towards head surface until coil touches scalp).
    exp_idx : str, default: 0
        Experiment ID.
    mesh_idx : str, default: 0
        Mesh ID.
    drop_mep_idx : List of int, optional
        Which MEPs to remove before matching.
    mep_onsets : List of int, optional
        If there are multiple .cfs per TMS Navigator sessions, onsets in [ms] of .cfs. E.g.: ``[0, 71186]``.
    cfs_data_column : int or list of int, optional
        Column(s) of dataset in .cfs file.
    channels : list of str, optional
        List of channel names.
    verbose : bool, default: false
        Flag to indicate verbosity.
    plot : bool, default: False
        Plot MEPs and p2p evaluation.
    start_mep : float, default: 18
        Start of time frame after TMS pulse where p2p value is evaluated (in ms).
    end_mep : float, default: 35
        End of time frame after TMS pulse where p2p value is evaluated (in ms).
    """
    if channels is None:
        channels = ["channel_0"]
    mep_paths_lst = subject.exp[exp_idx]['fn_data']
    tms_paths_lst = subject.exp[exp_idx]['fn_tms_nav']
    im_lst = subject.exp[exp_idx]['cond']
    nii_exp_path_lst = subject.exp[exp_idx]['fn_mri_nii']
    nii_conform_path = os.path.join(subject.mesh[mesh_idx]["mesh_folder"], subject.mesh[mesh_idx]["fn_mri_conform"])
    fn_exp_hdf5 = subject.exp[exp_idx]['fn_exp_hdf5'][0]
    fn_coil = subject.exp[exp_idx]['fn_coil']
    fn_mesh_hdf5 = subject.mesh[mesh_idx]['fn_mesh_hdf5']
    temp_dir = os.path.join(os.path.split(subject.exp[exp_idx]['fn_exp_hdf5'][0])[0], "nnav2simnibs")
    subject_obj = subject

    # allocate dict
    dict_lst = []

    # handle instrument marker
    if len(im_lst) < len(tms_paths_lst):
        for _ in range(len(tms_paths_lst)):
            im_lst.append(im_lst[0])

    # handle coil serial numbers
    coil_sn_lst = pynibs.get_coil_sn_lst(fn_coil)

    # get TMS pulse onset
    tms_pulse_time = subject.exp[exp_idx]['tms_pulse_time']

    # iterate over all files
    if mep_onsets is None:
        mep_onsets = [None] * len(mep_paths_lst)

    len_conds = []

    for cfs_paths, tms_paths, coil_sn, nii_exp_path, im, mep_onsets \
            in zip(mep_paths_lst, tms_paths_lst, coil_sn_lst, nii_exp_path_lst, im_lst, mep_onsets):
        dict_lst.extend(combine_nnav_mep(xml_paths=tms_paths,
                                         cfs_paths=cfs_paths,
                                         im=im,
                                         coil_sn=coil_sn,
                                         nii_exp_path=nii_exp_path,
                                         nii_conform_path=nii_conform_path,
                                         patient_id=subject.id,
                                         tms_pulse_time=tms_pulse_time,
                                         drop_mep_idx=drop_mep_idx,
                                         mep_onsets=mep_onsets,
                                         cfs_data_column=cfs_data_column,
                                         temp_dir=temp_dir,
                                         channels=channels,
                                         nnav_system=subject_obj.exp[exp_idx]["nnav_system"],
                                         mesh_approach=subject_obj.mesh[mesh_idx]["approach"],
                                         plot=plot,
                                         start_mep=start_mep,
                                         end_mep=end_mep))

        if len(len_conds) == 0:
            len_conds.append(len(dict_lst))
        else:
            len_conds.append(len(dict_lst) - len_conds[-1])

    # convert list of dict to dict of list
    results_dct = pynibs.list2dict(dict_lst)

    # check if we have a single pulse TMS experiments where every pulse is one condition
    single_pulse_experiment = np.zeros(len(len_conds))

    start = 0
    stop = len_conds[0]
    for i in range(len(len_conds)):
        if len(np.unique(np.array(results_dct["condition"])[start:stop])) == len_conds[i]:
            single_pulse_experiment[i] = True

        if i < (len(len_conds) - 1):
            start = stop
            stop = stop + len_conds[i + 1]

    # redefine condition vector because in case of multiple .cfs files and .xml files the conditions may double
    if single_pulse_experiment.all():
        results_dct["condition"] = np.arange(len(dict_lst))

    # reformat coil positions to 4x4 matrices
    coil_0 = np.zeros((4, 4, len(dict_lst)))
    coil_1 = np.zeros((4, 4, len(dict_lst)))
    coil_mean = np.zeros((4, 4, len(dict_lst)))

    # coil_0[3, 3, :] = 1
    # coil_1[3, 3, :] = 1
    # coil_mean[3, 3, :] = 1

    for m in range(4):
        for n in range(4):
            coil_0[m, n, :] = results_dct[f"coil0_{m}{n}"]
            coil_1[m, n, :] = results_dct[f"coil1_{m}{n}"]
            coil_mean[m, n, :] = results_dct[f"coil_mean_{m}{n}"]

            results_dct.pop(f"coil0_{m}{n}")
            results_dct.pop(f"coil1_{m}{n}")
            results_dct.pop(f"coil_mean_{m}{n}")

    coil_0 = np.split(coil_0, coil_0.shape[2], axis=2)
    coil_1 = np.split(coil_1, coil_1.shape[2], axis=2)
    coil_mean = np.split(coil_mean, coil_mean.shape[2], axis=2)

    coil_0 = [c.reshape((4, 4)) for c in coil_0]
    coil_1 = [c.reshape((4, 4)) for c in coil_1]
    coil_mean = [c.reshape((4, 4)) for c in coil_mean]

    results_dct["coil_0"] = coil_0
    results_dct["coil_1"] = coil_1
    results_dct["coil_mean"] = coil_mean

    results_dct["current"] = [float(c) for c in results_dct["current"]]

    # coil outlier correction
    if subject_obj.exp[exp_idx]["fn_exp_hdf5"] is not None or subject_obj.exp[exp_idx]["fn_exp_hdf5"] != []:
        fn_exp_hdf5 = subject_obj.exp[exp_idx]["fn_exp_hdf5"][0]

    elif subject_obj.exp[exp_idx]["fn_exp_csv"] is not None or subject_obj.exp[exp_idx]["fn_exp_csv"] != []:
        fn_exp_hdf5 = subject_obj.exp[exp_idx]["fn_exp_csv"][0]

    elif fn_exp_hdf5 is None or fn_exp_hdf5 == []:
        fn_exp_hdf5 = os.path.join(subject_obj.subject_folder, "exp", exp_idx, "experiment.hdf5")

    # remove coil position outliers (in case of conditions)
    #######################################################
    if coil_outlier_corr_cond:
        print("Removing coil position outliers")
        results_dct = pynibs.coil_outlier_correction_cond(exp=results_dct,
                                                          outlier_angle=5.,
                                                          outlier_loc=3.,
                                                          fn_exp_out=fn_exp_hdf5)

    # perform coil <-> head distance correction
    ###########################################
    if coil_distance_corr:
        print("Performing coil <-> head distance correction")
        results_dct = pynibs.coil_distance_correction(exp=results_dct,
                                                      fn_geo_hdf5=fn_mesh_hdf5,
                                                      remove_coil_skin_distance_outlier=remove_coil_skin_distance_outlier,
                                                      fn_plot=os.path.split(fn_exp_hdf5)[0])

    # plot finally used mep data
    ############################
    if plot:
        print("Creating MEP plots ...")
        sampling_rate = pynibs.get_mep_sampling_rate(cfs_paths[0])

        # Compute start and stop idx according to sampling rate
        start_mep = int((20 / 1000.) * sampling_rate)
        end_mep = int((35 / 1000.) * sampling_rate)

        # compute tms pulse idx in samplerate space
        tms_pulse_sample = int(tms_pulse_time * sampling_rate)

        for i_mep in tqdm(range(len(results_dct["mep_raw_data"]))):
            for i_channel, channel in enumerate(channels):
                # TODO: merge this code with calc_p2p
                sweep = results_dct["mep_raw_data"][i_mep][i_channel, :]
                sweep_filt = results_dct["mep_filt_data"][i_mep][i_channel, :]

                # get index for begin of mep search window
                # index_max_begin = np.argmin(sweep) + start_mep  # get TMS impulse # int(0.221 / 0.4 * sweep.size)
                # beginning of mep search window
                srch_win_start = tms_pulse_sample + start_mep  # get TMS impulse # in

                if srch_win_start >= sweep_filt.size:
                    srch_win_start = sweep_filt.size - 1

                # index_max_end = sweep_filt.size  # int(0.234 / 0.4 * sweep.size) + 1
                srch_win_end = srch_win_start + end_mep - start_mep

                fn_channel = os.path.join(os.path.split(cfs_paths[0])[0], "plots", channel)

                if not os.path.exists(fn_channel):
                    os.makedirs(fn_channel)

                fn_plot = os.path.join(fn_channel, f"mep_{i_mep:04}")
                t = np.arange(len(sweep)) / sampling_rate
                sweep_min_idx = np.argmin(sweep_filt[srch_win_start:srch_win_end]) + srch_win_start
                sweep_max_idx = np.argmax(sweep_filt[srch_win_start:srch_win_end]) + srch_win_start

                plt.figure(figsize=[4.07, 3.52])
                plt.plot(t, sweep)
                plt.plot(t, sweep_filt)
                plt.scatter(t[sweep_min_idx], sweep_filt[sweep_min_idx], 15, color="r")
                plt.scatter(t[sweep_max_idx], sweep_filt[sweep_max_idx], 15, color="r")
                plt.plot(t, np.ones(len(t)) * sweep_filt[sweep_min_idx], linestyle="--", color="r", linewidth=1)
                plt.plot(t, np.ones(len(t)) * sweep_filt[sweep_max_idx], linestyle="--", color="r", linewidth=1)
                plt.grid()
                plt.legend(["raw", "filtered", "p2p"], loc='upper right')

                plt.xlim([np.max((tms_pulse_time - 0.01, np.min(t))),
                          np.min((t[tms_pulse_sample + end_mep] + 0.1, np.max(t)))])
                plt.ylim([-1.1 * np.abs(sweep_filt[sweep_min_idx]), 1.1 * np.abs(sweep_filt[sweep_max_idx])])

                plt.xlabel("time in s", fontsize=11)
                plt.ylabel("MEP in mV", fontsize=11)
                plt.tight_layout()

                plt.savefig(fn_plot, dpi=200, transparent=True)
                plt.close()

    # Write experimental data to hdf5
    ###############################################
    # stimulation data
    df_stim_data = pd.DataFrame.from_dict(results_dct)
    df_stim_data = df_stim_data.drop(columns=["mep"])
    df_stim_data = df_stim_data.drop(columns=["mep_raw_data_time"])
    df_stim_data = df_stim_data.drop(columns=["mep_filt_data"])
    df_stim_data = df_stim_data.drop(columns=["mep_raw_data"])

    # raw data
    phys_data_raw_emg = {"time": results_dct["mep_raw_data_time"]}

    for chan_idx, chan in enumerate(channels):
        results_dct[f"mep_raw_data_{chan}"] = [sweep[chan_idx, :] for sweep in results_dct["mep_raw_data"]]
        phys_data_raw_emg[f"mep_raw_data_{chan}"] = results_dct[f"mep_raw_data_{chan}"]

    df_phys_data_raw_emg = pd.DataFrame.from_dict(phys_data_raw_emg)

    # post-processed data
    phys_data_postproc_emg = {"time": results_dct["mep_raw_data_time"]}

    for chan_idx, chan in enumerate(channels):
        phys_data_postproc_emg[f"mep_filt_data_{chan}"] = [sweep[chan_idx, :] for sweep in results_dct["mep_filt_data"]]
        phys_data_postproc_emg[f"p2p_{chan}"] = [mep[chan_idx] for mep in results_dct["mep"]]
        phys_data_postproc_emg[f"mep_latency_{chan}"] = [lat[chan_idx] for lat in results_dct["mep_latency"]]

    df_phys_data_postproc_emg = pd.DataFrame.from_dict(phys_data_postproc_emg)

    # save in .hdf5 file
    df_stim_data.to_hdf(fn_exp_hdf5, "stim_data")
    # df_stim_data[['coil_mean']].to_hdf(fn_exp_hdf5, "stim_data")
    # [print(type(df_stim_data[['coil_mean']].iloc[0].values)) for i in range(df_stim_data.shape[0])]
    # df_stim_data.columns
    df_phys_data_postproc_emg.to_hdf(fn_exp_hdf5, "phys_data/postproc/EMG")
    df_phys_data_raw_emg.to_hdf(fn_exp_hdf5, "phys_data/raw/EMG")

    with h5py.File(fn_exp_hdf5, "a") as f:
        f.create_dataset(name="stim_data/info/channels", data=np.array(channels).astype("|S"))


def merge_exp_data_rt(subject, coil_outlier_corr_cond, remove_coil_skin_distance_outlier, coil_distance_corr,
                      cond=None, exp_idx=0, mesh_idx=0, drop_trial_idx=None, verbose=False, plot=False):
    """
    Merge the TMS coil positions (TriggerMarker) and the mep data into an experiment.hdf5 file.

    Parameters
    ----------
    subject : pynibs.subject.Subject
        Subject object.
    coil_outlier_corr_cond : bool
        Correct outlier of coil position and orientation (+-2 mm, +-3 deg) in case of conditions.
    remove_coil_skin_distance_outlier : bool
        Remove outlier of coil position lying too far away from the skin surface (+- 5 mm).
    coil_distance_corr : bool
        Perform coil <-> head distance correction (coil is moved towards head surface until coil touches scalp).
    cond : string, optional
        Which condition to analyse.
    exp_idx : str, default: 0
        Experiment ID.
    mesh_idx : str, default: 0
        Mesh ID.
    drop_trial_idx : List of int, optional
        Which MEPs to remove before matching.
    verbose : bool, default: False
        Flag indicating verbosity.
    plot : bool, default: False
        Plot RTs and a running average over 10 trials.
    """
    behavior_paths_lst = subject.exp[exp_idx]['fn_data']
    tms_paths_lst = subject.exp[exp_idx]['fn_tms_nav']
    im_lst = subject.exp[exp_idx]['cond']
    nii_exp_path_lst = subject.exp[exp_idx]['fn_mri_nii']
    nii_conform_path = os.path.join(subject.mesh[mesh_idx]["mesh_folder"], subject.mesh[mesh_idx]["fn_mri_conform"])
    fn_exp_hdf5 = subject.exp[exp_idx]['fn_exp_hdf5'][0]
    fn_coil = subject.exp[exp_idx]['fn_coil']
    fn_mesh_hdf5 = subject.mesh[mesh_idx]['fn_mesh_hdf5']
    temp_dir = os.path.join(os.path.split(subject.exp[exp_idx]['fn_exp_hdf5'][0])[0],
                            "nnav2simnibs",
                            f"mesh_{mesh_idx}")
    subject_obj = subject

    # allocate dict
    dict_lst = []

    # handle instrument marker
    if len(im_lst) < len(tms_paths_lst):
        for _ in range(len(tms_paths_lst)):
            im_lst.append(im_lst[0])

    # handle coil serial numbers
    coil_sn_lst = pynibs.get_coil_sn_lst(fn_coil)

    # get TMS pulse onset
    tms_pulse_time = subject.exp[exp_idx]['tms_pulse_time']

    len_conds = []

    for behavior_paths, tms_paths, coil_sn, nii_exp_path, im \
            in zip(behavior_paths_lst, tms_paths_lst, coil_sn_lst, nii_exp_path_lst, im_lst):
        dict_lst.extend(combine_nnav_rt(xml_paths=tms_paths,
                                        behavior_paths=behavior_paths,
                                        im=im,
                                        coil_sn=coil_sn,
                                        nii_exp_path=nii_exp_path,
                                        nii_conform_path=nii_conform_path,
                                        patient_id=subject.id,
                                        drop_trial_idx=drop_trial_idx,
                                        temp_dir=temp_dir,
                                        cond=cond,
                                        nnav_system=subject_obj.exp[exp_idx]["nnav_system"],
                                        mesh_approach=subject_obj.mesh[mesh_idx]["approach"],
                                        plot=plot))

        if len(len_conds) == 0:
            len_conds.append(len(dict_lst))
        else:
            len_conds.append(len(dict_lst) - len_conds[-1])

    # convert list of dict to dict of list
    results_dct = pynibs.list2dict(dict_lst)

    # check if we have a single pulse TMS experiments where every pulse is one condition
    single_pulse_experiment = np.zeros(len(len_conds))

    results_dct["condition"] = np.arange(len(dict_lst))

    # reformat coil positions to 4x4 matrices
    coil_0 = np.zeros((4, 4, len(dict_lst)))
    coil_1 = np.zeros((4, 4, len(dict_lst)))
    coil_mean = np.zeros((4, 4, len(dict_lst)))

    # coil_0[3, 3, :] = 1
    # coil_1[3, 3, :] = 1
    # coil_mean[3, 3, :] = 1

    for m in range(4):
        for n in range(4):
            coil_0[m, n, :] = results_dct[f"coil0_{m}{n}"]
            coil_1[m, n, :] = results_dct[f"coil1_{m}{n}"]
            coil_mean[m, n, :] = results_dct[f"coil_mean_{m}{n}"]

            results_dct.pop(f"coil0_{m}{n}")
            results_dct.pop(f"coil1_{m}{n}")
            results_dct.pop(f"coil_mean_{m}{n}")

    coil_0 = np.split(coil_0, coil_0.shape[2], axis=2)
    coil_1 = np.split(coil_1, coil_1.shape[2], axis=2)
    coil_mean = np.split(coil_mean, coil_mean.shape[2], axis=2)

    coil_0 = [c.reshape((4, 4)) for c in coil_0]
    coil_1 = [c.reshape((4, 4)) for c in coil_1]
    coil_mean = [c.reshape((4, 4)) for c in coil_mean]

    results_dct["coil_0"] = coil_0
    results_dct["coil_1"] = coil_1
    results_dct["coil_mean"] = coil_mean

    results_dct["current"] = [float(c) for c in results_dct["current"]]

    # coil outlier correction
    if subject_obj.exp[exp_idx]["fn_exp_hdf5"] is not None or subject_obj.exp[exp_idx]["fn_exp_hdf5"] != []:
        fn_exp_hdf5 = subject_obj.exp[exp_idx]["fn_exp_hdf5"][0]

    elif subject_obj.exp[exp_idx]["fn_exp_csv"] is not None or subject_obj.exp[exp_idx]["fn_exp_csv"] != []:
        fn_exp_hdf5 = subject_obj.exp[exp_idx]["fn_exp_csv"][0]

    elif fn_exp_hdf5 is None or fn_exp_hdf5 == []:
        fn_exp_hdf5 = os.path.join(subject_obj.subject_folder, "exp", exp_idx, "experiment.hdf5")

    # remove coil position outliers (in case of conditions)
    #######################################################
    if coil_outlier_corr_cond:
        print("Removing coil position outliers")
        results_dct = pynibs.coil_outlier_correction_cond(exp=results_dct,
                                                          outlier_angle=5.,
                                                          outlier_loc=3.,
                                                          fn_exp_out=fn_exp_hdf5)

    # perform coil <-> head distance correction
    ###########################################
    if coil_distance_corr:
        print("Performing coil <-> head distance correction")
        results_dct = pynibs.coil_distance_correction(exp=results_dct,
                                                      fn_geo_hdf5=fn_mesh_hdf5,
                                                      remove_coil_skin_distance_outlier=remove_coil_skin_distance_outlier,
                                                      fn_plot=os.path.split(fn_exp_hdf5)[0])

    # plot finally used rt data
    ############################
    if plot:
        # assign data
        x = results_dct['number']
        y = results_dct['rt']

        # calculate running average over 10 trials
        avg_window = 10
        average_y = []
        for ind in range(len(y) - avg_window + 1):
            average_y.append(np.mean(y[ind:ind + avg_window]))
        # insert NaNs to match lengths
        for ind in range(avg_window - 1):
            average_y.insert(0, np.nan)

        # create plot
        plt.close()
        plt.figure(num='RT-plot for subject ' + subject.id)
        plt.scatter(x, y, s=10, label='reaction times in ms')
        plt.plot(x, average_y, color='blue', linestyle='-', label='running average')
        plt.xlabel('trial number')
        plt.legend()
        plt.title('development of the reaction times over the course of the trial')
        fn_rt_plot = os.path.join(subject_obj.subject_folder, "exp", "model_TMS", "plot_RT.png")
        plt.savefig(fn_rt_plot, dpi=600)
        # plt.show()
        plt.close()

    # Write experimental data to hdf5
    ###############################################
    # stimulation data
    stim_dict = {
        'date': results_dct['date'],
        'coil_sn': results_dct['coil_sn'],
        'patient_id': results_dct['patient_id'],
        'coil_0': results_dct['coil_0'],
        'coil_1': results_dct['coil_1'],
        'coil_mean': results_dct['coil_mean'],
        'current': results_dct['current'],
        'time_tms': results_dct['ts_tms'],
    }
    df_stim_data = pd.DataFrame.from_dict(stim_dict)

    behave_dict = {
        'number': results_dct['number'],
        'rt': results_dct['rt'],
        'time_trial': results_dct['time_trial']
    }
    df_behave_data = pd.DataFrame.from_dict(behave_dict)

    # save in .hdf5 file
    df_stim_data.to_hdf(fn_exp_hdf5, "stim_data")
    df_behave_data.to_hdf(fn_exp_hdf5, "behavioral_data")


def merge_exp_data_ft(subject, coil_outlier_corr_cond, remove_coil_skin_distance_outlier, coil_distance_corr,
                      cond, exp_idx=0, mesh_idx=0, drop_trial_idx=None, verbose=False, plot=False):
    """
    Merge the TMS coil positions (TriggerMarker) and the mep data into an experiment.hdf5 file.

    Parameters
    ----------
    subject : pynibs.subject.Subject
        Subject object.
    exp_idx : str
        Experiment ID.
    mesh_idx : str
        Mesh ID.
    coil_outlier_corr_cond : bool
        Correct outlier of coil position and orientation (+-2 mm, +-3 deg) in case of conditions.
    cond : string
        Which behavioral measurement to analyse.
    remove_coil_skin_distance_outlier : bool
        Remove outlier of coil position lying too far away from the skin surface (+- 5 mm).
    coil_distance_corr : bool
        Perform coil <-> head distance correction (coil is moved towards head surface until coil touches scalp).
    drop_trial_idx : List of int or None
        Which MEPs to remove before matching.
    verbose : bool
        Plot output messages.
    plot : bool, optional, default: False
        Plot RTs and a running average over 10 trials.
    """
    behavior_paths_lst = subject.exp[exp_idx]['fn_data']
    tms_paths_lst = subject.exp[exp_idx]['fn_tms_nav']
    im_lst = subject.exp[exp_idx]['cond']
    nii_exp_path_lst = subject.exp[exp_idx]['fn_mri_nii']
    nii_conform_path = os.path.join(subject.mesh[mesh_idx]["mesh_folder"], subject.mesh[mesh_idx]["fn_mri_conform"])
    fn_exp_hdf5 = subject.exp[exp_idx]['fn_exp_hdf5'][0]
    fn_coil = subject.exp[exp_idx]['fn_coil']
    fn_mesh_hdf5 = subject.mesh[mesh_idx]['fn_mesh_hdf5']
    temp_dir = os.path.join(os.path.split(subject.exp[exp_idx]['fn_exp_hdf5'][0])[0],
                            "nnav2simnibs",
                            f"mesh_{mesh_idx}")
    subject_obj = subject

    # allocate dict
    dict_lst = []

    # handle instrument marker
    if len(im_lst) < len(tms_paths_lst):
        for _ in range(len(tms_paths_lst)):
            im_lst.append(im_lst[0])

    # handle coil serial numbers
    coil_sn_lst = pynibs.get_coil_sn_lst(fn_coil)

    # get TMS pulse onset
    tms_pulse_time = subject.exp[exp_idx]['tms_pulse_time']

    len_conds = []

    for behavior_paths, tms_paths, coil_sn, nii_exp_path, im \
            in zip(behavior_paths_lst, tms_paths_lst, coil_sn_lst, nii_exp_path_lst, im_lst):
        dict_lst.extend(combine_nnav_ft(xml_paths=tms_paths,
                                        behavior_paths=behavior_paths,
                                        im=im,
                                        coil_sn=coil_sn,
                                        nii_exp_path=nii_exp_path,
                                        nii_conform_path=nii_conform_path,
                                        patient_id=subject.id,
                                        drop_trial_idx=drop_trial_idx,
                                        temp_dir=temp_dir,
                                        cond=cond,
                                        nnav_system=subject_obj.exp[exp_idx]["nnav_system"],
                                        mesh_approach=subject_obj.mesh[mesh_idx]["approach"],
                                        plot=plot))

        if len(len_conds) == 0:
            len_conds.append(len(dict_lst))
        else:
            len_conds.append(len(dict_lst) - len_conds[-1])

    # convert list of dict to dict of list
    results_dct = pynibs.list2dict(dict_lst)

    # check if we have a single pulse TMS experiments where every pulse is one condition
    single_pulse_experiment = np.zeros(len(len_conds))

    results_dct["condition"] = np.arange(len(dict_lst))

    # reformat coil positions to 4x4 matrices
    coil_0 = np.zeros((4, 4, len(dict_lst)))
    coil_1 = np.zeros((4, 4, len(dict_lst)))
    coil_mean = np.zeros((4, 4, len(dict_lst)))

    # coil_0[3, 3, :] = 1
    # coil_1[3, 3, :] = 1
    # coil_mean[3, 3, :] = 1

    for m in range(4):
        for n in range(4):
            coil_0[m, n, :] = results_dct[f"coil0_{m}{n}"]
            coil_1[m, n, :] = results_dct[f"coil1_{m}{n}"]
            coil_mean[m, n, :] = results_dct[f"coil_mean_{m}{n}"]

            results_dct.pop(f"coil0_{m}{n}")
            results_dct.pop(f"coil1_{m}{n}")
            results_dct.pop(f"coil_mean_{m}{n}")

    coil_0 = np.split(coil_0, coil_0.shape[2], axis=2)
    coil_1 = np.split(coil_1, coil_1.shape[2], axis=2)
    coil_mean = np.split(coil_mean, coil_mean.shape[2], axis=2)

    coil_0 = [c.reshape((4, 4)) for c in coil_0]
    coil_1 = [c.reshape((4, 4)) for c in coil_1]
    coil_mean = [c.reshape((4, 4)) for c in coil_mean]

    results_dct["coil_0"] = coil_0
    results_dct["coil_1"] = coil_1
    results_dct["coil_mean"] = coil_mean

    results_dct["current"] = [float(c) for c in results_dct["current"]]

    # create dir
    path_exp_hdf5 = os.path.join(subject_obj.subject_folder, "exp", exp_idx, cond)
    isExist = os.path.exists(path_exp_hdf5)
    if not isExist:
        os.makedirs(path_exp_hdf5)

    # coil outlier correction
    if subject_obj.exp[exp_idx]["fn_exp_hdf5"] is not None or subject_obj.exp[exp_idx]["fn_exp_hdf5"] != []:
        fn_exp_hdf5 = os.path.join(path_exp_hdf5, "experiment.hdf5")

    elif subject_obj.exp[exp_idx]["fn_exp_csv"] is not None or subject_obj.exp[exp_idx]["fn_exp_csv"] != []:
        fn_exp_hdf5 = subject_obj.exp[exp_idx]["fn_exp_csv"][0]

    elif fn_exp_hdf5 is None or fn_exp_hdf5 == []:
        fn_exp_hdf5 = os.path.join(subject_obj.subject_folder, "exp", exp_idx, "experiment.hdf5")

    # remove coil position outliers (in case of conditions)
    #######################################################
    if coil_outlier_corr_cond:
        print("Removing coil position outliers")
        results_dct = pynibs.coil_outlier_correction_cond(exp=results_dct,
                                                          outlier_angle=5.,
                                                          outlier_loc=3.,
                                                          fn_exp_out=fn_exp_hdf5)

    # perform coil <-> head distance correction
    ###########################################
    if coil_distance_corr:
        print("Performing coil <-> head distance correction")
        results_dct = pynibs.coil_distance_correction(exp=results_dct,
                                                      fn_geo_hdf5=fn_mesh_hdf5,
                                                      remove_coil_skin_distance_outlier=remove_coil_skin_distance_outlier,
                                                      fn_plot=os.path.split(fn_exp_hdf5)[0])

    # plot finally used ft data
    ############################
    if plot:
        # assign data
        x = results_dct['number']
        y = results_dct['ft']

        # calculate running average over 10 trials
        avg_window = 10
        average_y = []
        for ind in range(len(y) - avg_window + 1):
            average_y.append(np.mean(y[ind:ind + avg_window]))
        # insert NaNs to match lengths
        for ind in range(avg_window - 1):
            average_y.insert(0, np.nan)

        # create plot
        plt.close()
        plt.figure(num=cond + ' FT-plot for subject ' + subject.id)
        plt.scatter(x, y, s=10, label='reaction times in ms')
        plt.plot(x, average_y, color='blue', linestyle='-', label='running average')
        plt.xlabel('trial number')
        plt.legend()
        plt.title('Finger tapping performance over the course of the trial')
        fn_ft_plot = os.path.join(subject_obj.subject_folder, "exp", "FingerTapping", cond, "plot_ft.png")
        plt.savefig(fn_ft_plot, dpi=600)
        # plt.show()
        plt.close()

    # Write experimental data to hdf5
    ###############################################
    # stimulation data
    stim_dict = {
        'date': results_dct['date'],
        'coil_sn': results_dct['coil_sn'],
        'patient_id': results_dct['patient_id'],
        'coil_0': results_dct['coil_0'],
        'coil_1': results_dct['coil_1'],
        'coil_mean': results_dct['coil_mean'],
        'current': results_dct['current'],
        'time_tms': results_dct['ts_tms'],
    }
    df_stim_data = pd.DataFrame.from_dict(stim_dict)

    behave_dict = {
        'number': results_dct['number'],
        'ft': results_dct['ft'],
        'time_trial': results_dct['time_trial']
    }
    df_behave_data = pd.DataFrame.from_dict(behave_dict)

    # save in .hdf5 file
    df_stim_data.to_hdf(fn_exp_hdf5, "stim_data")
    df_behave_data.to_hdf(fn_exp_hdf5, "behavioral_data")


def match_behave_and_triggermarker(mep_time_lst, xml_paths, bnd_factor=0.99 / 2, isi=None):
    """
    Sort out timestamps of mep and tms files that do not match.

    Parameters
    ----------
    mep_time_lst : list of datetime.timedelta
        timedeltas of MEP recordings.
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file; if there is no coil1-file, use empty string.
    bnd_factor : float, default: 0.99/2
        Bound factor relative to interstimulus interval in which +- interval to match neuronavigation and mep data
        from their timestamps (0 means perfect matching, 0.5 means +- half interstimulus interval).
    isi : float, optional
        Interstimulus intervals. If not provided it's estimated from the first trial.

    Returns
    -------
    tms_index_lst : list of int
        Indices of tms-timestamps that match.
    mep_index_lst : list of int
        Indices of mep-timestamps that match.
    tms_time_lst : list of datetime
        TMS timestamps.
    """
    # mep_time_lst = []
    # for cfs_path in cfs_paths:
    #     _, mep_time_lst_tmp = get_mep_elements(cfs_path, tms_pulse_time)
    #     mep_time_lst.extend(mep_time_lst_tmp)

    _, tms_ts_lst, _, tms_idx_invalid = pynibs.localite.get_tms_elements(xml_paths, verbose=True)

    # get timestamp difference of mep measurements
    if isi is None:
        isi = (mep_time_lst[1] - mep_time_lst[0]).total_seconds()

    # get offset to match first timestamps of mep and tms
    coil_offset = datetime.timedelta(seconds=float(tms_ts_lst[0]) / 1000)

    # match start time with the timestamp of the xml file
    # tms_time_lst = [mep_time_lst[0] - time_offset + datetime.timedelta(seconds=float(ts) / 1000) for ts in tms_ts_lst]
    coil_time_delta_lst = [-coil_offset + datetime.timedelta(seconds=float(ts) / 1000) for ts in tms_ts_lst]
    coil_time_delta_lst_orig = [-coil_offset + datetime.timedelta(seconds=float(ts) / 1000) for ts in tms_ts_lst]

    # get index for cfs and xml files
    # mep_time_index, mep_index_lst = 0, []
    # tms_time_index, tms_index_lst = 0, []

    # get maximal list length of time lists
    # min_lst_length = min([len(lst) for lst in [mep_time_lst, tms_time_delta_lst]])

    # mep_last_working_idx = 0
    # tms_last_working_idx = 0

    if (len(coil_time_delta_lst) + len(tms_idx_invalid)) == len(mep_time_lst):
        print("Equal amount of TMS and MEP data...")
        print(f"Removing invalid coil positions {tms_idx_invalid} from MEP data...")

        # invalid coil positions were already removed in previous call of get_tms_elements(xml_paths)
        coil_to_mep_match_lst = [i for i in range(len(tms_ts_lst))]

        # MEP indices without invalid coil positions
        mep_index_lst = [i for i in range(len(mep_time_lst)) if i not in tms_idx_invalid]

    else:
        mep_index_lst = []
        coil_to_mep_match_lst = []
        mep_time_lst = np.array(mep_time_lst)
        coil_time_delta_lst = np.array(coil_time_delta_lst)

        # iterate over all MEPs
        for mep_index in range(len(mep_time_lst)):
            # set bounds
            time_bnd_l = mep_time_lst[mep_index] + datetime.timedelta(
                    seconds=-isi * bnd_factor)  # time bound low
            time_bnd_h = mep_time_lst[mep_index] + datetime.timedelta(
                    seconds=+isi * bnd_factor)  # time bound high

            # search for corresponding TMS coil positions
            coil_mep_in_bound = (time_bnd_l <= coil_time_delta_lst) & (coil_time_delta_lst <= time_bnd_h)

            # no TMS coil position in bound (untracked coil position already removed)
            if np.sum(coil_mep_in_bound) == 0:
                print(f"Untracked coil position, excluding MEP_idx: {mep_index}")

            # one correct TMS coil position in bound
            elif np.sum(coil_mep_in_bound) == 1:
                mep_index_lst.append(mep_index)
                coil_match_index = np.where(coil_mep_in_bound)[0][0]
                coil_to_mep_match_lst.append(coil_match_index)

                # zero times on last match to avoid time shift
                mep_time_lst -= mep_time_lst[mep_index]
                coil_time_delta_lst -= coil_time_delta_lst[coil_match_index]

            # one correct and one accidental TMS coil position in bound -> take closest
            elif np.sum(coil_mep_in_bound) > 1:
                mep_index_lst.append(mep_index)
                delta_t = np.abs(np.array([mep_time_lst[mep_index] for _ in range(np.sum(coil_mep_in_bound))]) -
                                 np.array(coil_time_delta_lst)[coil_mep_in_bound])
                coil_match_index = np.where(coil_mep_in_bound)[0][np.argmin(delta_t)]
                coil_to_mep_match_lst.append(coil_match_index)

                print(f"Two tracked TMS coil positions found within search window -> choosing closest index by time.")
                print(
                        f"MEP_idx: {mep_index} ({mep_time_lst[mep_index]}) -> "
                        f"TMS_idx: {coil_match_index} ({coil_time_delta_lst[coil_match_index]})")

                # zero times on last match
                mep_time_lst -= mep_time_lst[mep_index]
                coil_time_delta_lst -= coil_time_delta_lst[coil_match_index]

    return [coil_to_mep_match_lst, mep_index_lst, coil_time_delta_lst_orig]


def get_patient_id(xml_path):
    """
    Read patient-ID.

    Parameters
    ----------
    xml_path : str
        Path to coil0-file.

    Returns
    -------
    xml_pd.find('patientID').text : str
        ID of patient.
    """

    patient_data_path = os.path.dirname(xml_path) + '/PatientData.xml'
    # parse XML document
    xml_tree = ET.parse(patient_data_path)
    xml_root = xml_tree.getroot()
    xml_pd = xml_root.find('patientData')
    return xml_pd.find('patientID').text


def combine_nnav_mep(xml_paths, cfs_paths, im, coil_sn,
                     nii_exp_path, nii_conform_path,
                     patient_id, tms_pulse_time, drop_mep_idx, mep_onsets, nnav_system, mesh_approach="headreco",
                     temp_dir=None, cfs_data_column=0, channels=None, plot=False, start_mep=18, end_mep=35):
    """
    Creates dictionary containing all experimental data.

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file; if there is no coil1-file, use empty string.
    cfs_paths : list of str
        Paths to .cfs mep file.
    im : list of str
        List of path to the instrument-marker-file or list of strings containing the instrument marker.
    coil_sn : str
        Coil-serial-number.
    nii_exp_path : str
        Path to the .nii file that was used in the experiment.
    nii_conform_path : str
        Path to the conform*.nii file used to calculate the E-fields with SimNIBS.
    patient_id : str
        Patient id.
    tms_pulse_time : float
        Time in [s] of TMS pulse as specified in signal.
    drop_mep_idx : List of int or None
        Which MEPs to remove before matching.
    mep_onsets : List of int or None
        If there are multiple .cfs per TMS Navigator sessions, onsets in [ms] of .cfs. E.g.: [0, 71186].
    nnav_system : str
        Type of neuronavigation system ("Localite", "Visor").
    mesh_approach : str, default: "headreco"
        Approach the mesh is generated with ("headreco" or "mri2mesh").
    temp_dir : str, default: None (fn_exp_mri_nii folder)
        Directory to save temporary files (transformation .nii and .mat files) (fn_exp_mri_nii folder).
    cfs_data_column : int or list of int, default: 0
        Column(s) of dataset in .cfs file.
    channels : list of str, optional
        Channel names.
    plot : bool, default: False
        Plot MEPs and p2p evaluation.
    start_mep : float, default: 18
        Start of time frame after TMS pulse where p2p value is evaluated (in ms).
    end_mep : float, default: 35
        End of time frame after TMS pulse where p2p value is evaluated (in ms).

    Returns
    -------
    dict_lst : list of dicts, one dict for each zap
          'number'
          'condition'
          'current'
          'mep_raw_data'
          'mep'
          'mep_latency'
          'mep_filt_data'
          'mep_raw_data_time'
          'time_tms'
          'ts_tms'
          'time_mep'
          'date'
          'coil_sn'
          'patient_id'
    """
    # get arrays and lists
    coil_array, ts_tms_lst, current_lst, tms_idx_invalid = pynibs.get_tms_elements(xml_paths, verbose=False)

    # get MEP amplitudes from .cfs files
    time_mep_lst, mep_latencies = [], []
    last_mep_onset = datetime.timedelta(seconds=0)
    mep_raw_data, mep_filt_data, p2p_arr = None, None, None
    mep_raw_data_time = None

    if not isinstance(cfs_paths, list):
        cfs_paths = [cfs_paths]

    for idx, cfs_path in enumerate(cfs_paths):
        # calc MEP amplitudes and MEP onset times from .cfs file
        p2p_array_tmp, time_mep_lst_tmp, \
            mep_raw_data_tmp, mep_filt_data_tmp, \
            mep_raw_data_time, mep_latency = pynibs.get_mep_elements(mep_fn=cfs_path,
                                                                     tms_pulse_time=tms_pulse_time,
                                                                     drop_mep_idx=drop_mep_idx,
                                                                     cfs_data_column=cfs_data_column,
                                                                     channels=channels,
                                                                     plot=plot,
                                                                     start_mep=start_mep,
                                                                     end_mep=end_mep)

        # add .cfs onsets from subject object and add onset of last mep from last .cfs file
        if mep_onsets is not None:
            time_mep_lst_tmp = [time_mep_lst_tmp[i] + datetime.timedelta(milliseconds=mep_onsets[idx]) +
                                last_mep_onset for
                                i in range(len(time_mep_lst_tmp))]
        time_mep_lst.extend(time_mep_lst_tmp)

        if idx == 0:
            p2p_arr = p2p_array_tmp
            mep_raw_data = mep_raw_data_tmp
            mep_filt_data = mep_filt_data_tmp
            mep_latencies = mep_latency
        else:
            mep_raw_data = np.vstack((mep_raw_data, mep_raw_data_tmp))
            mep_filt_data = np.vstack((mep_filt_data, mep_filt_data_tmp))
            p2p_arr = np.concatenate((p2p_arr, p2p_array_tmp), axis=1)
            mep_latencies.append(mep_latency)

        last_mep_onset = time_mep_lst[-1]
    mep_latencies = np.array(mep_latencies)

    # match TMS Navigator zaps and MEPs
    tms_index_lst, mep_index_lst, time_tms_lst = match_behave_and_triggermarker(mep_time_lst=time_mep_lst,
                                                                                xml_paths=xml_paths,
                                                                                bnd_factor=0.99 / 2)  # 0.99/2

    if cfs_paths[0].endswith("cfs"):
        experiment_date_time = pynibs.get_time_date(cfs_paths)
    else:
        experiment_date_time = "N/A"

    # get indices of not recognizable coils
    unit_matrix_index_list = []
    for unit_matrix_index1 in range(coil_array.shape[0]):
        for unit_matrix_index2 in range(coil_array.shape[1]):
            if np.allclose(coil_array[unit_matrix_index1, unit_matrix_index2, :, :], np.identity(4)):
                unit_matrix_index_list.append([unit_matrix_index1, unit_matrix_index2])

    # set condition names in case of random sampling
    if im is None or im == [""] or im == "":
        coil_cond_lst = [str(i) for i in range(len(ts_tms_lst))]
        drop_idx = []
    else:
        # get conditions from instrument markers
        if os.path.isfile(im[0]):
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_file(xml_paths, im[0])
        else:
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_string(xml_paths, im)

    # coordinate transform (for coil_0, coil_1, coil_mean)
    for idx in range(coil_array.shape[0]):
        # move axis, calculate and move back
        m_simnibs = np.moveaxis(coil_array[idx, :, :, :], 0, 2)
        m_simnibs = pynibs.nnav2simnibs(fn_exp_nii=nii_exp_path[0],
                                        fn_conform_nii=nii_conform_path,
                                        m_nnav=m_simnibs,
                                        nnav_system=nnav_system,
                                        mesh_approach=mesh_approach,
                                        temp_dir=temp_dir)

        coil_array[idx, :, :, :] = np.moveaxis(m_simnibs, 2, 0)

    # replace transformed identity matrices
    for unit_matrix_indices in unit_matrix_index_list:
        coil_array[unit_matrix_indices[0], unit_matrix_indices[1], :, :] = np.identity(4)

    # list for dictionaries
    dict_lst = []
    idx = 0

    assert len(tms_index_lst) == len(mep_index_lst)

    delta_t = []
    ts_mep = [time_mep_lst[i] for i in mep_index_lst]
    ts_tms = [time_tms_lst[i] for i in tms_index_lst]

    for t1, t2 in zip(ts_mep, ts_tms):
        # print(f"MEP: {t1}     TMS: {t2}")
        delta_t.append(np.abs(t1 - t2))

    plt.plot(np.array([delta_t[i].microseconds for i in range(len(delta_t))]) / 1000)
    plt.xlabel("TMS pulse #", fontsize=11)
    plt.ylabel(r"$\Delta t$ in ms", fontsize=11)
    fn_plot = os.path.join(os.path.split(cfs_paths[0])[0], "delta_t_mep_vs_tms.png")
    plt.savefig(fn_plot, dpi=600)
    plt.close()

    # iterate over mep and tms indices to get valid matches of MEPs and TMS Navigator information
    for tms_index, mep_index in zip(tms_index_lst, mep_index_lst):
        if tms_index not in drop_idx:
            dictionary = {'number': idx,
                          'condition': coil_cond_lst[tms_index],
                          'current': current_lst[tms_index],
                          'mep_raw_data': mep_raw_data[:, mep_index, :],
                          'mep': p2p_arr[:, mep_index],
                          'mep_latency': mep_latencies[:, mep_index],
                          'mep_filt_data': mep_filt_data[:, mep_index, :],
                          'mep_raw_data_time': mep_raw_data_time,
                          'time_tms': time_tms_lst[tms_index].total_seconds(),
                          'ts_tms': ts_tms_lst[tms_index],
                          'time_mep': time_mep_lst[mep_index].total_seconds(),
                          'date': experiment_date_time,
                          'coil_sn': coil_sn,
                          'patient_id': patient_id}

            # write coils
            for index1 in range(4):
                for index2 in range(4):
                    dictionary.update({'coil0_' + str(index1) + str(index2): coil_array[0, tms_index, index1, index2]})
                    dictionary.update({'coil1_' + str(index1) + str(index2): coil_array[1, tms_index, index1, index2]})
                    dictionary.update(
                            {'coil_mean_' + str(index1) + str(index2): coil_array[2, tms_index, index1, index2]})

            # get time difference
            time_diff = time_tms_lst[tms_index] - time_mep_lst[mep_index]
            time_diff = time_diff.total_seconds() * 1000
            dictionary.update({'time_diff': time_diff})

            # append to list
            dict_lst.append(dictionary)

            idx += 1

    return dict_lst


def combine_nnav_rt(xml_paths, behavior_paths, im, coil_sn,
                    nii_exp_path, nii_conform_path,
                    patient_id, drop_trial_idx, nnav_system, cond,
                    mesh_approach="headreco", temp_dir=None, plot=False):
    """
    Creates dictionary containing all experimental data.

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string.
    behavior_paths : list of str
        Paths to .cfs mep file.
    im : list of str
        List of path to the instrument-marker-file or list of strings containing the instrument marker.
    coil_sn : str
        Coil-serial-number.
    nii_exp_path : str
        Path to the .nii file that was used in the experiment.
    nii_conform_path : str
        Path to the conform*.nii file used to calculate the E-fields with SimNIBS.
    patient_id : str
        Patient id.
    drop_trial_idx : List of int or None
        Which MEPs to remove before matching.
    nnav_system : str
        Type of neuronavigation system ("Localite", "Visor").
    cond : str
        Condition name in data_path.
    mesh_approach : str, default: "headreco"
        Approach the mesh is generated with ("headreco" or "mri2mesh").
    temp_dir : str, optional
        Directory to save temporary files (transformation .nii and .mat files) (fn_exp_mri_nii folder).
    plot : bool, default: False
        Plot MEPs and p2p evaluation.

    Returns
    -------
    dict_lst : list of dicts, one dict for each zap
          'number'
          'condition'
          'current'
          'mep_raw_data'
          'mep'
          'mep_latency'
          'mep_filt_data'
          'mep_raw_data_time'
          'time_tms'
          'ts_tms'
          'time_mep'
          'date'
          'coil_sn'
          'patient_id'
    """

    # get arrays and lists
    coil_array, ts_tms_lst, current_lst, tms_idx_invalid = pynibs.get_tms_elements(xml_paths, verbose=False)

    # get RT from .csv files
    time_mep_lst = []
    # last_mep_onset = datetime.timedelta(seconds=0)
    rt_arr = None

    if not isinstance(behavior_paths, list):
        behavior_paths = [behavior_paths]

    for idx, behavior_path in enumerate(behavior_paths):
        # get RT and trial onsets from .csv file
        rt_array_tmp, trial_onset_lst_tmp, mean_isi = pynibs.get_trial_data_from_csv(behavior_fn=behavior_path,
                                                                                     drop_trial_idx=drop_trial_idx,
                                                                                     cond=cond,
                                                                                     only_corr=True)

        time_mep_lst.extend(trial_onset_lst_tmp)

        if idx == 0:
            rt_arr = rt_array_tmp
        else:
            rt_arr = np.concatenate((rt_arr, rt_array_tmp), axis=1)

        # last_mep_onset = time_mep_lst[-1]

    # match TMS Navigator zaps and MEPs
    time_mep_lst = [datetime.timedelta(seconds=onset / 1000) for onset in time_mep_lst]

    tms_index_lst, mep_index_lst, time_tms_lst = match_behave_and_triggermarker(mep_time_lst=time_mep_lst,
                                                                                xml_paths=xml_paths,
                                                                                isi=mean_isi)  # 0.99/2

    experiment_date_time = "N/A"

    # get indices of not recognizable coils
    unit_matrix_index_list = []
    for unit_matrix_index1 in range(coil_array.shape[0]):
        for unit_matrix_index2 in range(coil_array.shape[1]):
            if np.allclose(coil_array[unit_matrix_index1, unit_matrix_index2, :, :], np.identity(4)):
                unit_matrix_index_list.append([unit_matrix_index1, unit_matrix_index2])

    # set condition names in case of random sampling
    if im is None or im == [""] or im == "":
        coil_cond_lst = [str(i) for i in range(len(ts_tms_lst))]
        drop_idx = []
    else:
        # get conditions from instrument markers
        if os.path.isfile(im[0]):
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_file(xml_paths, im[0])
        else:
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_string(xml_paths, im)

    # coordinate transform (for coil_0, coil_1, coil_mean)
    for idx in range(coil_array.shape[0]):
        # move axis, calculate and move back
        m_simnibs = np.moveaxis(coil_array[idx, :, :, :], 0, 2)
        m_simnibs = pynibs.nnav2simnibs(fn_exp_nii=nii_exp_path[0],
                                        fn_conform_nii=nii_conform_path,
                                        m_nnav=m_simnibs,
                                        nnav_system=nnav_system,
                                        mesh_approach=mesh_approach,
                                        temp_dir=temp_dir)

        coil_array[idx, :, :, :] = np.moveaxis(m_simnibs, 2, 0)

    # replace transformed identity matrices
    for unit_matrix_indices in unit_matrix_index_list:
        coil_array[unit_matrix_indices[0], unit_matrix_indices[1], :, :] = np.identity(4)

    # list for dictionaries
    dict_lst = []
    idx = 0

    assert len(tms_index_lst) == len(mep_index_lst)

    delta_t = []
    ts_mep = [time_mep_lst[i] for i in mep_index_lst]
    ts_tms = [time_tms_lst[i] for i in tms_index_lst]

    for t1, t2 in zip(ts_mep, ts_tms):
        # print(f"MEP: {t1}     TMS: {t2}")
        delta_t.append(np.abs(t1 - t2))

    plt.plot(np.array([delta_t[i].microseconds for i in range(len(delta_t))]) / 1000)
    plt.xlabel("TMS pulse #", fontsize=11)
    plt.ylabel(r"$\Delta t$ in ms", fontsize=11)
    fn_plot = os.path.join(os.path.split(behavior_paths[0])[0], "delta_t_mep_vs_tms.png")
    plt.savefig(fn_plot, dpi=600)
    plt.close()

    # iterate over trial and tms indices to get valid matches of trials and TMS Navigator information
    for tms_index, mep_index in zip(tms_index_lst, mep_index_lst):
        if tms_index not in drop_idx:
            dictionary = {'number': idx,
                          'condition': coil_cond_lst[tms_index],
                          'current': current_lst[tms_index],
                          'rt': rt_arr[mep_index],
                          'time_tms': time_tms_lst[tms_index].total_seconds(),
                          'ts_tms': ts_tms_lst[tms_index],
                          'time_trial': time_mep_lst[mep_index].total_seconds(),
                          'date': experiment_date_time,
                          'coil_sn': coil_sn,
                          'patient_id': patient_id}

            # write coils
            for index1 in range(4):
                for index2 in range(4):
                    dictionary.update({'coil0_' + str(index1) + str(index2): coil_array[0, tms_index, index1, index2]})
                    dictionary.update({'coil1_' + str(index1) + str(index2): coil_array[1, tms_index, index1, index2]})
                    dictionary.update(
                            {'coil_mean_' + str(index1) + str(index2): coil_array[2, tms_index, index1, index2]})

            # get time difference
            time_diff = time_tms_lst[tms_index] - time_mep_lst[mep_index]
            time_diff = time_diff.total_seconds() * 1000
            dictionary.update({'time_diff': time_diff})

            # append to list
            dict_lst.append(dictionary)

            idx += 1

    return dict_lst


def combine_nnav_ft(xml_paths, behavior_paths, im, coil_sn,
                    nii_exp_path, nii_conform_path,
                    patient_id, drop_trial_idx, nnav_system, cond,
                    mesh_approach="headreco", temp_dir=None, plot=False):
    """
    Creates dictionary containing all experimental data.

    Parameters
    ----------
    xml_paths : list of str
        Paths to coil0-file and optionally coil1-file if there is no coil1-file, use empty string
    behavior_paths : list of str
        Paths to .csv ft file
    im : list of str
        List of path to the instrument-marker-file or list of strings containing the instrument marker
    coil_sn : str
        Coil-serial-number
    nii_exp_path : str
        Path to the .nii file that was used in the experiment
    nii_conform_path : str
        Path to the conform*.nii file used to calculate the E-fields with SimNIBS
    patient_id : str
        Patient id
    drop_trial_idx : List of int or None
        Which fts to remove before matching.
    temp_dir : str, default: None (fn_exp_mri_nii folder)
        Directory to save temporary files (transformation .nii and .mat files)
    nnav_system : str
        Type of neuronavigation system ("Localite", "Visor")
    cond : str
        behavioral outcome
    mesh_approach : str, default: "headreco"
        Approach the mesh is generated with ("headreco" or "mri2mesh")
    plot : bool, default: False
        Plot MEPs and p2p evaluation

    Returns
    -------
    dict_lst : list of dicts, one dict for each zap
          'number'
          'condition'
          'current'
          'mep_raw_data'
          'mep'
          'mep_latency'
          'mep_filt_data'
          'mep_raw_data_time'
          'time_tms'
          'ts_tms'
          'time_mep'
          'date'
          'coil_sn'
          'patient_id'
    """

    # get arrays and lists
    coil_array, ts_tms_lst, current_lst, tms_idx = pynibs.get_tms_elements(xml_paths, verbose=False)

    # get finger tapping data from .csv files
    time_ft_lst = []
    # last_mep_onset = datetime.timedelta(seconds=0)
    ft_arr = None

    if not isinstance(behavior_paths, list):
        behavior_paths = [behavior_paths]

    for idx, behavior_path in enumerate(behavior_paths):
        # get finger tapping data and trial onsets from .csv file
        ft_array_tmp, trial_onset_lst_tmp, mean_isi = pynibs.get_ft_data_from_csv(behavior_fn=behavior_path,
                                                                                  drop_trial_idx=drop_trial_idx,
                                                                                  cond=cond)

        time_ft_lst.extend(trial_onset_lst_tmp)

        if idx == 0:
            ft_arr = ft_array_tmp
        else:
            ft_arr = np.concatenate((ft_arr, ft_array_tmp), axis=1)

        # last_mep_onset = time_mep_lst[-1]

    # match TMS Navigator zaps and fts
    time_ft_lst = [datetime.timedelta(seconds=onset / 1000) for onset in time_ft_lst]

    tms_index_lst, ft_index_lst, time_tms_lst = match_behave_and_triggermarker(mep_time_lst=time_ft_lst,
                                                                               xml_paths=xml_paths,
                                                                               isi=mean_isi)  # 0.99/2

    experiment_date_time = "N/A"

    # get indices of not recognizable coils
    unit_matrix_index_list = []
    for unit_matrix_index1 in range(coil_array.shape[0]):
        for unit_matrix_index2 in range(coil_array.shape[1]):
            if np.allclose(coil_array[unit_matrix_index1, unit_matrix_index2, :, :], np.identity(4)):
                unit_matrix_index_list.append([unit_matrix_index1, unit_matrix_index2])

    # set condition names in case of random sampling
    if im is None or im == [""] or im == "":
        coil_cond_lst = [str(i) for i in range(len(ts_tms_lst))]
        drop_idx = []
    else:
        # get conditions from instrument markers
        if os.path.isfile(im[0]):
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_file(xml_paths, im[0])
        else:
            coil_cond_lst, drop_idx = pynibs.match_instrument_marker_string(xml_paths, im)

    # coordinate transform (for coil_0, coil_1, coil_mean)
    for idx in range(coil_array.shape[0]):
        # move axis, calculate and move back
        m_simnibs = np.moveaxis(coil_array[idx, :, :, :], 0, 2)
        m_simnibs = pynibs.nnav2simnibs(fn_exp_nii=nii_exp_path[0],
                                        fn_conform_nii=nii_conform_path,
                                        m_nnav=m_simnibs,
                                        nnav_system=nnav_system,
                                        mesh_approach=mesh_approach,
                                        temp_dir=temp_dir)

        coil_array[idx, :, :, :] = np.moveaxis(m_simnibs, 2, 0)

    # replace transformed identity matrices
    for unit_matrix_indices in unit_matrix_index_list:
        coil_array[unit_matrix_indices[0], unit_matrix_indices[1], :, :] = np.identity(4)

    # list for dictionaries
    dict_lst = []
    idx = 0

    assert len(tms_index_lst) == len(ft_index_lst)

    delta_t = []
    ts_ft = [time_ft_lst[i] for i in ft_index_lst]
    ts_tms = [time_tms_lst[i] for i in tms_index_lst]

    for t1, t2 in zip(ts_ft, ts_tms):
        # print(f"MEP: {t1}     TMS: {t2}")
        delta_t.append(np.abs(t1 - t2))

    plt.plot(np.array([delta_t[i].microseconds for i in range(len(delta_t))]) / 1000)
    plt.xlabel("TMS pulse #", fontsize=11)
    plt.ylabel(r"$\Delta t$ in ms", fontsize=11)
    fn_plot = os.path.join(os.path.split(behavior_paths[0])[0], "delta_t_ft_vs_tms.png")
    plt.savefig(fn_plot, dpi=600)
    plt.close()

    # iterate over trial and tms indices to get valid matches of trials and TMS Navigator information
    for tms_index, ft_index in zip(tms_index_lst, ft_index_lst):
        if tms_index not in drop_idx:
            dictionary = {'number': idx,
                          'condition': coil_cond_lst[tms_index],
                          'current': current_lst[tms_index],
                          'ft': ft_arr[ft_index],
                          'time_tms': time_tms_lst[tms_index].total_seconds(),
                          'ts_tms': ts_tms_lst[tms_index],
                          'time_trial': time_ft_lst[ft_index].total_seconds(),
                          'date': experiment_date_time,
                          'coil_sn': coil_sn,
                          'patient_id': patient_id}

            # write coils
            for index1 in range(4):
                for index2 in range(4):
                    dictionary.update({'coil0_' + str(index1) + str(index2): coil_array[0, tms_index, index1, index2]})
                    dictionary.update({'coil1_' + str(index1) + str(index2): coil_array[1, tms_index, index1, index2]})
                    dictionary.update(
                            {'coil_mean_' + str(index1) + str(index2): coil_array[2, tms_index, index1, index2]})

            # get time difference
            time_diff = time_tms_lst[tms_index] - time_ft_lst[ft_index]
            time_diff = time_diff.total_seconds() * 1000
            dictionary.update({'time_diff': time_diff})

            # append to list
            dict_lst.append(dictionary)

            idx += 1

    return dict_lst
