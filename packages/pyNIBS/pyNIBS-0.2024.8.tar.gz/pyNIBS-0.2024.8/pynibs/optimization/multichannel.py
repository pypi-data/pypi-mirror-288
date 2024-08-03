"""
Functions to optimize single coil currents for multichannel TMS arrays.
"""
import numpy as np
from scipy.optimize import minimize


def get_score_raw(x, e, n_stim, n_ele, n_channel, x_opt=None, opt_target='elms'):
    """
    Compute score for e-efield cross correlations.
    Non-normalized score is returned, so you need to do sth like

    score = 1 / ((n_ele ** 2 - n_ele) / 2) * get_score()

    Parameters
    ----------
    x : np.ndarray of float
        (n_channel * n_stim_opt, ) Vector to scale channels for each.
    e : np.ndarray of float
        (n_ele*3, n_channels) E-field.
    n_stim : int
        Number of stimulations to compute score for.
    n_ele : int
        Number of elements.
    n_channel : int
        Number of channels.
    x_opt :  np.ndarray of float, optinonal
        (n_pre_opt,) Previously optimized channel currents.
    opt_target : str, default: 'elms'
        Optimization target. 'elms' for optimizing decorrelations of elements, 'stims' for stimulations.

    Returns
    -------
    score : float
        non-normalized score np.nansum(np.abs(np.triu(np.corrcoef(e_mag), k=1)))
    """
    if x_opt is None:
        currents_all_zaps_channels = np.reshape(x, (n_channel, n_stim))
    else:
        currents_all_zaps_channels = np.hstack((x_opt, np.reshape(x, (n_channel, n_stim - x_opt.shape[1]))))
    # currents_all_zaps_channels.shape = (n_chans, n_zaps)

    # determine total electric field (vector form)
    e_vec = np.matmul(e, currents_all_zaps_channels)  # e_vec.shape = (n_elems*3, n_zaps)
    # determine magnitude
    # for e_ in e_vec.T:
    #     a = np.linalg.norm(np.reshape(e_, (n_ele, 3)), axis=1)
    #     # e_.shape = (n_ele=3,)
    #     # np.reshape(e_, (n_ele, 3)).shape = (n_ele,3)
    #     # a.shape = (n_ele,)

    if e.ndim == 2:
        e_mag = np.vstack([np.linalg.norm(np.reshape(e_, (n_ele, 3)), axis=1) for e_ in e_vec.T]).T
    elif e.ndim == 3:
        e_mag = np.linalg.norm(e_vec, axis=1)
    else:
        raise ValueError
    # e_mag.shape = (n_ele, n_zaps)

    # determine average correlation coefficient
    # r_avg = 1/((n_ele**2-n_ele)/2) * np.sum(np.abs(np.triu(np.corrcoef(e_mag), k=1)))
    if opt_target == 'elms':
        r_sum = np.nansum(np.abs(np.triu(np.corrcoef(e_mag), k=1)))
    elif opt_target == 'stims':
        r_sum = np.nansum(np.abs(np.triu(np.corrcoef(e_mag.T), k=1)))
    else:
        raise ValueError("opt_target has to be 'elms' or 'stims'")

    return r_sum


def get_score_raw_single_channel(x, e, x_opt=None):
    """
    Compute score for e-efield cross correlations.
    Non-normalized score is returned, so you need to do sth like

    score = 1 / ((n_ele ** 2 - n_ele) / 2) * get_score()

    Parameters
    ----------
    x : np.ndarray of float
        (n_placements, ) selection of coil placements.
    e : np.ndarray of float
        (n_ele*3, n_channels) E-field.
    x_opt :  np.ndarray of float, optinonal
        (n_pre_opt,) Previously optimized channel currents.

    Returns
    -------
    score : float
        non-normalized score np.nansum(np.abs(np.triu(np.corrcoef(e_mag), k=1)))
    """
    # x = ((x / x.max()) * e.shape[0]-1).astype(int)
    if x_opt is not None:
        x = np.hstack((x_opt, x))
    x = x.astype(int)
    e_mag = e[x, :]

    # determine average correlation coefficient
    # r_avg = 1/((n_ele**2-n_ele)/2) * np.sum(np.abs(np.triu(np.corrcoef(e_mag), k=1)))
    # a = np.abs(np.triu(np.corrcoef(e_mag.T), k=1))

    r_avg = np.nansum(np.abs(np.triu(np.corrcoef(e_mag.T), k=1)))
    return r_avg


def optimize_currents(e, n_stim, currents_prev=None, seed=None,
                      maxiter=200, method='SLSQP', opt_target='elms', verbose=False):
    """
    Optimize the currents for a multichannel TMS array by minimizing e-fields cross-correlation.

    Parameters
    ----------
    e : np.ndarray of float
        (n_elms * 3, n_channel) or (n_elms, 3, n_channel). E in ROI for currents = 1.
    n_stim : int
        Number of stimulations.
    currents_prev : np.ndarray of float, optional
        (n_channels, n_stims_prev) Previous currents to append to.
    seed : int, optional
        Seed for random number generator.
    maxiter : int, default=200
        Max iterations of the optimization.
    method : str, default: 'SLSQP'
        Optimization method.
    verbose : bool, default: False
        Print additional information.
    opt_target : str, default: 'elms'
        Optimization target. 'elms' for optimizing decorrelations of elements, 'stims' for stimulations.

    Returns
    -------
    currents : np.ndarray
        (n_channels, n_stims) The optimized currents to drive the multichannel array.
    score : float
        Final score of the solution.
    """
    if e.ndim == 2:
        n_channel = e.shape[1]
        n_ele = int(e.shape[0] / 3)
    elif e.ndim == 3:
        n_channel = e.shape[2]
        n_ele = int(e.shape[0])
    else:
        raise ValueError

    if currents_prev is None:
        n_stim_opt = n_stim
    else:
        n_stim_opt = n_stim - currents_prev.shape[1]

        if n_stim_opt <= 0:
            raise ValueError("N_stim has to be larger than already optimized optimal values!")

    # initial guess for currents for all channels * stimulations
    if seed is not None:
        np.random.seed(seed)
    x0 = (np.random.rand(n_channel * n_stim_opt) * 2) -1
    # print(x0[:5])
    if verbose:
        print(f"n_ele: {n_ele}, n_channels: {n_channel}, n_stims: {n_stim}")

    # optimization algorithm
    res = minimize(get_score_raw,
                   args=(e, n_stim, n_ele, n_channel, currents_prev, opt_target),
                   x0=x0,
                   method=method,
                   options={'disp': False, 'maxiter': maxiter},
                   bounds=[(-1, 1) for _ in range(len(x0))],
                   tol=1e-6)
    # print(res.fun, res.success, res.message)

    if currents_prev is None:
        currents = np.reshape(res.x, (n_channel, n_stim))
    else:
        currents = np.hstack((currents_prev, np.reshape(res.x, (n_channel, n_stim - currents_prev.shape[1]))))
    if opt_target == 'elms':
        score = 1 / ((n_ele ** 2 - n_ele) / 2) * res.fun
    elif opt_target == 'stims':
        score = 1 / ((n_stim ** 2 - n_stim) / 2) * res.fun
    else:
        raise ValueError("opt_target has to be 'elms' or 'stims'")

    return currents, score, res


def optimize_currents_single_channel(e, n_stim, currents_prev=None, seed=None,
                                     maxiter=200, method='SLSQP', verbose=False):
    """
    Optimize the coil placement selection for a single channel e-field set minimizing e-fields cross-correlation.

    Parameters
    ----------
    e : np.ndarray of float
        (n_elms3, n_placements).
    n_stim : int
        Number of stimulations.
    currents_prev : np.ndarray of float, optional
        (n_channels, n_stims_prev) Previous currents to append to.
    seed : int, optional
        Seed for random number generator.
    maxiter : int, default=200
        Max iterations of the optimization.
    method : str, default: 'SLSQP'
        Optimization method.
    verbose : bool, default: False
        Print additional information.

    Returns
    -------
    currents :  np.ndarray
        (n_channels, n_stims) The optimized currents to drive the multichannel array.
    score : float
        Final score of the solution.
    """
    n_placements = e.shape[0]
    n_ele = e.shape[1]

    if currents_prev is None:
        n_stim_opt = n_stim
    else:
        n_stim_opt = n_stim - currents_prev.shape[0]

        if n_stim_opt <= 0:
            raise ValueError("N_stim has to be larger than already optimized optimal values!")

    # initial guess for currents for all channels * stimulations
    if seed is not None:
        np.random.seed(seed)
    x0 = np.random.randint(0, n_placements, n_stim_opt)
    if verbose:
        print(f"n_ele: {n_ele}, n_placements: {n_placements}, n_stims: {n_stim}")

    # optimization algorithm
    res = minimize(get_score_raw_single_channel,
                   args=(e, currents_prev),
                   x0=x0,
                   method=method,
                   options={'disp': False, 'maxiter': maxiter},
                   bounds=[(0, n_placements) for _ in range(len(x0))])

    # if currents_prev is None:
    #     currents = np.reshape(res.x, (n_placements, n_stim))
    # else:
    #     currents = np.hstack((currents_prev, np.reshape(res.x, (n_placements, n_stim - currents_prev.shape[1]))))

    score = 1 / ((n_ele ** 2 - n_ele) / 2) * res.fun
    # score = res.fun

    return res.x, score


def get_score(x, e, n_stim, n_ele, n_channel, x_opt=None):
    """
    Normalize the score by the number of elements.

    Parameters
    ----------
    x : np.ndarray of float
        (n_channel * n_stim_opt, ) Vector to scale channels for each.
    e : np.ndarray of float
        (n_ele*3, n_channels) E-field.
    n_stim : int
        Number of stimulations to compute score for.
    n_ele : int
        Number of elements.
    n_channel : int
        Number of channels.
    x_opt :  np.ndarray of float, optinonal
        (n_pre_opt,) Previously optimized channel currents.

    Returns
    -------
    score : float
        The normalized score.
    """
    score_raw = get_score_raw(x, e, n_stim, n_ele, n_channel, x_opt)
    return 1 / ((n_ele ** 2 - n_ele) / 2) * score_raw
