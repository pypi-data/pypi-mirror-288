"""
The `optimizhat.py` module provides functions for optimizing coil placements in Transcranial Magnetic Stimulation
(TMS) based on given electric field matrices and fMRI statistics. It includes functions for identifying optimal coil
placement regions, calculating the gain map between a reference and an optimized sequence of electric fields,
and performing virtual online optimization to determine the congruence factor.

The module includes the following functions:

- `rowvec_diff()`: This function returns the coil configuration out of all available configurations exhibiting the
highest minimum difference to the already selected configurations.

- `get_optimal_coil_positions()`: This function determines a set of optimal coil positions for TMS regression analysis.

- `online_optimization()`: This function performs virtual online optimization to determine the congruence factor.
After an initial set of coil positions, the algorithm iteratively optimizes the next coil position based on the
virtually measured MEP data.

- `calc_opt_gain_map()`: This function calculates the gain map between a reference e_matrix (e.g. from random
sampling) and an optimized sequence of electric fields for mapping.

- `optimal_coilplacement_region()`: This function identifies the optimal coil placement regions based on given
electric field (E-field) matrices and fMRI statistics.

Each function in this module is documented with docstrings providing more detailed information about its purpose,
parameters, and return values.

This module is primarily used for handling and optimizing coil placements in TMS studies.
"""
import os
import h5py
import numpy as np
import multiprocessing
from functools import partial
from matplotlib import pyplot as plt

import pynibs


def rowvec_diff(candidate_coil_idcs, selected_coil_idcs, efields_diff_mat):
    """
    Given a difference matrix (e.g. of row vectors/coil configurations) this function
    returns the coil configuration out of all available configurations exhibiting the
    highest minimum difference to the already selected configurations.

    :param candidate_coil_idcs: np.ndarry[int]
        List of indices of coil configurations that are still available to pick for the optiized sequence.
    :param selected_coil_idcs: np.ndarray[int]
        List of indices of coil configurations that have already been selected for the optimized sequence.
    :param efields_diff_mat: np.ndarray[float], [n_coil,n_coil]
        Difference matrix, where each cell denotes the magnitude of the difference vector between
        two coil configurations (determined by row_idx,col_idx).

    Returns
    -------
    coil_idx: int
        index of coil configuration with maximal minimal difference to the set of already selected coil configurations.
    """

    # min_diff_selected_to_all_coil_pos = matrix with:
    #   rows -> set of selected coil configurations (selected_coil_idcs)
    #   columns -> available coil configuration for optimization (candidate_coil_idcs)
    min_diff_selected_to_all_coil_pos = np.min(efields_diff_mat[selected_coil_idcs][:, candidate_coil_idcs], axis=0)

    # returned index valid in the "idx_list" array
    return np.argmax(min_diff_selected_to_all_coil_pos), np.max(min_diff_selected_to_all_coil_pos)


def get_optimal_coil_positions(
        e_matrix,
        criterion,
        n_stim,
        ele_idx_1=None,
        ele_idx_2=None,
        fn_out_hdf5=None,
        n_cpu=4,
        zap_idx_opt=None,
        regression_cmap=None,
        regression_fit_parameters=None,
        metrics_weights=None,
        overwrite=True,
        verbose=True,
        fn_coilpos_hdf5=None,
        start_zap_idx=-1,
        fim_fit_fun=None,
        fim_p2p_amps=None,
        fim_didt_list=None,
        fim_rmt_mso=None,
        fim_mso_didt_conversion_factor=1.43,
        fim_visited_positions_e_mat=None,
        fim_regression_n_refit=10,
        fim_debug_screenshot_dir_fn=None,
        fim_roi_pts=None,
        fim_roi_tris=None,
        fim_use_gpu=False):
    """
    Determine set of optimal coil positions for TMS regression analysis.

    Parameters
    ----------
    e_matrix : np.ndarray of float
        (n_stim, n_ele) Matrix containing the electric field values in the ROI.
    criterion : str
        Optimization criterion:
        * "mc_cols": Minimization of mutual coherence between columns
        * "mc_rows": Minimization of mutual coherence between rows
        * "svd": Minimization of condition number
        * "dist": Equal distant sampling
        * "dist_svd": Minimization of condition number and equidistant sampling
        * "dist_mc_cols": Minimization of mutual coherence between columns and equidistant sampling
        * "dist_mc_rows": Minimization of mutual coherence between rows and equidistant sampling
        * "coverage": Maximizes the electric field coverage
        * "variability": Maximizes variability between elements

    n_stim : int
        Maximum number of stimulations.
    ele_idx_1 : np.ndarray of int, optional
        Element indices the first optimization goal is performed for, If None, all elements are consiered.
    ele_idx_2 : np.ndarray of int, optional
        Element indices the first optimization goal is performed for. If None, all elements are consiered.
    n_cpu : int
        Number of threads.
    fn_out_hdf5 : str, optional
        Returns the list of optimal zap indices if fn_out_hdf5 is None, otherwise, save the results in .hdf5 file.
        Filename of output .hdf5 file where the zap index lists are saved in subfolder "zap_index_lists"

        * "zap_index_lists/0": [213]
        * "zap_index_lists/1": [213, 5]
        * etc

    zap_idx_opt : list of int, optional
        List of already selected optimal coil positions
        (those are ignored in the optimization and will not be picked again).
    fim_fit_fun : function object
        Function object defined in interval [0, 1] (only needed for fim optimization).
    regression_fit_parameters : dict [n_ele], optional, optional
        The parameter estimates that should be used for the FIM optimization (whole ROI).
        The keys are the parameter names of fun
        (only needed for fim and dist optimization).
    regression_cmap : np.ndarray of float [n_ele], optional, optional
        Congruence factor in each ROI element. Used to weight fim and dist optimization
        (only needed for fim and dist optimization).
    metrics_weights : list of float [2], default: [0.5, 0.5]
        Weights of optimization criteria in case of multiple goal functions (e_all_coil_pos.g. fim_svd).
        Higher weight means higher importance for the respective criteria.
        By default both optimization criteria are weighted equally [0.5, 0.5].
    overwrite : bool, default: True
        Overwrite existing solutions or read existing hdf5 file and continue optimization.
    verbose : bool, default: True
        Print output messages.
    fn_coilpos_hdf5 : str
        File containing the corresponding coil positions and orientations (centers, m0, m1, m2).
    start_zap_idx : int, default: 0
        First zap index to start greedy search.
    fim_didt_list : np.array(float), [len(zap_idx_opt)]
        List of realized dI/dt of each of the already stimulated coil configurations in 'zap_idx_opt'.
        Not required for any other metric than FIM.
    fim_rmt_mso : int
        Resting motor threshold used as the lower boundary of the FIM optimal e-field scaling. Unit in %MSO
        Not required for any other metric than FIM.
    fim_mso_didt_conversion_factor : float, default: 1.43
        Factor to convert between realized current (dI/dt) and percentage of maximum stimulator output (%MSO).
        Defaults to 1.43 describing the factor of a Magventure Pro with an MCF-B65 coil.
        Not required for any other metric than FIM.
    fim_visited_positions_e_mat : np.ndarray[float], (len(zap_idx_opt], n_ele), optional
        The efield matrix computed using the actually approached coil configurations.
        This is intended to make the FIM method even more precise by taking into account slight deviations in the
        approached coil configuration instead of relying on the static pre-computed coil configurations.
        Not required for any other metric than FIM.
    fim_p2p_amps : np.ndarray[float], (len(zap_idx_opt))
        EMG peak to peak amplitudes associated with the already collected (optimal) coil positions.
        Not required for any other metric than FIM.
    fim_didt_list : np.ndarray[float], (len(zap_idx_op))
        Realized current (didt) in TMS coil (as returned by the stimulator).
        of the already collected (optimal) coil positions.
        Not required for any other metric than FIM.
    fim_regression_n_refit : float
        Number of refits used in the mag(E)<>p2p regression during FIM optimization.
        Not required for any other metric than FIM.
    fim_debug_screenshot_dir_fn : str
        String representation of the fully qualified path to a directory where a 3D rendering of the
        the FIM optimal coil positions, ie coil positions that can reach the FIM optimal e-field strength
        at the current target hotspot given the MSO bounds [fim_rmt_mso, 100], should be saved.
        Not required for any other metric than FIM.
    fim_roi_pts : np.ndarray, (n_points x 3)
        Points (vertices) of ROI surface mesh (where the congruence scores should be computed on).
        Not required for any other metric than FIM.
    fim_roi_tris : np.ndarray, (n_tris x 3)
        Connectivity list of the 'fim_roi_points'.
        Not required for any other metric than FIM.
    fim_use_gpu : bool
        True: Use cupy and CUDA acceleration for the computation of the correlation matrix.
        False: Use Python multiprocessing for the computation of the corrleation matrix.
        Not required for any other metric than FIM.

    Returns
    -------
    zap_idx_e_opt : list of int
        (n_stim) Optimal zap indices.
    <File> .hdf5 file
        Output file containing the zap index lists.
    """
    if zap_idx_opt is not None and fn_out_hdf5 is not None and (os.path.exists(fn_out_hdf5) and not overwrite):
        raise ValueError("zap_idx_opt and fn_out_hdf5 given... please choose whether to load optimal zap indices from "
                         "file or given explicitly as list")

    e_all_coil_pos = e_matrix

    if ele_idx_1 is None:
        ele_idx_1 = np.arange(e_all_coil_pos.shape[1])

    if ele_idx_2 is None:
        ele_idx_2 = np.arange(e_all_coil_pos.shape[1])

    # Normalize congruence map as it is used to weight the scores of some metrics.
    if regression_cmap is not None:
        regression_cmap_normalized = regression_cmap / np.max(regression_cmap)

    # value of the associated optimization metric
    crit = np.zeros(n_stim)

    # Position of the last optimal coil idx in the result list.
    # Greedy search will continue from 'idx_of_last_result+1' until 'n_stim' configurations have been found.
    idx_of_last_result = -1 if start_zap_idx == -1 else 0

    # Out of the set of all available indices, which indices should be considered for the sequence of optimal configs.
    idcs_to_check = list(range(0, e_all_coil_pos.shape[0]))

    # Initialize the list of indices valid for rows of 'e_matrix'
    # (= coil configurations identified as optimal configurations)
    zap_idx_e_opt = [-1 for _ in range(n_stim)]
    zap_idx_e_opt[0] = start_zap_idx
    # Adopt predefined set of optimal coil positions as 'zap_idx_e_opt'
    if zap_idx_opt is not None:
        num_visited_configurations = len(zap_idx_opt)
        idx_of_last_result = num_visited_configurations - 1
        zap_idx_e_opt[:num_visited_configurations] = zap_idx_opt
        for idx in zap_idx_opt:
            idcs_to_check.remove(idx)

        # set the next to-be determined position to 'start_zap_idx'
        zap_idx_e_opt[idx_of_last_result + 1] = start_zap_idx

    # load position and orientation vectors of all available coil configurations
    if fn_coilpos_hdf5 is not None:
        with h5py.File(fn_coilpos_hdf5, "r") as f:
            centers = f["centers"][:]
            m0 = f["m0"][:]
            m1 = f["m1"][:]
            m2 = f["m2"][:]

    pool = multiprocessing.Pool(n_cpu)

    # load already present optimization results
    if fn_out_hdf5 is not None:
        if not overwrite and os.path.exists(fn_out_hdf5):
            with h5py.File(fn_out_hdf5, "r") as f:

                idx_of_last_result = 0

                try:
                    keys = f[f"zap_index_list"].keys()
                    crit = f["criterion"][:]

                    for k in keys:
                        zap_idx_e_opt[int(k)] = list(f[f"zap_index_list/{k}"][:])

                        if int(k) > idx_of_last_result:
                            idx_of_last_result = int(k)

                    # check if loaded sequence starts with the same zap index as intended
                    if zap_idx_e_opt[0] != start_zap_idx:
                        idx_of_last_result = 0
                        zap_idx_e_opt = [-1 for _ in range(n_stim)]
                        zap_idx_e_opt[0] = start_zap_idx
                        if verbose:
                            print(f"Loaded sequence does not start with specified start idx (restarting optimization)")
                            print(f"=================================================================================")
                    else:
                        if verbose:
                            print(f"Loading optimal index set for n={idx_of_last_result + 1}")
                            print(f"====================================")

                        for idx in zap_idx_e_opt:
                            idcs_to_check.remove(idx)
                except KeyError:
                    pass

    if criterion == "rowvec_diff":
        # Preparation for the rowvec difference metric is independent of the number of requested stimulation (n_stim):
        #   Compute the difference matrix.
        workhorse_prepare = partial(pynibs.optimization.workhorses.rowvec_diff_prepare, array=e_all_coil_pos, ele_idx_1=ele_idx_1)
        coil_idx_list_chunks = pynibs.compute_chunks(list(range(e_all_coil_pos.shape[0])), n_cpu)
        res = pool.map(workhorse_prepare, coil_idx_list_chunks)

        # sum all difference matrices up = create upper triangle difference matrix
        efields_diff = np.sum(res, axis=0)

        efields_diff_mat_full = efields_diff + np.transpose(efields_diff)

        if n_stim >= 2:
            if idx_of_last_result < 1:
                # Search coil position sequence yielding the highest difference score.
                # Use the global maximum as the initial pair of positions.
                zap_idx_e_opt[:2] = list(
                        np.unravel_index(np.argmax(efields_diff_mat_full), efields_diff_mat_full.shape))
                crit[:2] = np.max(efields_diff_mat_full)

                # remove the identified optimal coil configuration
                # from the list of available/to-be checked configurations
                idcs_to_check.remove(zap_idx_e_opt[0])
                idcs_to_check.remove(zap_idx_e_opt[1])

                # We completed two positions: #0, #1
                idx_of_last_result = 1
        else:
            print("[WARN] get_optimal_coil_positions: A minimum number of n_stim=2 stimulations"
                  "can be computed for the metric 'rowvec_diff'.")

    workhorse_partial = None
    for idx_in_result_list in range(idx_of_last_result + 1, n_stim):
        if verbose:
            # if idx_of_last_result == 0:
            #     print(f"Initializing greedy algorithm for n={idx_in_result_list}")
            #     print(f"=====================================")
            #     print(f" >>> Chosen index: {start_zap_idx}")

            print(f"Calculating optimal idx for n={idx_in_result_list + 1}")
            print(f"==================================")

        # preparatory functions of some of the result metrics
        if criterion == "coverage":
            workhorse_prepare = partial(workhorses.coverage_prepare, array=e_all_coil_pos,
                                        zap_idx=zap_idx_e_opt[:idx_in_result_list - 1])
            ele_idx_list_chunks = pynibs.compute_chunks([j for j in range(e_all_coil_pos.shape[1])], n_cpu)
            res = pool.map(workhorse_prepare, ele_idx_list_chunks)

            x = np.zeros((1, 1))
            y = np.zeros((1, 1))

            for j in range(len(res)):
                if j == 0:
                    x = res[0][0]
                    y = res[0][1]
                else:
                    x = np.hstack((x, res[j][0]))
                    y = np.hstack((y, res[j][1]))

            workhorse_partial = partial(workhorses.coverage, array=e_all_coil_pos, x=x, y=y)
        # Preprocessing of metrics combined with FIM:
        # - determine the required %MSO for each candidate location via FIM
        # - determine valid candidate locations that can achieve a FIM optimal mag(E) within the valid range of
        #   the stimulator output intensity, %MSO in [RMT,100]
        elif "fim" in criterion:
            # Sanity checks first
            if n_stim - len(zap_idx_opt) > 1:
                raise ValueError("[Error] get_optimal_coil_positions: Cannot compute more than one new coil"
                                 "configuration with the FIM optimization criterion due to lacking feedback"
                                 "from future coil configurations.")

            if len(zap_idx_opt) != len(fim_didt_list) or len(zap_idx_opt) != len(fim_p2p_amps) or \
                    fim_visited_positions_e_mat is not None and len(fim_visited_positions_e_mat) != len(zap_idx_e_opt):
                raise ValueError("[Error] get_optimal_coil_positions: The number of provided optimized positions,"
                                 "the number of e-fields of the visited positions, the number of dI/dt values and the"
                                 "the number of p2p amplitudes must be the same:"
                                 "reflecting the number of already visited positions.")

            if fim_rmt_mso is None:
                raise ValueError("[Error] get_optimal_coil_positions: requested FIM optimal sampling without"
                                 "specifying a specific resting motor threshold (fim_rmt_mso).")

            if fim_fit_fun == pynibs.sigmoid4 or fim_fit_fun == pynibs.sigmoid4_log:
                default_sigmoid_params = {
                    "x0": 0.5,
                    "y0": 1e-10,
                    "r": 12.5,
                    "amp": 1
                }
            else:
                raise AttributeError("[Error] Unsupported function type requested for FIM optimization."
                                     "Currently 'simgoid4', 'sigmoig4_log' supported.")

            # convert between arbitrarily shaped sigmoids and a standard sigmoid defined by the parameters above
            def to_std_sigmoid(x, params_real_data, params_ideal_sigmoid):
                return params_real_data["r"] / params_ideal_sigmoid["r"] \
                    * \
                    (x - params_real_data["x0"]) \
                    + \
                    params_ideal_sigmoid["x0"]

            def from_std_sigmoid(x, params_real_data, params_ideal_sigmoid):
                return params_ideal_sigmoid["r"] / params_real_data["r"] \
                    * \
                    (x - params_ideal_sigmoid["x0"]) \
                    + \
                    params_real_data["x0"]

            # Normalize already selected e-fields to the argument space of the standard sigmoid [0, 1].
            if fim_didt_list is None:
                didt_list = np.ones(idx_in_result_list)
            else:
                didt_list = fim_didt_list

            e_optimal_positions = e_all_coil_pos[zap_idx_e_opt[:idx_in_result_list], :] \
                if fim_visited_positions_e_mat is None else fim_visited_positions_e_mat

            max_r2_ele_idx = np.argmax(regression_cmap_normalized)

            e_realized_in_hotspot = np.multiply(
                    e_optimal_positions[:, max_r2_ele_idx],
                    didt_list
            )

            # compute sigmoid4 fit parameters in hotspot if parameters were not provided externally as parameters
            if regression_fit_parameters is None:
                e_realized_in_hotspot_np = np.zeros((e_realized_in_hotspot.shape[0], 1))
                e_realized_in_hotspot_np[:, 0] = e_realized_in_hotspot

                _, regression_sigmoid_fitparams = pynibs.regress_data(
                        e_matrix=e_realized_in_hotspot_np,
                        mep=fim_p2p_amps,
                        fun=fim_fit_fun,
                        n_refit=fim_regression_n_refit,
                        n_cpu=n_cpu,
                        return_fits=True,
                        refit_discontinuities=False
                )[0]
            else:
                regression_sigmoid_fitparams = regression_fit_parameters

            e_in_hotspot_normalized_to_std_sigmoid = to_std_sigmoid(
                    e_realized_in_hotspot,
                    params_real_data=regression_sigmoid_fitparams,
                    params_ideal_sigmoid=default_sigmoid_params
            )
            e_in_hotspot_normalized_to_std_sigmoid = np.clip(e_in_hotspot_normalized_to_std_sigmoid, 0, 1)

            import time
            # Determine optimal e-field intensity for next zap for each ROI element.
            t0 = time.time()
            e_opt_in_hotspot_on_std_sigmoid = pynibs.get_optimal_sample_fim(
                    fun=fim_fit_fun,
                    x=e_in_hotspot_normalized_to_std_sigmoid,
                    p=default_sigmoid_params
            )
            print(f"Elapsed time FIM {round((time.time() - t0) * 10) / 10}")

            t0 = time.time()
            # Undo e-field normalization: e_opt contains the optimal mag(E) for each ROI element in 'ele_idx_1'
            e_opt_real_in_hotspot = from_std_sigmoid(
                    e_opt_in_hotspot_on_std_sigmoid,
                    params_real_data=regression_sigmoid_fitparams,
                    params_ideal_sigmoid=default_sigmoid_params
            )

            # Determine required %MSO for candidate coil configurations.
            e_candidates = e_all_coil_pos[idcs_to_check, :]

            # compute the current the stimulator would need to realize (dI/dt) to achieve
            # the 'e_opt' at the hotspot location for each of the candidate locations
            didt_opt = np.divide(np.ones(e_candidates.shape[0]) * e_opt_real_in_hotspot,
                                 e_candidates[:, max_r2_ele_idx])

            mso_opt = didt_opt / fim_mso_didt_conversion_factor

            # select feasible efields:
            # required e-field value at hotspot location must be achievable with
            # <= 100%MSO && >= resting motor threshold
            num_configurations_below_valid_range = np.sum(mso_opt < fim_rmt_mso)
            num_configurations_within_valid_range = np.sum(np.logical_and(fim_rmt_mso <= mso_opt, mso_opt <= 100))
            num_configurations_above_valid_range = np.sum(mso_opt > 100)

            # If the target e_opt could not be achieved with a stimulator intensity within the valid range for any of
            # the candidate coil configurations, use the bounds of the valid range depending on where most of the
            # outliers were (above or below).
            if num_configurations_within_valid_range == 0:
                if num_configurations_below_valid_range >= num_configurations_above_valid_range:
                    # setting 'mso_opt' to either of the bounds will make of the candidate locations available for the
                    # secondary optimization metric and still scale them in the minimum or maximum allowed direction as
                    # requested by the FIM optimization.
                    mso_opt = np.ones(mso_opt.shape) * fim_rmt_mso
                else:
                    mso_opt = np.ones(mso_opt.shape) * 100

                # convert to didt after changing mso values
                didt_opt = mso_opt * fim_mso_didt_conversion_factor

            # extract the indices of valid coil configurations and associated scaling factors
            achievable_candidates_idcs = np.where(np.logical_and(fim_rmt_mso <= mso_opt, mso_opt <= 100))[0].tolist()
            idcs_to_check = [idcs_to_check[i] for i in achievable_candidates_idcs]
            # Create didt scaling vector for all coil configurations:
            # - valid coil configurations exhibit a scaling factor accoridng to their computed optimla didt
            # - invlaid coil configurations remain unscaled
            # 'fim_didt_scaling' is used to initialize the metric workers:
            # Only through 'idcs_to_check' the worker individually subset the rows (=coil configurations) of the
            # full e-field matrix upon execution. To provide them with a (full) scaled e-field matrix the scaling
            # vector must be of the same length as the number of rows of the full efield matrix.
            fim_didt_scaling = np.ones(e_all_coil_pos.shape[0])
            fim_didt_scaling[idcs_to_check] = didt_opt[achievable_candidates_idcs]
            print(f"Elapsed time array stuff {round((time.time() - t0) * 10) / 10}")

            t0 = time.time()
            if fim_debug_screenshot_dir_fn is not None and fn_coilpos_hdf5 is not None:
                pynibs.render_coil_positions(
                        coil_conf_set_2_positions=centers[:],
                        coil_conf_set_2_orientations=m1[:],
                        coil_conf_set_1_positions=centers[achievable_candidates_idcs],
                        coil_conf_set_1_orientations=m1[achievable_candidates_idcs],
                        viewport_dim=(1280, 720),
                        camera_polar_coords=(-175, 66, 110),
                        screenshot_fn=os.path.join(
                                fim_debug_screenshot_dir_fn,
                                f"fim_coilpos_selection_debug_after_{e_realized_in_hotspot.shape[0]}_stims.png"
                        ),
                        interactive=False
                )
            print(f"Elapsed time Rendering {round((time.time() - t0) * 10) / 10}")

        # prepare the result metrics for the parallel execution
        if criterion == "svd":
            workhorse_partial = partial(workhorses.svd, array=e_all_coil_pos, ele_idx_1=ele_idx_1)

        elif criterion == "dist":
            workhorse_partial = partial(workhorses.dist, array=e_all_coil_pos, ele_idx_1=ele_idx_1)

        elif criterion == "mc_cols":
            e_all_coil_pos = e_all_coil_pos - np.mean(e_all_coil_pos[:, ele_idx_1], axis=1)[:, np.newaxis]
            workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1, mode="cols")

        elif criterion == "mc_rows":
            workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1, mode="rows")

        elif criterion == "variability":
            workhorse_partial = partial(workhorses.variability, array=e_all_coil_pos, ele_idx_1=ele_idx_1)

        elif criterion == "dist_mc_cols":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_2, mode="cols")
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.dist, array=e_all_coil_pos, ele_idx_1=ele_idx_1)
            else:
                workhorse_partial = partial(workhorses.dist_mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2,
                                            mode="cols")

        elif criterion == "dist_mc_rows":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_2, mode="rows")
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.dist, array=e_all_coil_pos, ele_idx_1=ele_idx_1)
            else:
                workhorse_partial = partial(workhorses.dist_mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2,
                                            mode="rows")

        elif criterion == "dist_svd":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.svd, array=e_all_coil_pos, ele_idx_1=ele_idx_2)
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.dist, array=e_all_coil_pos, ele_idx_1=ele_idx_1)
            else:
                workhorse_partial = partial(workhorses.dist_svd, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2)

        elif criterion == "fim":
            workhorse_partial = partial(workhorses.fim, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                        e_opt=e_opt_real_in_hotspot, c=regression_cmap_normalized)

        elif criterion == "fim_svd":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.svd, array=e_all_coil_pos, ele_idx_1=ele_idx_2)
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.fim, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            e_opt=e_opt_real_in_hotspot, c=regression_cmap_normalized)
            else:
                workhorse_partial = partial(workhorses.fim_svd, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2, e_opt=e_opt_real_in_hotspot,
                                            c=regression_cmap_normalized)

        elif criterion == "fim_mc_rows":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_2, mode="rows")
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.fim, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            e_opt=e_opt_real_in_hotspot, c=regression_cmap_normalized)
            else:
                workhorse_partial = partial(workhorses.fim_mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2, e_opt=e_opt_real_in_hotspot,
                                            c=regression_cmap_normalized,
                                            mode="rows")

        elif criterion == "fim_mc_cols":
            if metrics_weights[0] == 0:
                workhorse_partial = partial(workhorses.mc, array=e_all_coil_pos, ele_idx_1=ele_idx_2, mode="cols")
            elif metrics_weights[1] == 0:
                workhorse_partial = partial(workhorses.fim, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            e_opt=e_opt_real_in_hotspot, c=regression_cmap_normalized)
            else:
                workhorse_partial = partial(workhorses.fim_mc, array=e_all_coil_pos, ele_idx_1=ele_idx_1,
                                            ele_idx_2=ele_idx_2, e_opt=e_opt_real_in_hotspot,
                                            c=regression_cmap_normalized,
                                            mode="cols")
        elif criterion == "fim_correlation":
            try:
                e_all_coil_pos_scaled = np.multiply(e_all_coil_pos, fim_didt_scaling[:, np.newaxis])

                # mask regions of low r^2 out for correlation optimization
                max_r2_idx = np.argmax(regression_cmap_normalized)
                high_r2_roi_ele_idcs = np.array(regression_cmap_normalized > 0.6, dtype=np.int16)
                subsampled_ele_idc = np.zeros(regression_cmap_normalized.shape[0])
                subsampled_ele_idc[ele_idx_2] = 1

                ele_idcs_mask = np.logical_and(high_r2_roi_ele_idcs, subsampled_ele_idc).astype(np.int16)

                # for plotting set hotspot_idx to 2
                if fim_debug_screenshot_dir_fn is not None:
                    ele_idcs_mask[max_r2_idx] = 2
                    pynibs.render_data_on_surface(
                            points=fim_roi_pts,
                            tris=fim_roi_tris,
                            data=ele_idcs_mask,
                            screenshot_fn=os.path.join(
                                    fim_debug_screenshot_dir_fn,
                                    f"fim_decorrelation_idcs_{e_realized_in_hotspot.shape[0]}_stims.png"
                            ),
                            interactive=False
                    )
                # make sure to set max_r2_idx to 0 to avoid double insertion of the hotspot idx
                # (will be inserted at the end of the index list in any case)
                ele_idcs_mask[max_r2_idx] = 0

                subsampled_ele_idcs = np.append(np.where(ele_idcs_mask)[0], max_r2_idx)

                if not fim_use_gpu:
                    workhorse_partial = partial(
                            workhorses.roi_elmt_wise_corr,
                            array=e_all_coil_pos_scaled,
                            # hotspot idx must be last element of "ele_idx_1" to decorrelate
                            # only the hotspot idx with all other ROI elements
                            ele_idx_1=subsampled_ele_idcs,  # indices of elements marked with '1'
                            decorrelate_hotspot_only=False
                    )
                else:
                    import cupy as cp
                    import time

                    # assemble to be checked index lists
                    idx_list = []
                    for j in range(len(idcs_to_check)):
                        idx_list.append(zap_idx_e_opt[:idx_in_result_list - 1] + [idcs_to_check[j]])
                    idx_list = np.array(idx_list)

                    # load data on GPU
                    e = cp.empty(shape=e_all_coil_pos_scaled.shape, dtype=cp.float32)
                    subsampling_idcs = cp.empty(shape=subsampled_ele_idcs.shape, dtype=cp.int32)
                    index_lists = cp.empty(shape=idx_list.shape, dtype=cp.int32)
                    e[:] = cp.asarray(e_all_coil_pos_scaled[:], dtype=cp.float32)
                    subsampling_idcs[:] = cp.asarray(subsampled_ele_idcs[:], dtype=cp.int32)
                    index_lists[:] = cp.asarray(idx_list[:], dtype=cp.int32)

                    # execute optimization
                    res_all = workhorses.roi_elmt_wise_corr(
                            idx_list=index_lists,
                            array=e,
                            ele_idx_1=subsampling_idcs,
                            decorrelate_hotspot_only=False,
                            backend=cp
                    )
                    idx_best = cp.argmin(res_all).get()
                    crit[idx_in_result_list] = res_all[idx_best].get()
            except NameError:
                print("[Error] opt/get_optimal_coil_positions: Could not access precomputed "
                      "target optimal e-field values from FIM. Will skip computing 'fim_correlation' metric.")
        elif criterion == "rowvec_diff":
            # "rowvec_diff" metric will not be parallelized: no "workhorse_partial" will be prepared,
            # instead the result is computed immediately as it is a simple direct matrix lookup.
            # Must have the results of at least two stimulations already.
            # (either provided via 'zap_idx_opt' or computed in the preparatory function)
            if idx_of_last_result >= 1:
                try:
                    idx_best, crit[idx_in_result_list] = rowvec_diff(
                            candidate_coil_idcs=idcs_to_check,
                            selected_coil_idcs=zap_idx_e_opt[:idx_in_result_list],
                            efields_diff_mat=efields_diff_mat_full,
                    )
                except NameError:
                    print("[Error] opt/get_optimal_coil_positions: Could not access precomputed "
                          "e-field difference matrix. Will skip computing 'rowvec_diff' metric.")
        else:
            raise NameError(f"criterion: {criterion} not implemented")

        # parallel execution of prepared workers
        if workhorse_partial is not None:
            # Create the list of lists the optimization criterion is supposed to be computed for:
            # - first part of the sub-lists is always the sequence of already determined optimal positions
            # - all of these lists differ only in their last element: which are the indices from "idcs_to_check"
            idx_list = []
            for j in range(len(idcs_to_check)):
                idx_list.append(zap_idx_e_opt[:idx_in_result_list - 1] + [idcs_to_check[j]])

            idx_list_chunks = pynibs.compute_chunks(idx_list, n_cpu)
            res = pool.map(workhorse_partial, idx_list_chunks)

            # extract best solution (multiple objectives)
            if type(res[0]) is tuple:

                for j in range(len(res)):
                    if j == 0:
                        res_all = np.vstack(res[j]).transpose()
                    else:
                        res_all = np.vstack((res_all, np.vstack(res[j]).transpose()))

                # filter nans # TODO: not to 1e6 -> max of each opt criterion (column)
                res_all[np.isnan(res_all)] = 1e6
                res_all[res_all == 0] = 1e-6

                # normalize both optimization criteria to [0, 1]
                res_all = (res_all - np.min(res_all, axis=0)) / (np.max(res_all, axis=0) - np.min(res_all, axis=0))

                # weight optimization criteria
                res_all = res_all * metrics_weights

                # find the best solution with the lowest sum
                res_all_sum = np.sum(res_all, axis=1)
                idx_best = np.argmin(res_all_sum)
                crit[idx_in_result_list] = res_all_sum[idx_best]

            # extract best solution (single objective)
            else:
                # filter nans
                res = np.concatenate(res)
                res[np.isnan(res)] = 1e6

                # find best solution
                idx_best = np.argmin(res)
                crit[idx_in_result_list] = res[idx_best]

        if verbose:
            print(f" >>> Best index: {idcs_to_check[idx_best]}, criterion: {crit[idx_in_result_list]}")

        next_optimal_coil_idx = idcs_to_check[idx_best]
        if "fim" in criterion:
            next_optimal_stim_mso = np.round(fim_didt_scaling[next_optimal_coil_idx] / fim_mso_didt_conversion_factor)
        else:
            next_optimal_stim_mso = None
        zap_idx_e_opt[idx_in_result_list] = next_optimal_coil_idx
        idcs_to_check.remove(next_optimal_coil_idx)

        if fn_out_hdf5 is not None:
            # save results
            with h5py.File(fn_out_hdf5, "a") as f:
                try:
                    del f["criterion"]
                except (RuntimeError, KeyError):
                    f.create_dataset("criterion", data=crit)

                try:
                    f.create_dataset(f"zap_index_list/{idx_in_result_list}", data=zap_idx_e_opt[:idx_in_result_list])
                except (RuntimeError, KeyError):
                    if overwrite:
                        del f[f"zap_index_list/{idx_in_result_list}"]
                        f.create_dataset(f"zap_index_list/{idx_in_result_list}",
                                         data=zap_idx_e_opt[:idx_in_result_list])
                    else:
                        print(f"Could not write zap_index_list/{idx_in_result_list}. Dataset already exists.")

                if fn_coilpos_hdf5 is not None:
                    try:
                        del f["centers"], f["m0"], f["m1"], f["m2"]
                    except (RuntimeError, KeyError):
                        if overwrite:
                            f.create_dataset("centers", data=centers[zap_idx_e_opt[idx_in_result_list], :])
                            f.create_dataset("m0", data=m0[zap_idx_e_opt[idx_in_result_list], :])
                            f.create_dataset("m1", data=m1[zap_idx_e_opt[idx_in_result_list], :])
                            f.create_dataset("m2", data=m2[zap_idx_e_opt[idx_in_result_list], :])

    pool.close()
    pool.join()

    if fn_out_hdf5 is None:
        if "fim" not in criterion:
            return zap_idx_e_opt, crit
        else:
            return zap_idx_e_opt, crit, next_optimal_stim_mso
    else:
        with h5py.File(fn_out_hdf5, "a") as f:
            try:
                # f.create_dataset(f"zap_index_list", data=np.array(zap_idx_e_opt[-1])[:, np.newaxis])
                f.create_dataset(f"zap_index_list", data=np.array(zap_idx_e_opt)[:, np.newaxis])
            except (RuntimeError, KeyError):
                if overwrite:
                    del f[f"zap_index_list"]
                    # f.create_dataset(f"zap_index_list", data=np.array(zap_idx_e_opt[-1])[:, np.newaxis])
                    f.create_dataset(f"zap_index_list", data=np.array(zap_idx_e_opt)[:, np.newaxis])
                else:
                    print(f"Could not write zap_index_list. Dataset already exists.")

            if fn_coilpos_hdf5 is not None:
                m0_opt_reshaped = np.hstack((m0[zap_idx_e_opt[-1], :],
                                             np.zeros((len(zap_idx_e_opt[-1]), 1)))).T[:, np.newaxis, :]
                m1_opt_reshaped = np.hstack((m1[zap_idx_e_opt[-1], :],
                                             np.zeros((len(zap_idx_e_opt[-1]), 1)))).T[:, np.newaxis, :]
                m2_opt_reshaped = np.hstack((m2[zap_idx_e_opt[-1], :],
                                             np.zeros((len(zap_idx_e_opt[-1]), 1)))).T[:, np.newaxis, :]
                centers_opt_reshaped = np.hstack((centers[zap_idx_e_opt[-1], :],
                                                  np.ones((len(zap_idx_e_opt[-1]), 1)))).T[:, np.newaxis, :]
                matsimnibs = np.concatenate((m0_opt_reshaped,
                                             m1_opt_reshaped,
                                             m2_opt_reshaped,
                                             centers_opt_reshaped), axis=1)

                try:
                    f.create_dataset("centers", data=centers[zap_idx_e_opt[-1], :])
                    f.create_dataset("m0", data=m0[zap_idx_e_opt[-1], :])
                    f.create_dataset("m1", data=m1[zap_idx_e_opt[-1], :])
                    f.create_dataset("m2", data=m2[zap_idx_e_opt[-1], :])
                    f.create_dataset("matsimnibs", data=matsimnibs)
                except (RuntimeError, KeyError):
                    if overwrite:
                        del f["centers"], f["m0"], f["m1"], f["m2"]
                        f.create_dataset("centers", data=centers[zap_idx_e_opt[-1], :])
                        f.create_dataset("m0", data=m0[zap_idx_e_opt[-1], :])
                        f.create_dataset("m1", data=m1[zap_idx_e_opt[-1], :])
                        f.create_dataset("m2", data=m2[zap_idx_e_opt[-1], :])
                        f.create_dataset("matsimnibs", data=matsimnibs)
                    else:
                        print(f"Could not write centers, m0, m1, m2 ... Dataset already exists.")


def online_optimization(fn_subject_hdf5, fn_roi_ss_indices_hdf5, fn_out_hdf5, fn_stimsites_hdf5, e_matrix, mep,
                        mesh_idx, roi_idx, n_zaps_init=3, criterion_init="mc_rows", criterion="coverage", n_cpu=4,
                        threshold=0.8, weights=None, eps0=0.01, eps0_dist=1, exponent=5, perc=99,
                        n_refit=0, fun=pynibs.sigmoid, verbose=True):
    """
    Performs virtual online optimization to determine the congruence factor. After an initial set of coil positions,
    the algorithm iteratively optimizes the next coil position based on the virtually measured MEP data.

    Parameters
    ----------
    fn_subject_hdf5 : str
        Filename of subject .hdf5 file.
    fn_roi_ss_indices_hdf5 : str
        Filename of .hdf5 file containing the element indices of the subsampled ROI in ``f["roi_indices"]``.
    e_matrix : np.ndarray of float
        (n_zaps, n_ele) Electric field matrix.
    mep : np.ndarray of float
        (n_zaps) Motor evoked potentials for every stimulation.
    fn_out_hdf5 : str
        Filename of .hdf5 output file containing the coil positions and the congruence factor maps for every iteration.
    fn_stimsites_hdf5 : str
        Filename of the .hdf5 file containing the stimulation sites in "centers", "m0", "m1", "m2".
    mesh_idx : int
        Mesh index.
    roi_idx : int
        ROI index.
    n_zaps_init : int, default: 3
        Number of initial samples optimized using optimization criterion specified in ``criterion_init``.
    criterion_init : str, default: "mc_rows"
        Optimization criterion for which the initial samples are optimized (e.g. "mc_rows", "svd", ...).
    criterion : str, default: "coverage"
        Optimization criterion for which the online optimization is performed (e.g. "coverage", "mc_rows", "svd", ...).
    n_cpu : int, optional, dfault: 4
        Number of CPU cores to use.
    threshold : float, default: 0.1
        Threshold between [0 ... 1] of the maximal congruence factor. Elements where c > threshold * max(c)
        are included in the online optimization to select the next optimal coil position.
    weights : list of float [2], default: [0.5, 0.5]
        Weights of optimization criteria in case of multiple goal functions (e.g. fim_svd). Higher weight means higher
        importance for the respective criteria. By default, both optimization criteria are weighted equally [0.5, 0.5].
    eps0 : float, default: 0.01
        First error threshold to terminate the online optimization. The normalized root mean square deviation is
        calculated between the current and the previous solution. If the error is lower than eps0 for 3 times in a row,
        the online optimization terminates and returns the results.
    eps0_dist : float, default: 1
        Second error threshold to terminate the online optimization. The geodesic distance in mm of the hotspot is
        calculated between the current and the previous solution. If the error is lower than eps0_dist for 3 times
        in a row, the online optimization terminates and returns the results.
    exponent : float, default: 5
        Exponent the congruence factor map is scaled c**exponent.
    perc : float, default: 99
        Percentile the congruence factor map is normalized (between 0 and 100).
    n_refit : int, default: 0
        Number of refit iterations. No refit is applied if ``n_refit=0``.
    fun : function object, default: pynibs.linear
        Function to use to determine the congruence factor (e.g. pynibs.linear, pynibs.sigmoid, ...).
    verbose : bool, default: True
        Plot output messages.

    Returns
    -------
    <file> .hdf5 file
        Results output file containing the coil positions and the congruence factor maps for every iteration.

    """
    if weights is None:
        weights = [0.5, 0.5]
    print("Starting online congruence factor optimization:")
    print("===============================================")
    print(f" > fn_subject_hdf5:          {fn_subject_hdf5}")
    print(f" > fn_roi_ss_indices_hdf5:   {fn_roi_ss_indices_hdf5}")
    print(f" > fn_stimsites_hdf5:        {fn_stimsites_hdf5}")
    print(f" > fn_out_hdf5:              {fn_out_hdf5}")
    print(f" > e_matrix:                 shape: {e_matrix.shape}")
    print(f" > mep:                      shape: {mep.shape}")
    print(f" > mesh_idx:                 {mesh_idx}")
    print(f" > roi_idx:                  {roi_idx}")
    print(f" > n_zaps_init:              {n_zaps_init}")
    print(f" > criterion_init:           {criterion_init}")
    print(f" > criterion:                {criterion}")
    print(f" > n_cpu:                    {n_cpu}")
    print(f" > threshold:                {threshold}")
    print(f" > weights:                  {weights}")
    print(f" > eps0:                     {eps0}")
    print(f" > eps0_dist:                {eps0_dist}")
    print(f" > exponent:                 {exponent}")
    print(f" > perc:                     {perc}")
    print(f" > n_refit:                  {n_refit}")
    print(f" > fun:                      {fun.__name__}")
    print(f" > verbose:                  {verbose}")
    print("")

    zap_idx = dict()
    c = dict()

    # load subject
    if verbose:
        print(f"Loading subject")
    subject = pynibs.load_subject(fn_subject_hdf5)

    # load ROI and perform subsampling
    if verbose:
        print(f"Loading ROI and perform subsampling")
    roi = pynibs.load_roi_surface_obj_from_hdf5(subject.mesh[mesh_idx]['fn_mesh_hdf5'])[roi_idx]
    con = roi.node_number_list
    points = roi.node_coord_mid

    with h5py.File(fn_roi_ss_indices_hdf5, "r") as f:
        ele_idx_ss = f["roi_indices"][:]

    # e-fields
    if verbose:
        print(f"Loading electric field from regression.hdf5")
    n_ele = e_matrix.shape[1]

    # loading coil positions and create matsimnibs [4x4] matrices
    with h5py.File(fn_stimsites_hdf5, "r") as f:
        centers_all = f["centers"][:]
        m0_all = f["m0"][:]
        m1_all = f["m1"][:]
        m2_all = f["m2"][:]

    coil_mean = dict()
    current_dict = dict()

    for i in range(centers_all.shape[0]):
        coil_mean[str(i)] = np.hstack((m0_all[i, :][:, np.newaxis],
                                       m1_all[i, :][:, np.newaxis],
                                       m2_all[i, :][:, np.newaxis],
                                       centers_all[i, :][:, np.newaxis]))
        current_dict[str(i)] = 1

    # determine initial number of optimal samples
    if verbose:
        print(f"Determine optimal coil positions for initial number of {n_zaps_init} samples using {criterion_init}")

    zap_idx_opt = pynibs.get_optimal_coil_positions(e_matrix=e_matrix,
                                                    ele_idx_1=ele_idx_ss,
                                                    ele_idx_2=None,
                                                    criterion=criterion_init,
                                                    n_stim=n_zaps_init,
                                                    fn_out_hdf5=None,
                                                    n_cpu=n_cpu,
                                                    zap_idx_opt=None,
                                                    metrics_weights=weights,
                                                    overwrite=False,
                                                    verbose=True)

    # determine initial c-factor map for all N (not existing in real life)
    if verbose:
        print(f"Determine reference c-factor map (N)")

    c_ref_n = pynibs.regress_data(elm_idx_list=np.arange(n_ele),
                                  e_matrix=e_matrix,
                                  mep=mep,
                                  zap_idx=None,
                                  fun=fun,
                                  n_refit=n_refit,
                                  n_cpu=n_cpu,
                                  con=con,
                                  return_fits=False,
                                  refit_discontinuities=True)

    ref_n = c_ref_n.flatten() ** exponent
    ref_n = ref_n / np.percentile(ref_n, perc)

    c_max_idx_N = np.argmax(c_ref_n)

    ##########################################################################
    #
    # Robot measures initial offline optimal coil positions and collects MEPs
    #
    ##########################################################################

    # determine initial c-factor map (after robot measured first offline optimal coil positions)
    if verbose:
        print(f"Determine initial c-factor map")

    c_init, p = pynibs.regress_data(elm_idx_list=np.arange(n_ele),
                                    e_matrix=e_matrix,
                                    mep=mep,
                                    zap_idx=zap_idx_opt,
                                    fun=fun,
                                    n_refit=n_refit,
                                    n_cpu=n_cpu,
                                    con=con,
                                    return_fits=True,
                                    refit_discontinuities=True)
    ref = c_init.flatten() ** exponent
    ref = ref / np.percentile(ref, perc)

    eps = [eps0 + 1 for _ in range(len(zap_idx_opt))]
    eps_n = [eps0 + 1 for _ in range(len(zap_idx_opt))]

    gdist = [eps0_dist + 1 for _ in range(len(zap_idx_opt))]
    gdist_n = [eps0_dist + 1 for _ in range(len(zap_idx_opt))]

    for i in range(len(zap_idx_opt)):
        zap_idx[str(i)] = zap_idx_opt[:(i + 1)]
        c[str(i)] = np.zeros(ref.shape)

    c[str(n_zaps_init - 1)] = c_init

    n_zaps = [i for i in range(1, n_zaps_init + 1)]

    # Start online optimization loop
    while not ((np.array(eps[-3:]) < eps0).all() and (np.array(gdist[-3:]) < eps0_dist).all()):

        if "fim" in criterion or "dist_" in criterion:
            # find elements with values greater than threshold
            mask_perc = ref >= threshold * np.max(ref)
            ele_idx_1 = np.where(mask_perc)[0]
            ele_idx_2 = ele_idx_ss

        else:
            ele_idx_1 = ele_idx_ss
            ele_idx_2 = ele_idx_ss

        # optimize coil positions for subset of ROI elements
        if verbose:
            print(f"Optimizing next coil position for ROI_1: {len(ele_idx_1)} / ROI_2: {len(ele_idx_2)} elements "
                  f"using {criterion}")

        n_zaps.append(n_zaps[-1] + 1)
        zap_idx_opt = pynibs.get_optimal_coil_positions(e_matrix=e_matrix,
                                                        ele_idx_1=ele_idx_1,
                                                        ele_idx_2=ele_idx_2,
                                                        criterion=criterion,
                                                        n_stim=n_zaps[-1],
                                                        fn_out_hdf5=None,
                                                        n_cpu=n_cpu,
                                                        zap_idx_opt=zap_idx_opt,
                                                        fim_fit_fun=fun,
                                                        regression_fit_parameters=p,
                                                        regression_cmap=ref,
                                                        metrics_weights=weights,
                                                        overwrite=False,
                                                        verbose=True)
        key = str(len(zap_idx_opt) - 1)
        zap_idx[key] = zap_idx_opt

        ##########################################################################
        #
        # Robot measures next optimal coil position
        #
        ##########################################################################

        # determine updated c-factor map
        if verbose:
            print(f"Determine c-factor map for {len(zap_idx_opt)} zaps")

        c[key], p = pynibs.regress_data(elm_idx_list=np.arange(n_ele),
                                        e_matrix=e_matrix,
                                        mep=mep,
                                        zap_idx=zap_idx_opt,
                                        fun=fun,
                                        n_refit=n_refit,
                                        n_cpu=n_cpu,
                                        con=con,
                                        return_fits=True,
                                        refit_discontinuities=True)
        arr = c[key].flatten() ** exponent
        arr = arr / np.percentile(arr, perc)

        ##########################################################################
        #
        # Plot updated c-factor map
        #
        ##########################################################################

        # determine NRMSD w.r.t. previous solution
        eps.append(pynibs.nrmsd(arr, ref))

        if verbose:
            print(f"NRMSD to previous solution: {eps[-1]}")

        # determine NRMSD w.r.t. global solution (not existing in real life)
        eps_n.append(pynibs.nrmsd(arr, ref_n))

        if verbose:
            print(f"NRMSD to global solution: {eps_n[-1]}")

        # determine geodesic distance w.r.t. previous solution
        nodes_dist, tris_dist = pynibs.geodesic_dist(nodes=points, tris=con, source=np.argmax(c[key]),
                                                     source_is_node=False)
        gdist.append(tris_dist[np.argmax(c[str(len(zap_idx_opt) - 2)])])

        if verbose:
            print(f"GDIST to previous solution: {gdist[-1]:.3f} mm")

        # determine geodesic distance w.r.t. global solution (not existing in real life)
        gdist_n.append(tris_dist[c_max_idx_N])

        if verbose:
            print(f"GDIST to global solution: {gdist_n[-1]:.3f} mm")

        # set current solution as ref
        ref = arr

    eps_n = np.array(eps_n)
    eps = np.array(eps)
    gdist_n = np.array(gdist_n)
    gdist = np.array(gdist)
    n_zaps = np.array(n_zaps)

    if verbose:
        print(f"Saving results to {fn_out_hdf5}")

    with h5py.File(fn_out_hdf5, "w") as f:
        f.create_dataset("nrmsd", data=eps_n)
        f.create_dataset("nrmsd_n_1", data=eps)
        f.create_dataset("gdist", data=gdist_n)
        f.create_dataset("gdist_n_1", data=gdist)
        f.create_dataset("n_zaps", data=n_zaps)
        f.create_dataset(f"c_ref", data=c_ref_n)

        for key in zap_idx:
            f.create_dataset(f"zap_index_lists/{key}", data=zap_idx[key])
            f.create_dataset(f"c/{key}", data=c[key])

            n_zaps_tmp = len(zap_idx[key])
            centers = np.zeros((n_zaps_tmp, 3))
            m0 = np.zeros((n_zaps_tmp, 3))
            m1 = np.zeros((n_zaps_tmp, 3))
            m2 = np.zeros((n_zaps_tmp, 3))
            current = np.zeros((n_zaps_tmp, 1))

            for i, j in enumerate(zap_idx[key]):
                centers[i, :] = coil_mean[str(j)][0:3, 3]
                m0[i, :] = coil_mean[str(j)][0:3, 0]
                m1[i, :] = coil_mean[str(j)][0:3, 1]
                m2[i, :] = coil_mean[str(j)][0:3, 2]
                current[i, 0] = current_dict[str(j)]

            f.create_dataset(f"centers/{key}", data=centers)
            f.create_dataset(f"m0/{key}", data=m0)
            f.create_dataset(f"m1/{key}", data=m1)
            f.create_dataset(f"m2/{key}", data=m2)
            f.create_dataset(f"current/{key}", data=current)

    # create geo .hdf5
    fn_geo_hdf5 = os.path.splitext(fn_out_hdf5)[0] + "_geo.hdf5"
    pynibs.write_geo_hdf5_surf(out_fn=fn_geo_hdf5,
                               points=points,
                               con=con,
                               replace=True,
                               hdf5_path='/mesh')

    # write xdmf file with optimal results
    if verbose:
        print(f"Creating .xdmf ...")

    pynibs.write_temporal_xdmf(hdf5_fn=fn_out_hdf5,
                               data_folder='c',
                               coil_center_folder="centers",
                               coil_ori_0_folder="m0",
                               coil_ori_1_folder="m1",
                               coil_ori_2_folder="m2",
                               coil_current_folder="current",
                               hdf5_geo_fn=fn_geo_hdf5,
                               overwrite_xdmf=True,
                               verbose=False)

    # plot results
    fn_plot_nrmsd = os.path.splitext(fn_out_hdf5)[0] + "_nrmsd.png"
    fn_plot_gdist = os.path.splitext(fn_out_hdf5)[0] + "_gdist.png"

    if verbose:
        print(f"Plotting results to {fn_plot_nrmsd}")

    sort_idx = np.argsort(n_zaps)
    n_zaps = n_zaps[sort_idx]
    eps_n = eps_n[sort_idx]
    eps = eps[sort_idx]

    # nrmsd (n vs N) error
    plt.plot(n_zaps[n_zaps_init:], eps_n[n_zaps_init:], color="r")

    # nrmsd (n vs n-1) error
    plt.plot(n_zaps[n_zaps_init:], eps[n_zaps_init:], color="b")

    # 5% error bar
    plt.plot(np.array([n_zaps[4], n_zaps[-1]]), np.array([0.05, 0.05]), "r--")

    # 1% error bar
    plt.plot(np.array([n_zaps[4], n_zaps[-1]]), np.array([0.01, 0.01]), "b--")

    plt.grid()
    plt.xlabel("n", fontsize=11)
    plt.ylabel("NRMSD", fontsize=11)
    plt.ylim([0, 0.2])
    # plt.xscale("log")
    plt.title("Convergence analysis of online optimization", fontsize=11)
    plt.legend(["n vs N", "n vs (n-1)"])
    plt.savefig(fn_plot_nrmsd)
    plt.close()

    # gdist (n vs N) error
    plt.plot(n_zaps[n_zaps_init:], gdist_n[n_zaps_init:], color="r")

    # gdist (n vs n-1) error
    plt.plot(n_zaps[n_zaps_init:], gdist[n_zaps_init:], color="b")

    # 1% error bar
    plt.plot(np.array([n_zaps[4], n_zaps[-1]]), np.array([1, 1]), "b--")

    plt.grid()
    plt.xlabel("n", fontsize=11)
    plt.ylabel("GDIST", fontsize=11)
    plt.title("Convergence analysis of online optimization", fontsize=11)
    plt.legend(["n vs N", "n vs (n-1)"])
    plt.savefig(fn_plot_gdist)
    plt.close()

    if verbose:
        print("DONE")


def calc_opt_gain_map(e_matrix_ref, e_matrix_opt, points, con, fn_out=None, threshold=0.75):
    """
    Calculates the gain map between a reference e_matrix (e.g. from random sampling) and an optimized sequence of
    electric fields for mapping.

    Parameters
    ----------
    e_matrix_ref : np.ndarray of float [n_ref, n_ele_roi]
        Electric field matrix of reference simulations. E-fields in ROI are in the rows.
        (n_ref does not have to match n_opt)
    e_matrix_opt : np.ndarray of float [n_opt, n_ele_roi]
        Electric field matrix of optimal simulations. E-fields in ROI are in the rows.
        (n_ref does not have to match n_opt)
    points : np.ndarray of float [n_points_roi, 3]
        Node coordinates of the ROI.
    con : np.ndarray of float [n_ele_roi, 3]
        Connectivity matrix of ROI surface.
    fn_out : str, optional, default: None
        Filename of .hdf5 and .xdmf file for plots with paraview. (Without file extension)
    threshold : float, optional, default: 0.75
        Threshold of correlation the focality is quantified by area.

    Returns
    -------
    focality_ref : np.ndarray of float [n_ele_roi, 3]
        Focality measure (area) of PSF in each element > threshold for reference case.
    focality_opt : np.ndarray of float [n_ele_roi, 3]
        Focality measure (area) of PSF in each element > threshold for optimal case.
    focality_dif : np.ndarray of float [n_ele_roi, 3]
        Difference between focality_opt and focality_ref quantifying absolute gain in mm^2.
        Values < 0 : Optimal solution has smaller PSF than reference if hotspot would be in this element.
        Values > 0 : Optimal solution has larger PSF than reference if hotspot would be in this element.
    <file> : .hdf5 and .xmdf
        Geo and data files for visualization in paraview.
    """
    assert e_matrix_ref.shape[1] == e_matrix_opt.shape[1], "e_matrix_ref and e_matrix_opt do not have the same number" \
                                                           "columns, i.e. elements."
    n_ele = e_matrix_ref.shape[1]

    # determine correlation matrices
    corr_matrix_ref = np.abs(np.corrcoef(e_matrix_ref.T)) ** 2
    corr_matrix_opt = np.abs(np.corrcoef(e_matrix_opt.T)) ** 2

    # determine element areas
    p1_tri = points[con[:, 0], :]
    p2_tri = points[con[:, 1], :]
    p3_tri = points[con[:, 2], :]
    area = 0.5 * np.linalg.norm(np.cross(p2_tri - p1_tri, p3_tri - p1_tri), axis=1)

    # calculate focality
    focality_ref = np.zeros(n_ele)
    focality_opt = np.zeros(n_ele)

    for i_ele in range(n_ele):
        focality_ref[i_ele] = np.sum(area[corr_matrix_ref[i_ele, :] > threshold])
        focality_opt[i_ele] = np.sum(area[corr_matrix_opt[i_ele, :] > threshold])

    focality_dif = focality_opt - focality_ref

    # export results for visualization in paraview
    if fn_out is not None:
        if not os.path.exists(os.path.split(fn_out)[0]):
            os.makedirs(os.path.split(fn_out)[0])

        pynibs.write_geo_hdf5_surf(out_fn=fn_out + "_geo.hdf5",
                                   points=points,
                                   con=con,
                                   replace=True,
                                   hdf5_path='/mesh')

        pynibs.write_data_hdf5_surf(data=[focality_ref, focality_opt, focality_dif],
                                    data_names=["focality_ref", "focality_opt", "focality_dif"],
                                    data_hdf_fn_out=fn_out + "_data.hdf5",
                                    geo_hdf_fn=fn_out + "_geo.hdf5",
                                    replace=True)

    return focality_ref, focality_opt, focality_dif


def optimal_coilplacement_region(e, fmri_stats, best_n=1, metric='dot', non_negative=False, pos_matrices=None,
                                 res_folder=None):
    """
    Identify the optimal coil placement regions based on given electric field (E-field) matrices and fMRI statistics.

    Parameters
    ----------
    e : np.ndarray
        The E-field matrix containing field strengths for various positions.
    fmri_stats : ndarray
        fMRI statistics used to identify optimal stimulation regions. The values are normalized to the maximum value.
    best_n : int, default: 1
        Number of top positions to identify.
    metric : str, default: 'dot'
        The evaluation metric to use.

        - 'dot' calculates the dot product,
        - 'cor' computes the correlation coefficient.
    non_negative : bool, optional
        If True, only considers non-negative fMRI statistics.
    pos_matrices : ndarray, optional
        Position matrices for each coil position.
    res_folder : str, optional
        Directory to save the results. If not specified, no files are saved.

    Returns
    -------
    best_coil_id : int
        N best coil ids, accoring to ``best_n``

    Raises
    ------
    ValueError
        If the specified metric is not recognized.

    Notes
    -----
    - The function normalizes the input E-field matrix and fMRI statistics for evaluation.
    - If `res_folder` is specified, visualizations of the results are saved to the directory.
    - The function supports saving and writing TMS navigator instrument marker files using `simnibs.localite`.
    """
    # Import localite utility to write TMS navigator instrument marker files
    from simnibs.utils.nnav import localite
    loc = localite()
    write_tms_navigator_im = loc.write

    # Normalize fMRI statistics
    fmri_stats /= fmri_stats.max()

    # Normalize E-field matrix
    e_max = e.max()
    e /= e_max

    # Handle negative fMRI statistics based on the non_negative parameter
    if non_negative:
        suffix = 'nonneg'
    else:
        fmri_stats[fmri_stats < 0] = 0
        suffix = 'full'

    # Calculate evaluation scores using the specified metric
    if metric == 'dot':
        ef_stats = np.dot(e, fmri_stats)  # Dot product
        suffix = f"dot_{suffix}"
        title = "np.dot(e_matrix, fmri_stats)"
    elif metric == 'cor':
        ef_stats = np.corrcoef(e, fmri_stats)[-1, :-1]  # Correlation coefficient
        suffix = f"cor_{suffix}"
        title = "np.corrcoef(e_matrix, fmri_stats)"
    else:
        raise ValueError("Unsupported metric. Use either 'dot' or 'cor'.")

    # Find the index of the best coil position and the top N positions
    nth_best_coil_pos = np.argsort(ef_stats)[-best_n:][::-1]

    # If a results folder is specified, plot and save the optimization results
    if res_folder is not None:
        def plot_placement_optimizations(stats, fn, title, n_elms, n_elms_nonneg):
            """
            This plots two images to visualize the optimzation metric across coil placements
            """
            # plot optim results
            plt.plot(stats)
            plt.suptitle(f'Optimization results')
            plt.title(f'n_elms ROI: {n_elms}, nonnegative elms: {n_elms_nonneg}')
            plt.xlabel("Coil placement candidate")
            plt.ylabel(title)
            plt.savefig(fn)
            plt.close()

            # plot another version with results normalized based on elements used
            plt.plot(stats / (stats != 0).sum())
            plt.suptitle(f'Optimization results - normalized to nonnegative elms')
            plt.title(f'n_elms ROI: {n_elms}, nonnegative elms: {n_elms_nonneg}')
            plt.xlabel("Coil placement candidate")
            plt.ylabel(title)
            plt.savefig(fn.replace('.png', '_normalized.png'))
            plt.close()

        optim_plot_fn = os.path.join(res_folder, f"coil_placements_{suffix}.png")
        plot_placement_optimizations(ef_stats, optim_plot_fn, title, e.shape[1], (fmri_stats > 0).sum())

    # If position matrices are provided, identify the best and N best positions
    if pos_matrices is not None:
        nth_opt_matsim = pos_matrices[:, :, nth_best_coil_pos]

        # Transpose the matrices for proper alignment
        nth_opt_matsim = np.transpose(nth_opt_matsim, axes=(1, 0, 2))

        # Save the best coil position to an HDF5 file
        with h5py.File(os.path.join(res_folder, f'opt_coil_pos_{metric}.hdf5'), "w") as f:
            f.create_dataset(name="matsimnibs", data=nth_opt_matsim[:, :, 0])

        # Write the instrument marker file for the top N positions
        write_tms_navigator_im(nth_opt_matsim, os.path.join(res_folder, f'opt_coil_pos_nth_{metric}.xml'),
                               names=[f'opt_{i:0>2}' for i in range(best_n)], overwrite=True)
        pynibs.create_stimsite_from_matsimnibs(os.path.join(res_folder, f'opt_coil_pos_nth_{metric}.hdf5'),
                                               nth_opt_matsim, overwrite=True, data=np.array(range(1, best_n + 1)),
                                               datanames='Best coil id')
    return nth_best_coil_pos
