import os
import copy
import pynibs
import numpy as np
import _pickle as pickle
import multiprocessing.pool
from _functools import partial
from scipy.interpolate import LinearNDInterpolator


def workhorse_interp(idx_list, interp, params):
    """
    Single core workhorse to interpolate data.

    Parameters
    ----------
    idx_list : np.nfarray or list of float
        (n_interpolations) Indices in params array where the interpolation has to be performed
        (subset of all indices in params array).
    interp : instance of scipy.interpolate
        Interpolator instance.
    params : np.ndarray of float
        (N_interpolations, N_params) Array containing the parameters the function is evaluated
        (total array with all parameters).

    Returns
    -------
    res : np.ndarray of float
        (n_interpolations) Interpolation results (subset params[idx_list, :]).
    """
    return interp(params[idx_list, 0], params[idx_list, 1], params[idx_list, 2]) / 2.2  # 2.2


def load_cell_model(fn_csv):
    """
    Load interpolation points of the mean field model from the specified CSV file.

    Parameters
    ----------
    fn_csv : str
        Fully qualified path to the CSV containing the interpolation points of the mean field model.

    Returns
    -------
    scipy.interpolate.LinearNDInterpolator
    interpolation points 'theta'
    interpolation points 'gradient'
    """
    cell_simulation_data = [np.genfromtxt(fn_csv, delimiter=',')]

    thresholds = cell_simulation_data[-1][:, 2]
    theta = cell_simulation_data[-1][:, 1]
    rel_grad = cell_simulation_data[-1][:, 0]

    return LinearNDInterpolator(list(zip(theta, rel_grad)), thresholds), theta, rel_grad


# TODO: implement the creation of a response interpolator
def _create_model_response_interpolator(fn_model_csv):
    return LinearNDInterpolator([(0, 0), (0, 1), (1, 0), (1, 1)], [1, 1, 1, 1], fill_value=1)


def calc_e_threshold(layerid, theta, gradient=None, mep=None, neuronmodel="sensitivity_weighting",
                     waveform="biphasic", e_thresh_subject=None):
    """
    Determine sensitivity map of electric field.

    Parameters
    ----------
    layerid : str
        Choose from the neocortical layers (e.g. "L1", "L23", "L4", "L5", "L6") to load data for.
    theta : np.ndarray
        (N_stim, N_ele) Theta angle (matrix) of electric field with respect to surface normal. In degrees [0 .. 180].
    gradient : np.ndarray, optional
        (N_stim, N_ele) Electric field gradient (matrix) between layer 1 and layer 6. Optional, the neuron mean field
        model is more accurate when provided. Percent [-100 .. 100].
    mep : np.ndarray of float, optional
        (N_stim, ) MEP data (required in case of "IOcurve" approach (neuronmodel)
    neuronmodel : str, default: 'sensitivity_weighting'
        Select neuron model to modify the electric field values

        - "sensitivity_weighting": normalize threshold map and divide raw e-field by it.
        - "threshold_subtract": subtract mean threshold from electric field.
        - "threshold_binary": assign e-field a binary value to predict MEPs
            (False -> below threshold, True, above threshold).
        - "IOcurve": subtract value read from precomputed neuron IO curve from electric field.
        - "cosine" : # TODO: document
    waveform : str, default: 'biphasic'
        Waveform of TMS pulse:

        - "monophasic"
        - "biphasic"
    e_thresh_subject : float, optional
        Subject specific stimulation threshold in V/m. Typically between 60 ... 80 V/m.
        Only used for 'threshold_subtract' and '"threshold_binary",'

    Returns
    -------
    e_sens : np.ndarray
        (N_stim, N_ele) Electric field sensitivity maps.
    """
    # load neuron models
    ####################################################################################################################
    models_folder = os.path.join(pynibs.__datadir__, "neuron", "models")
    interp_folder = os.path.join(pynibs.__datadir__, "neuron", "interpolators")
    scaling_factor = None

    if waveform == "monophasic":
        models = {
            "L23": os.path.join(models_folder, "L23_PC_cADpyr_monophasic_v1.csv"),
            "L4SBC": os.path.join(models_folder, "L4_SBC_monophasic_v1.csv"),
            "L4NBC": os.path.join(models_folder, "L4_NBC_monophasic_v1.csv"),
            "L4LBC": os.path.join(models_folder, "L4_LBC_monophasic_v1.csv"),
            "L5": os.path.join(models_folder, "L5_TTPC2_cADpyr_monophasic_v1.csv")
        }

        models_io = {
            "L23": os.path.join(interp_folder, "L23_biphasic_recruitment_rate_interpolator_inverse.pkl"),
            "L5": os.path.join(interp_folder, "L5_biphasic_recruitment_rate_interpolator_inverse.pkl")
        }
    elif waveform == "biphasic":
        models = {
            "L23": os.path.join(models_folder, "L23_PC_cADpyr_biphasic_v1.csv"),
            "L4SBC": os.path.join(models_folder, "L4_SBC_biphasic_v1.csv"),
            "L4NBC": os.path.join(models_folder, "L4_NBC_biphasic_v1.csv"),
            "L4LBC": os.path.join(models_folder, "L4_LBC_biphasic_v1.csv"),
            "L5": os.path.join(models_folder, "L5_TTPC2_cADpyr_biphasic_v1.csv")
        }

        models_io = {
            "L23": os.path.join(interp_folder, "L23_biphasic_recruitment_rate_interpolator_inverse.pkl"),
            "L5": os.path.join(interp_folder, "L5_biphasic_recruitment_rate_interpolator_inverse.pkl")
        }
    else:
        raise NotImplementedError(f"Specified waveform {waveform} not implemented.")

    if neuronmodel in ["threshold_subtract", "threshold_binary", "sensitivity_weighting", "cosine"]:
        interp, thetas, rel_gradients = load_cell_model(models[layerid])

        if neuronmodel in ["sensitivity_weighting", "cosine"]:
            scaling_factor = interp(0, 0)
            if e_thresh_subject is not None:
                print(f"e_thresh_subject={e_thresh_subject} is not used for neuronmodel={neuronmodel}")

        elif e_thresh_subject is not None:
            scaling_factor = np.mean(interp(np.linspace(0, 180, 181),
                                            np.zeros(181))) / e_thresh_subject

        else:
            # Scaling factor between electric field thresholds of model and subject specific e-field thresholds.
            # scaling_factor = e_threshold_model / e_threshold_subject
            # Model thresholds are higher than subject specific thresholds (typically in a range between 2..3)
            # average thresholds between 0 and 180° at E_grad = 0
            scaling_factor = 1

    elif neuronmodel == "IOcurve":
        _, thetas, rel_gradients = load_cell_model(models[layerid])

        # TODO: not implemented yet
        if not os.path.exists(models_io[layerid]):
            raise NotImplementedError("[neuron_regression] Pickl files containing the response interpolators "
                                      f"do not exist (path checked: {models_io[layerid]}) and their creation "
                                      "is not implemented yet.")
            # interp = _create_model_response_interpolator(models[layerid])
            # with open(models_io[layerid], 'wb') as f:
            #    pickle.dump(interp, f)
        else:
            with open(models_io[layerid], 'rb') as f:
                interp = pickle.load(f)

    else:
        raise NotImplementedError(f"Specified neuronmodel {neuronmodel} not implemented.")

    # bound observed values to min/max values available in the model
    ####################################################################################################################
    theta_bound = theta
    theta_bound[np.where(theta > np.max(thetas))] = np.max(thetas)
    theta_bound[np.where(theta < np.min(thetas))] = np.min(thetas)

    if gradient is None:
        gradient_bound = np.zeros(theta.shape)
    else:
        gradient_bound = gradient
        gradient_bound[np.where(gradient > np.max(rel_gradients))] = np.max(rel_gradients)
        gradient_bound[np.where(gradient < np.min(rel_gradients))] = np.min(rel_gradients)

    # Determine approach specific effective electric field
    ####################################################################################################################
    if neuronmodel in ["threshold_subtract", "threshold_binary", "sensitivity_weighting"]:
        e_thres = interp(theta_bound, gradient_bound) / scaling_factor

    elif neuronmodel == "cosine":
        e_thres = scaling_factor * 1 / np.abs(np.cos(theta_bound / np.pi))

    elif neuronmodel == "IOcurve":
        # normalize MEPs between [0, 0.999]
        mep_threshold = 2
        mep_cropped = copy.deepcopy(mep)
        mep_cropped[mep > mep_threshold] = mep_threshold
        mep_norm = mep_cropped / (mep_threshold * 1.05)

        # calculate expected electric field at observed MEP
        params = np.zeros((theta.shape[0] * theta.shape[1], 3))
        params[:, 0] = gradient_bound.flatten()
        params[:, 1] = theta_bound.flatten()
        params[:, 2] = np.repeat(mep_norm, theta.shape[1])

        idx = np.arange(params.shape[0])
        idx_chunked = pynibs.compute_chunks(list(idx), multiprocessing.cpu_count())

        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        workhorse_partial = partial(workhorse_interp, interp=interp, params=params)
        res = np.hstack(pool.map(workhorse_partial, idx_chunked))
        e_thres = np.reshape(res, theta.shape)
        pool.close()
        pool.join()

    else:
        raise NotImplementedError

    return e_thres


def calc_e_effective(e, layerid, theta, gradient=None, neuronmodel="sensitivity_weighting", mep=None,
                     waveform="biphasic", e_thresh_subject=None):
    """
    Determines the effective electric field using a neuron mean field model.
    The electric field magnitude is 'subtracted' by the threshold map (in V/m), yielding the
    effective electric field (e_eff).

    Parameters
    ----------
    e : np.ndarray
        (N_stim, N_ele) Electric field (matrix).
    layerid : str
        Choose from the neocortical layers (e.g. "L1", "L23", "L4", "L5", "L6").
    theta : np.ndarray
        (N_stim, N_ele) Theta angle (matrix)  of electric field with respect to surface normal.
    gradient : np.ndarray, optional
        (N_stim, N_ele) Electric field gradient (matrix)  between layer 1 and layer 6. Optional, the neuron mean field
        model is more accurate when provided.
    neuronmodel : str, default: 'threshold'
        Select neuron model to modify the electric field values

        - "sensitivity_weighting": normalize threshold map and divide raw e-field by it.
        - "threshold_subtract": subtract mean threshold from electric field.
        - "threshold_binary": assign e-field a binary value to predict MEPs
          (False -> below threshold, True, above threshold).
        - "IOcurve": subtract value read from precomputed neuron IO curve from electric field.
    mep : np.ndarray of float [N_stim], optional
        MEP data (required in case of "IOcurve" approach (neuronmodel)).
    waveform : str, default: 'biphasic'
        Waveform of TMS pulse:

        - "monophasic"
        - "biphasic"
    e_thresh_subject : float, optional
        Subject specific stimulation threshold in V/m. Typically, between 60 ... 80 V/m.
        This is not used for sensitivity_weighting and

    Returns
    -------
    e_eff : np.ndarray
        Effective electric field (matrix) [N_stim x N_ele] the regression analysis can be performed with.
    """
    # determine sensitivity map
    e_thres = calc_e_threshold(layerid=layerid,
                               theta=theta,
                               gradient=gradient,
                               neuronmodel=neuronmodel,
                               mep=mep,
                               waveform=waveform,
                               e_thresh_subject=e_thresh_subject)

    if neuronmodel == "threshold_subtract":
        e_eff = e - e_thres
    elif neuronmodel == "threshold_binary":
        e_eff = e > e_thres
    elif neuronmodel in ["sensitivity_weighting", "cosine"]:
        e_eff = e / e_thres
    else:
        e_eff = np.zeros(e.shape)

    return e_eff
