"""
Functions to select optimal stimulation conditions based on the estimated y (i.e., MEPs in MEP studies).
"""

import numpy as np


def get_fim_sample(fun, x, p):
    """
    Get Fisher Information Matrix of one single sample.

    Parameters
    ----------
    fun : callable
        Callable the fisher information matrix is calculated for. The sample is passed as the first argument.
    x : float
        Sample passed to function.
    p : dict
        Dictionary containing the parameter estimates. The keys are the parameter names of fun.

    Returns
    -------
    fim_matrix : np.ndarray of float
        (n_params, n_params) Fisher information matrix.
    """

    # read function arguments
    params = p.keys()

    # determine gradient of function w.r.t. parameters using forward approximation
    dfdp = np.zeros(len(params))

    for i, para in enumerate(params):
        # copy original params dict
        p_dp = dict()

        for pa in params:
            p_dp[pa] = p[pa]

        # perturb parameter
        dp = p[para] / 1000
        p_dp[para] = p[para] + dp

        # determine gradient with forward approximation
        dfdp[i] = (fun(x, **p_dp) - fun(x, **p)) / dp

    fim_matrix = np.outer(dfdp, dfdp)

    return fim_matrix


def get_det_fim(x, fun, p, fim_matrix):
    """
    Updates the Fisher Information Matrix and returns the negative determinant based on the sample x.
    It is a score how much information the additional sample yields.

    Parameters
    ----------
    fun : callable
        Callable defined in interval [0, 1].
    x : float
        Single sample location (interval [0, 1]).
    p : dict
        Dictionary containing the parameter estimates. The keys are the parameter names of fun.
    fim_matrix : np.ndarray of float
        (n_params, n_params) Fisher Information Matrix.

    Returns
    -------
    det : float
        Determinant of the Fisher Information Matrix after adding sample x.
    """
    fim_matrix_sample = fim_matrix + get_fim_sample(fun=fun, x=x, p=p)
    sign, logdet = np.linalg.slogdet(fim_matrix_sample)

    return -sign * np.exp(logdet)


def init_fim_matrix(fun, x, p):
    """
    Initializes the Fisher Information Matrix based on the samples given in x.

    Parameters
    ----------
    fun : callable
        Callable defined in interval [0, 1].
    x : np.ndarray of float
        Initial sample locations (interval [0, 1]).
    p : dict
        Dictionary containing the parameter estimates. The keys are the parameter names of fun.

    Returns
    -------
    fim_matrix : np.ndarray of float [n_params x n_params]
        Fisher Information Matrix.
    """
    fim_matrix = np.zeros((len(p), len(p)))

    for x_i in x:
        fim_matrix += get_fim_sample(fun=fun, x=x_i, p=p)

    return fim_matrix


def get_optimal_sample_fim(fun, p, x=None):
    """
    Determines optimal location of next sample by maximizing the determinant of the Fisher Information Matrix.

    Parameters
    ----------
    fun : callable
        Callable (interval [0, 1]).
    x : np.ndarray of float, optional
        Previous sample locations (interval [0, 1]).
    p : dict
        Dictionary containing the parameter estimates. The keys are the parameter names of fun.

    Returns
    -------
    x_opt : float
        Optimal location of next sample (interval [0, 1]).
    """
    # initialize fim matrix with initial samples
    if x is None:
        fim_matrix = np.zeros((len(p), len(p)))
    else:
        fim_matrix = init_fim_matrix(fun=fun, x=x, p=p)

    # run optimization
    # res = minimize(fun=get_det_fim,
    #                method="trust-constr",
    #                bounds=((0, 1),),
    #                x0=np.array([0.5]),
    #                args=(fun, p, fim_matrix),
    #                options={"finite_diff_rel_step": 0.05, "xtol": 0.01})

    # res = minimize(fun=get_det_fim,
    #                 method="SLSQP",
    #                 x0=np.array([0.5]),
    #                 bounds=((0, 1),),
    #                 args=(fun, p, fim_matrix),
    #                 options={'disp': None, "eps": 0.001, "ftol": 1e-12}) #,
    # return res.x[0]

    x_bf = np.linspace(0, 1, 200)
    det = np.zeros(len(x_bf))
    for i in range(len(x_bf)):
        det[i] = get_det_fim(x=x_bf[i], fun=fun, p=p, fim_matrix=fim_matrix)

    x_opt = x_bf[np.argmin(det)]

    return x_opt
