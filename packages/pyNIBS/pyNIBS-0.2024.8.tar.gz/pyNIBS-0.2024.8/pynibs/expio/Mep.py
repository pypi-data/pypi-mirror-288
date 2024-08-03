import re
import json
import pylab
import warnings
import datetime
import numpy as np
import pandas as pd
from lmfit import Model
import scipy.io as spio
from scipy.signal import butter, lfilter
import matplotlib.pyplot as plt

import pynibs

from pynibs.expio.fit_funs import sigmoid, sigmoid4_log, linear, exp, exp0

try:
    import biosig
except ImportError:
    # print("WARNING: Please install biosig from pynibs/pkg/biosig folder!")
    pass
np.seterr(over="ignore")


def get_mep_virtual_subject_TVS(x, p1=-5.0818, p2=-2.4677, p3=3.6466, p4=0.42639, p5=1.6665,
                                mu_y_add=10 ** -5.0818, mu_y_mult=-0.9645334, mu_x_add=0.68827324,
                                sigma_y_add=1.4739 * 1e-6, k=0.39316, sigma2_y_mult=2.2759 * 1e-2,
                                sigma2_x_add=2.3671 * 1e-2,
                                subject_variability=False, trial_variability=True):
    print("get_mep_virtual_subject_TVS() got renamed to get_virtual_mep_tvs()")
    raise NotImplementedError


def get_virtual_mep_tvs(x, p1=-5.0818, p2=-2.4677, p3=3.6466, p4=0.42639, p5=1.6665,
                        mu_y_add=10 ** -5.0818, mu_y_mult=-0.9645334, mu_x_add=0.68827324,
                        sigma_y_add=1.4739 * 1e-6, k=0.39316, sigma2_y_mult=2.2759 * 1e-2,
                        sigma2_x_add=2.3671 * 1e-2,
                        subject_variability=False, trial_variability=True):
    """
    Creates random mep data using the 3 variability source model from [1]_.
    There are typos in the paper but the code seems to be correct.
    Originally from S. Goetz: https://github.com/sgoetzduke/Statistical-MEP-Model .
    Rewritten from MATLAB to Python by Konstantin Weise.

    Parameters
    ----------
    x : np.ndarray of float
        (n_x) Normalized stimulator intensities [0 ... 1].
    p1 : float, default: -5.0818
        First parameter of sigmoidal hilltype function.
    p2 : float, default: 4.5323
        Second parameter of sigmoidal hilltype function.
    p3 : float, default: 3.6466
        Third parameter of sigmoidal hilltype function.
    p4 : float, default: 0.42639
        Fourth parameter of sigmoidal hilltype function.
    p5 : float, default: 1.6665
        Fifth parameter of sigmoidal hilltype function.
    mu_y_add : float, default:  10**-5.0818
        Mean value of additive y variability source.
    mu_y_mult : float, default: -0.9645334
        Mean value of multiplicative y variability source.
    mu_x_add : float, default: -0.68827324
        Mean value of additive x variability source.
    sigma_y_add : float, default: 1.4739*1e-6
        Standard deviation of additive y variability source.
    k : float, default: 0.39316
        Shape parameter of generalized extreme value distribution.
    sigma2_y_mult : float, default: 2.2759*1e-2
        Standard deviation of multiplicative y variability source.
    sigma2_x_add : float, default: 2.3671*1e-2
        Standard deviation of additive x variability source.
    subject_variability : bool, default: False
        Choose if shape parameters from IO curve are sampled from random distributions to model subject variability.
        This does not influence the trial-to-trial variability.
    trial_variability : bool, default: True
        Enable or disable trial-to-trial variability. Disabling it will result in ideal IO curves w/o noise.

    Returns
    -------
    mep : np.ndarray of float
        (n_x) Motor evoked potential values in mV.

    References
    ----------
    .. [1] Goetz, S. M., Alavi, S. M., Deng, Z. D., & Peterchev, A. V. (2019).
       Statistical Model of Motor-Evoked Potentials.
       IEEE Transactions on Neural Systems and Rehabilitation Engineering, 27(8), 1539-1545.
    """
    x = x * 100
    n_x = len(x)
    mu_y_add = 10 ** p1

    # determine variabilities
    if trial_variability:
        e_y_mult = 10 ** np.random.normal(loc=mu_y_mult, scale=np.sqrt(sigma2_y_mult), size=n_x)
        e_x_add = 10 ** np.random.normal(loc=mu_x_add, scale=np.sqrt(sigma2_x_add), size=n_x)

        # determine generalized value distribution of additive y variability
        p_e_y_add = pynibs.generalized_extreme_value_distribution(x=np.linspace(5e-6, 1e-4, 100000),
                                                                  mu=mu_y_add, sigma=sigma_y_add, k=k)

        # sample from generalized value distribution to determine additive y variability
        e_y_add = np.random.choice(np.linspace(5e-6, 1e-4, 100000), p=p_e_y_add / np.sum(p_e_y_add), size=n_x)

    else:
        e_y_mult = np.ones(n_x) * 10 ** mu_y_mult
        e_x_add = np.ones(n_x) * 10 ** mu_x_add
        e_y_add = np.ones(n_x) * mu_y_add

    x_prime = 2.224 * 1e-16 + x - 10 ** p5 + e_x_add
    x_prime[x_prime < 0] = 2.224 * 1e-16

    mep = e_y_add + np.exp(np.log(10) * (e_y_mult - 7 + (p2 + 7) / (1 + (10 ** p3) / (x_prime ** (10 ** p4)))))
    mep = mep * 1000

    return mep


def get_mep_virtual_subject_DVS(x, x0=0.5, r=10, amp=1, sigma_x=0, sigma_y=0, y0=1e-2, seed=None, rng=None):
    """
    Creates random mep data using the 2 variability source model from Goetz et al. 2014 [1]_ together with a standard 3
    parametric sigmoid function.

    Parameters
    ----------
    x : np.ndarray of float
        (n_x) Normalized stimulator intensities [0 ... 1].
    x0 : float, default: 0.5
        Location of turning point sigmoidal function.
    r : float, default: 0.25
        Steepness of sigmoidal function.
    amp : float, default: 1.0
        Saturation amplitude of sigmoidal function.
    sigma_x : float, default: 0.1
        Standard deviation of additive x variability source.
    sigma_y : float, default: 0.1
        Standard deviation of additive y variability source.
    y0 : float, default: 1e-2
        y-offset.
    seed : int, optional
        Seed to use.
    rng : numpy._generator.Generator, optional
        An already initialized random number generator that will be used instead of intializing a new one with seed.

    Returns
    -------
    mep : np.ndarray of float
        (n_x) Motor evoked potential values

    References
    ----------
    .. [1] Goetz, S. M., Luber, B., Lisanby, S. H., & Peterchev, A. V. (2014).
       A novel model incorporating two variability sources for describing motor evoked potentials.
       Brain stimulation, 7(4), 541-552.
    """
    if not isinstance(x, np.ndarray):
        x = np.atleast_1d(x)
    if type(rng) is np.random._generator.Generator:
        default_rng = rng
    else:
        if type(rng) is not type(None):
            print("[get_mep_virtual_subject_DVS] Invalid argument: get_mep_virtual_subject_DVS. Using numpy default_rng"
                  f" with seed={seed}")

        default_rng = np.random.default_rng(seed=seed)

    if not isinstance(x, np.ndarray):
        x = np.array([x])

    n_x = len(x)

    if sigma_x > 0:
        e_x_add = default_rng.normal(loc=0, scale=sigma_x, size=n_x)
    else:
        e_x_add = np.zeros(n_x)

    if sigma_y > 0:
        e_y_add = default_rng.normal(loc=0, scale=sigma_y, size=n_x)
    else:
        e_y_add = np.zeros(n_x)

    x_pert = x + e_x_add

    mep = 10 ** (sigmoid4_log(x=x_pert, x0=x0, r=r, amp=amp, y0=y0) + e_y_add)

    return mep


class Mep:
    """
    Mep object.

    Attributes
    ----------
    fun : function
        Function type to fit data with (``pynibs.sigmoid`` / ``pynibs.exp`` / ``pynibs.linear``).
    fun_sig : function
        Best fitting equivalent sigmoidal function (added by ``self.add_sigmoidal_bestfit()``).
    popt : np.ndarray of float
        (N_para) Fitted optimal function parameters.
    popt_sig : np.ndarray of float
        (3) Best fitting parameters ``x0``, ``r``, and ``amp`` of equivalent sigmoidal function.
    copt :  np.ndarray of float
        (N_para, N_para) covariance matrix of fitted parameters.
    pstd : np.ndarray of float
        (N_para) Standard deviation of fitted parameters.
    fit : object instance
        Gmodel object instance of parameter fit.
    x_limits : np.ndarray of float
        (2) Minimal and maximal value of intensity data.
    y_limits : np.ndarray of float
        (2) Minimal and maximal value of mep data.
    mt : float
        Motor threshold (MEP > 50 uV), evaluated from fitted curve, added after fitting.
    """

    # TODO: implement list of already fitted function types and their indices in self.fit[] for plot function. \
    #       condition name as attribute
    def __init__(self, intensities, mep, intensity_min_threshold=None, mep_min_threshold=None):
        """
        Initialize ``Mep`` object.

        Parameters
        ----------
        intensities : np.ndarray of float
            (N_mep) Intensities of TMS stimulator corresponding to measured MEP amplitudes.
        mep : np.ndarray of float
            (N_mep) MEP amplitudes in [V] measured during TMS.
        intensity_min_threshold : float, optional
            Minimum user defined intensity (values below it will be filtered out).
        mep_min_threshold : float, optional
            Minimum user defined MEP amplitude (values below it will be filtered out).
        """

        self.intensities_orig = intensities
        self.mep_orig = mep
        self.cvar = []
        self.popt = []
        self.pstd = []
        self.fun = sigmoid
        self.fun_sig = sigmoid
        self.popt_sig = []
        self.fit = []
        self.best_fit_idx = None
        self.mt = None
        self.constraints = None

        if intensity_min_threshold is None:
            intensity_min_threshold = -np.inf

        if mep_min_threshold is None:
            mep_min_threshold = -np.inf

        # filter negative meps or too small intensities
        mmask = np.where(self.mep_orig >= mep_min_threshold)
        self.intensities = self.intensities_orig[mmask]  # + np.random.randn(intensities.size)*1e-6
        self.mep = self.mep_orig[mmask]

        imask = np.where(self.intensities >= intensity_min_threshold)
        self.intensities = self.intensities[imask]  # + np.random.randn(intensities.size)*1e-6
        self.mep = self.mep[imask]

        self.x_limits = np.array([np.min(self.intensities), np.max(self.intensities)])
        self.y_limits = np.array([np.min(self.mep), np.max(self.mep)])

        # sort data in ascending order
        idx_sort = np.argsort(self.intensities)
        self.intensities = self.intensities[idx_sort]
        self.mep = self.mep[idx_sort]

    def fit_mep_to_function(self, p0=None):
        """
        Fits MEP data to function. The algorithm tries to fit the function first to a sigmoid, then to an
        exponential and finally to a linear function.

        Parameters
        ----------
        p0: np.ndarray of float, optional
            Initial guess of parameter values.

        Notes
        -----
        Additional attributes:

        Mep.popt : np.ndarray of float
            (N_para) Fitted optimal function parameters.
        Mep.copt : np.ndarray of float
            (N_para, N_para) Covariance matrix of fitted parameters.
        Mep.pstd : np.ndarray of float
            (N_para) Standard deviation of fitted parameters.
        Mep.fun : function
            Function mep data was fitted with.
        Mep.fit : object instance
            Gmodel object instance of parameter fit.
        Mep.mt : float
            Motor threshold (MEP > 50 uV).
        """
        if p0 is None:
            p0 = []

        delta = 0.4

        try_to_fit = True
        i_try = 1
        while try_to_fit:
            # unsuccessful fit
            if i_try == 4:
                break

            if i_try == 1:
                self.fun = sigmoid
                gmodel = Model(self.fun)
                self.fit = gmodel.fit(self.mep, x=self.intensities, x0=p0[0], r=p0[1], amp=p0[2])

            if i_try == 2:
                self.fun = exp
                gmodel = Model(self.fun)
                self.fit = gmodel.fit(self.mep, x=self.intensities, x0=p0[0], r=p0[1], y0=p0[2])

            if i_try == 3:
                self.fun = linear
                gmodel = Model(self.fun)
                self.fit = gmodel.fit(self.mep,
                                      x=self.intensities,
                                      m=(np.max(self.mep) - np.min(self.mep)) /
                                        (np.max(self.intensities) - np.min(self.intensities)),
                                      n=0)
                i_try = i_try + 1

            print('Fitting data to {} function ...'.format(str(self.fun.__name__)))

            # filter out unseccussful fit
            if self.fit.covar is None:
                i_try = i_try + 1
                print('Unsuccessful fit ... trying next function!')
                continue

            # get names of arguments of function
            argnames = self.fun.__code__.co_varnames[1:self.fun.__code__.co_argcount]

            # read out optimal function parameters
            self.popt = []
            for i in range(len(argnames)):
                self.popt.append(self.fit.best_values[argnames[i]])

            self.popt = np.asarray(self.popt)
            self.cvar = self.fit.covar
            self.pstd = np.sqrt(np.diag(self.cvar))

            # re-fit if std of any parameter is > delta
            if ((self.pstd / self.popt) > delta).any() and i_try < 3:
                print(f'Unsuccessful fit ... relative STD of one parameter is > {delta * 100}% ... '
                      f'trying next function!')
                i_try = i_try + 1
                continue

            # successful fit
            if ((self.pstd / self.popt) <= delta).all():
                break

        # determine motor threshold considering a threshold of 50 uV
        self.calc_motor_threshold(threshold=0.05)

    def fit_mep_to_function_multistart(self, p0=None, constraints=None, fun=None):
        """
        Fits MEP data to function.

        Parameters
        ----------
        p0 :  np.ndarray of float, optional
            Initial guess of parameter values.
        constraints : dict, optional
            Dictionary with parameter names as keys and [min, max] values as constraints.
        fun : list of functions, optional
            Functions to incorporate in the multistart fit (e.g.
            [``pynibs.sigmoid``, ``pynibs.exp0``, ``pynibs.linear``]).

        Notes
        -----
        Add Attributes:

        Mep.popt : np.ndarray of float
            (N_para) Best fitted optimal function parameters.
        Mep.copt : np.ndarray of float
            (N_para, N_para) Covariance matrix of best fitted parameters.
        Mep.pstd : np.ndarray of float
            (N_para) Standard deviation of best fitted parameters.
        Mep.fun : function
            Function of best fit mep data was fitted with.
        Mep.fit : list of fit object instances
            Gmodel object instances of parameter fits.
        Mep.best_fit_idx : int
            Index of best function fit (``fit[best_fit_idx]``).
        Mep.constraints : dict
            Dictionary with parameter names as keys and [min, max] values as constraints.
        """
        if fun is None:
            fun = [sigmoid, exp0, linear]
        if p0 is None:
            p0 = []

        self.constraints = constraints

        self.fit = []
        p0_passed = []
        argnames = []

        # fun = [sigmoid, exp0, linear]
        # # fun = [sigmoid]
        pstd_mean = np.zeros(len(fun))
        aic = np.zeros(len(fun))

        for i in range(len(fun)):
            if fun[i] == sigmoid:
                p0_passed = p0
            elif fun[i] == exp:
                p0_passed = p0  # (p0[0], p0[1])
            elif fun[i] == exp0:
                p0_passed = (p0[0], p0[1])
            elif fun[i] == linear:
                p0_passed = ((np.max(self.mep) - np.min(self.mep)) /
                             (np.max(self.intensities) - np.min(self.intensities)),
                             1)

            print('Fitting data to {} function ...'.format(str(fun[i].__name__)))
            self.fit.append(self.run_fit_multistart(fun[i],
                                                    x=self.intensities,
                                                    y=self.mep,
                                                    p0=p0_passed,
                                                    constraints=constraints))

            if self.fit[i] is not None:
                if self.fit[i].covar is not None:
                    pstd_mean[i] = np.mean(np.sqrt(np.diag(self.fit[i].covar)))
                else:
                    pstd_mean[i] = None

                aic[i] = self.fit[i].aic
                print("\t> found optimal parameters")
            else:
                pstd_mean[i] = None
                aic[i] = np.inf
                print("\t> failed")

            # get names of arguments of function
            argnames.append(fun[i].__code__.co_varnames[1:fun[i].__code__.co_argcount])

        # determine best model by aic (Akaike information criterion)
        self.best_fit_idx = int(np.argmin(aic))

        print("====================================")
        print("> Best fit: {} function".format(str(fun[self.best_fit_idx].__name__)))
        print("\n")

        # read out optimal function parameters from best fit
        self.popt = []
        for i in range(len(argnames[self.best_fit_idx])):
            self.popt.append(self.fit[self.best_fit_idx].best_values[argnames[self.best_fit_idx][i]])

        self.popt = np.asarray(self.popt)
        self.cvar = np.asarray(self.fit[self.best_fit_idx].covar)
        self.pstd = np.sqrt(np.diag(self.cvar))
        self.fun = fun[self.best_fit_idx]

        # determine motor threshold considering a threshold of 50 uV
        self.calc_motor_threshold(threshold=0.05)

    def run_fit_multistart(self, fun, x, y, p0, constraints=None, verbose=False, n_multistart=100):
        """
        Run multistart approach to fit data to function. ``n_multistart`` optimizations are performed based on random
        variations of the initial guess parameters ``p0``. The fit with the lowest AIC (Akaike information criterion),
        i.e. best fit is returned as gmodel fit instance.

        Parameters
        ----------
        fun : function
            Function mep data has to be fitted with.
        x : np.ndarray of float
            (N_data) Independent variable the data is fitted on.
        y : np.ndarray of float
            (N_data) Dependent data the curve is fitted through.
        p0 : np.ndarray of float or list of float
            Initial guess of parameter values.
        constraints : dict, optional
            Dictionary with parameter names as keys and [min, max] values as constraints.
        verbose : bool, default: False
            Show output messages.
        n_multistart : int, default: 100
            Number of repeated optimizations with different starting points to perform.

        Returns
        -------
        fit : object instance
            Gmodel object instance of best parameter fit with lowest parameter variance.
        """

        argnames = fun.__code__.co_varnames[1:fun.__code__.co_argcount]
        gmodel = Model(fun)

        if constraints:
            for i in range(len(list(constraints.keys()))):
                gmodel.set_param_hint(list(constraints.keys())[i],
                                      value=(constraints[list(constraints.keys())[i]][0] +
                                             constraints[list(constraints.keys())[i]][1]) / 2,
                                      min=constraints[list(constraints.keys())[i]][0],
                                      max=constraints[list(constraints.keys())[i]][1])

        n_p = len(argnames)
        fit = []

        # run n_s curve fits with random starting points
        for i in range(n_multistart):

            params = dict()

            # generate random samples of between constraint min and max or start points between 0 ... 2*p0
            for j in range(n_p):
                if constraints and argnames[j] in list(constraints.keys()):
                    params[argnames[j]] = np.random.random_sample(1) \
                                          * (constraints[argnames[j]][1] - constraints[argnames[j]][0]) \
                                          + constraints[argnames[j]][0]
                else:
                    params[argnames[j]] = p0[j] * (1 + (2 * np.random.random_sample(1) - 1))

            # set underflow and overflow warnings to exceptions, to be able to catch them
            old_np_settings = np.seterr(under='raise', over='raise')
            try:
                if fun == sigmoid:
                    fit.append(gmodel.fit(y, x=x, x0=params['x0'], r=params['r'], amp=params['amp'], verbose=False))
                if fun == exp:
                    fit.append(gmodel.fit(y, x=x, x0=params['x0'], r=params['r'], y0=params['y0'], verbose=False))
                if fun == exp0:
                    fit.append(gmodel.fit(y, x=x, x0=params['x0'], r=params['r'], verbose=False))
                if fun == linear:
                    fit.append(gmodel.fit(y, x=x, m=params['m'], n=params['n'], verbose=False))

            except (ValueError, FloatingPointError):
                if verbose:
                    print('\t Single fit failed in multistart optimization ... skipping value!')
                fit.append(None)

            # reset warnings to previous state
            np.seterr(**old_np_settings)

        # select best fit with lowest aic (Akaike information criterion) and return it
        pstd = []
        aic = []
        for i in range(n_multistart):
            if fit[i] is not None:
                if fit[i].covar is None:
                    pstd.append(float('Inf'))
                    aic.append(float('Inf'))
                else:
                    pstd.append(np.mean(np.sqrt(np.diag(fit[i].covar))))
                    aic.append(fit[i].aic)
            else:
                pstd.append(float('Inf'))
                aic.append(float('Inf'))
        idx = int(np.argmin(np.asarray(aic)))

        return fit[idx]

    def calc_motor_threshold(self, threshold):
        """
        Determine motor threshold of stimulator depending on MEP threshold given in [mV].

        Parameters
        ----------
        threshold : float
            Threshold of MEP amplitude in [mV].

        Notes
        -----
        Add Attributes:

        Mep.mt : float
            Motor threshold for given MEP threshold.
        """

        self.mt = np.nan

        # sample MEP curve very fine in given range
        intensities = np.linspace(self.x_limits[0], self.x_limits[1], 1000)
        mep_curve = self.eval_opt(intensities)
        i_threshold_idx = np.where(mep_curve > threshold)[0]

        if i_threshold_idx.any():
            self.mt = intensities[i_threshold_idx[0]]

    def plot(self, label, sigma=3, plot_samples=True, show_plot=False, fname_plot='', ylim=None, ylabel=None,
             fontsize_axis=10, fontsize_legend=10, fontsize_label=10, fontsize_title=10, fun=None):
        """
        Plotting mep data and fitted curve together with uncertainties.
        If ``fun == None`, the optimal function is plotted.

        Parameters
        ----------
        label : str
            Plot title.
        sigma : float, default: 3
            Factor of standard deviations the uncertainty of the fit is plotted with.
        plot_samples : bool, default: True
            Plot sampling curves of the fit in the uncertainty interval.
        show_plot : bool, default: False
            Show or hide plot window (``TRUE`` / ``FALSE``).
        fname_plot : str, default: ''
            Filename of plot showing fitted data (with .png extension).
        ylim : list of float, optional
            (2) Min and max values of y-axis.
        fontsize_axis : int, default: 10
            Fontsize of axis numbers.
        fontsize_legend : int, default: 10
            Fontsize of Legend labels.
        fontsize_label : int, default: 10
            Fontsize of axis labels.
        fontsize_title : int, default: 10
            Fontsize of title.
        fun : str, default: None
            Which function to plot (None, ``sigmoid``, ``exp``, ``linear``).

        Returns
        -------
        <File> : .png file
            Plot of Mep data and fit (format: png).
        """
        p = []
        if show_plot or fname_plot:
            x_range = np.max(self.intensities) - np.min(self.intensities)
            x = np.linspace(np.min(self.intensities) - 0.0 * x_range, np.max(self.intensities) + 0.0 * x_range, 100)

            # plot random sampling curves
            if plot_samples:
                n_s = 100
                params = np.random.randn(n_s, self.popt.shape[0]) * self.pstd + self.popt
                for i in range(n_s):
                    pylab.plot(x, self.fun(x, *params[i, :]), 'k', linewidth=0.25)

            # plot raw data
            p.append(pylab.plot(self.intensities, self.mep, 'o', label='data', markersize=3))

            # plot fit if present
            if self.fit:
                if fun is not None:
                    assert fun in ['sigmoid', 'exp0', 'linear']
                    # assert order of self.fit is ['sigmoid', 'linear', 'exp0']
                    if fun == 'sigmoid':
                        argnames = sigmoid.__code__.co_varnames[1:sigmoid.__code__.co_argcount]
                        opt = []
                        for i in range(len(argnames)):
                            opt.append(self.fit[0].best_values[argnames[i]])

                        opt = np.asarray(opt)
                        y = sigmoid(x, *opt)
                    elif fun == 'exp0':
                        argnames = exp0.__code__.co_varnames[1:exp0.__code__.co_argcount]
                        opt = []
                        for i in range(len(argnames)):
                            opt.append(self.fit[1].best_values[argnames[i]])

                        opt = np.asarray(opt)
                        y = exp0(x, *opt)
                    elif fun == 'linear':
                        argnames = linear.__code__.co_varnames[1:linear.__code__.co_argcount]
                        opt = []
                        for i in range(len(argnames)):
                            opt.append(self.fit[2].best_values[argnames[i]])

                        opt = np.asarray(opt)
                        y = linear(x, *opt)
                    else:
                        raise ValueError("{} is unknown. One of [None, 'sigmoid', 'exp', 'linear'")
                else:
                    y = self.fun(x, *self.popt)
                p.append(pylab.plot(x, y, 'r', label='fit ({})'.format(self.fun.__name__)))
                if ylim is not None:
                    pylab.ylim(ylim[0], ylim[1])
                pylab.title(label, size=fontsize_title)

                if sigma != 0:
                    y_min, y_max = self.eval_uncertainties(x, sigma=sigma)
                    p.append(pylab.fill_between(x, y_max, y_min, facecolor=[0.8, 0.8, 0.8],
                                                interpolate=True, label='std'))

            pylab.grid(color=[0.6, 0.6, 0.6], linestyle='--', linewidth=0.25)
            pylab.legend(loc=2, fontsize=fontsize_legend)
            pylab.xticks(size=fontsize_axis)
            pylab.yticks(size=fontsize_axis)
            pylab.xlabel(r'Stimulator intensity [A/$\mu$s]', size=fontsize_label)

            if ylabel is not None:
                pylab.ylabel(ylabel, size=fontsize_label)

            if show_plot:
                pylab.show()

            if fname_plot:
                pylab.savefig(fname_plot, format='png', bbox_inches='tight', pad_inches=0.01 * 4, dpi=600)

            pylab.close()

    def eval_uncertainties(self, x, sigma=1):
        """
        Evaluating approximated uncertainty interval around fitted distribution.

        Parameters
        ----------
        x : np.ndarray of float
            (N_x) Function values where uncertainty is evaluated.
        sigma : float, default: 1
            Standard deviation of parameters taken into account when evaluating uncertainty interval.

        Returns
        -------
        y_min : np.ndarray of float
            (N_x) Lower bounds of y-values.
        y_max : np.ndarray of float
            (N_x) Upper bounds of y-values.
        """

        if not self.fit:
            raise Exception('Please fit function first before evaluating uncertainties!')

        p = [np.array([self.popt[i] - sigma * self.pstd[i], self.popt[i] + sigma * self.pstd[i]])
             for i in range(self.popt.shape[0])]

        para_combinations = pynibs.get_cartesian_product(p)

        y = np.zeros((x.shape[0], para_combinations.shape[0]))

        for i in range(para_combinations.shape[0]):
            y[:, i] = self.eval(x, para_combinations[i, :])

        y_min = np.min(y, axis=1)
        y_max = np.max(y, axis=1)

        return y_min, y_max

    def eval_opt(self, x):
        """
        Evaluating fitted function with optimal parameters in points x.

        Parameters
        ----------
        x : np.ndarray of float
            (N_x) Function arguments.

        Returns
        -------
        y : np.ndarray of float
            (N_x) Function values.
        """

        y = self.fun(x, *self.popt)
        return y

    def eval(self, x, p):
        """
        Evaluating fitted function with optimal parameters in points x.

        Parameters
        ----------
        x: np.ndarray of float
            (N_x) Function arguments.
        p: tuple of float
            Function parameters.

        Returns
        -------
        y: np.ndarray of float
            (N_x) Function values.
        """

        y = self.fun(x, *p)
        return y

    def eval_fun_sig(self, x, p):
        """
        Evaluating optimally fitted sigmoidal function with optimal parameters in points x.

        Parameters
        ----------
        x: np.ndarray of float
            (N_x) Function arguments.
        p: tuple of float
            Function parameters.

        Returns
        -------
        y: np.ndarray of float
            (N_x) Function values.
        """

        y = self.fun_sig(x, *p)
        return y


def read_biosig_emg_data(fn_data, include_first_trigger=False, type="cfs"):
    """
    Reads EMG data from a biosig file.

    Parameters
    ----------
    fn_data : str
        Path to the biosig file.
    include_first_trigger : bool, default: False
        Whether to include the first trigger event in the data (default: False).
    type : str, default: 'cfs'
        Type of the biosig file.

    Returns
    -------
    emg_data : np.ndarray
        (num_sweeps, num_channels, samples_per_sweep) EMG data with shape.
    time_diff_list : list
        Time differences between trigger events in seconds.
    num_sweeps : int
        Number of sweeps in the EMG data.
    num_channels : int
        Number of channels in the EMG data.
    samples_per_sweep : int
        Number of samples per sweep in the EMG data.
    sampling_rate : int
        Sampling rate of the EMG data.
    """
    try:
        import biosig
    except ImportError:
        ImportError("Please install biosig from pynibs/pkg/biosig folder!")
        return

    if type == "cfs":  # TODO: also move the TXT reader here?
        cfs_fn = fn_data
        cfs_header = json.loads(biosig.header(cfs_fn))
        cfs_emg = biosig.data(cfs_fn)

        num_sweeps = cfs_header["NumberOfSweeps"]
        num_channels = cfs_emg.shape[1]

        total_num_samples = cfs_header["NumberOfSamples"]
        samples_per_sweep = int(total_num_samples / num_sweeps)
        sampling_rate = int(cfs_header["Samplingrate"])

        # get timestamps
        tms_pulse_timedelta = datetime.timedelta()
        # get hour, minute and second
        time_mep_list = []
        time_diff_list = []
        trigger_event_idcs = []
        if include_first_trigger:
            trigger_event_idcs.append(0)
            time_diff_list.append(0)
            time_mep_list.append(
                datetime.datetime.strptime(
                    cfs_header["EVENT"][0]["TimeStamp"], '%Y-%b-%d %H:%M:%S'
                )
                -
                datetime.timedelta(
                    seconds=float(cfs_header["EVENT"][0]["POS"])
                )
            )

        # convert time string into integer
        for event in cfs_header["EVENT"]:
            date = datetime.datetime.strptime(event["TimeStamp"], '%Y-%b-%d %H:%M:%S')

            # we are interested in the tms pulse time, so add it to ts
            date += tms_pulse_timedelta
            time_mep_list.append(date)
            time_diff_list.append((date - time_mep_list[0]).total_seconds())

            # compute indices in data block corresponding to the events
            if event["TYP"] == "0x7ffe":
                trigger_event_idcs.append(
                    round(event["POS"] * cfs_header["Samplingrate"])
                )

        num_sweeps = min(num_sweeps, len(trigger_event_idcs))

        emg_data = np.zeros((num_sweeps, num_channels, samples_per_sweep), dtype=np.float32)

        for c_idx in range(num_channels):
            # Use emg data starting from the index of the first trigger event
            # assumptions:
            # - after an initial offset all emg data were captured consecutively
            # - the first emg data frame may be captured without an explicit TMS
            #   tigger (eg. by checking the "write to disk" option)
            # - if we had dropouts in between the emg data block (not just at the
            #   beginning) we would need to adhere to the entire trigger_event_indices
            #   list.
            emg_data[:, c_idx, :] = np.reshape(
                cfs_emg[trigger_event_idcs[0]:, c_idx],
                (num_sweeps, samples_per_sweep)
            )

        return emg_data, time_diff_list, num_sweeps, num_channels, samples_per_sweep, sampling_rate


def get_mep_elements(mep_fn, tms_pulse_time, drop_mep_idx=None, cfs_data_column=0, channels=None, time_format="delta",
                     plot=False, start_mep=18, end_mep=35):
    """
    Read EMG data from CED .cfs or .txt file and returns MEP amplitudes.

    Parameters
    ----------
    mep_fn : string
        path to .cfs-file or .txt file (Signal export).
    tms_pulse_time : float
        Time in [s] of TMS pulse as specified in signal.
    drop_mep_idx : List of int or None, optional
        Which MEPs to remove before matching.
    cfs_data_column : int or list of int, default: 0
        Column(s) of dataset in cfs file. +1 for .txt.
    channels : list of str, optional
        Channel names.
    time_format : str, default: "delta"
        Format of mep time stamps in time_mep_lst to return.

        * ``"delta"`` returns list of datetime.timedelta in seconds.
        * ``"hms"`` returns datetime.datetime(year, month, day, hour, minute, second, microsecond).

    plot : bool, default: False
        Plot MEPs.
    start_mep : float, default: 18
        Start of time frame after TMS pulse where p2p value is evaluated (in ms).
    end_mep : float, default: 35
        End of time frame after TMS pulse where p2p value is evaluated (in ms).

    Returns
    -------
    p2p_array : np.ndarray of float
        (N_stim) Peak to peak values of N sweeps.
    time_mep_lst : list of datetime.timedelta
        MEP-timestamps
    mep_raw_data : np.ndarray of float
        (N_channel, N_stim, N_samples) Raw (unfiltered) MEP data.
    mep_filt_data : np.ndarray of float
        (N_channel, N_stim, N_samples) Filtered MEP data (Butterworth lowpass filter).
    time : np.ndarray of float
        (N_samples) Time axis corresponding to MEP data.
    mep_onset_array : np.ndarray of float
        (S_samples) MEP onset after TMS pulse.
    """
    # convert pulse time to datetime object in case of "delta"
    if time_format == "delta":
        tms_pulse_timedelta = datetime.timedelta(milliseconds=tms_pulse_time * 1000)
    elif time_format == "hms":
        tms_pulse_timedelta = datetime.timedelta()
    else:
        raise NotImplementedError("Specified time_format not implemented yet...")

    if mep_fn.endswith('.cfs'):
        # get data from cfs file
        import biosig
        mep_raw_data_tmp = biosig.data(mep_fn)
        mep_raw_data_tmp = mep_raw_data_tmp[:, cfs_data_column]  # get first channel

        # get header from cfs file
        cfs_header = biosig.header(mep_fn)

        # get timestamps
        # get all indices of timestamps from cfs header
        ts_mep_lst = [timestamp.start() for timestamp in re.finditer('TimeStamp', cfs_header)]
        # get hour, minute and second
        time_mep_list = []
        # convert time string into integer
        for index in ts_mep_lst:
            hour = int(cfs_header[index + 26:index + 28])
            minute = int(cfs_header[index + 29:index + 31])
            second = int(cfs_header[index + 32:index + 34])
            # fix bug with second 60
            if second == 60:
                ts = datetime.datetime(1900, 1, 1, hour, minute, 59)
                ts += datetime.timedelta(seconds=1)
            else:
                ts = datetime.datetime(1900, 1, 1, hour, minute, second)

            # we are interested in the tms pulse time, so add it to ts
            ts += tms_pulse_timedelta
            time_mep_list.append(ts)

        if time_format == "delta":
            time_mep_list = [time_mep_list[i] - time_mep_list[0] for i in range(len(time_mep_list))]
        if time_format == "hms":
            pass

        # add first timestamp (not saved by signal) and shift other by isi
        time_mep_list = [datetime.timedelta(seconds=0)] + [t + time_mep_list[1] - time_mep_list[0] for t in
                                                           time_mep_list]

        # get peak-to-peak values
        # get the ratio of samples per sweep
        sweep_index = cfs_header.find('NumberOfSweeps')
        comma_index = cfs_header.find(',', sweep_index)
        n_sweeps = int(cfs_header[sweep_index + 18:comma_index])
        record_index = cfs_header.find('NumberOfRecords')
        comma_index = cfs_header.find(',', record_index)
        records = int(cfs_header[record_index + 19:comma_index])
        n_samples = int(records / n_sweeps)
        if not isinstance(n_samples, int):
            print('Warning: Number of samples is not an integer.')
            # TODO: Correct get_mep_elements() sample number check. This does not work as expected (from Ole)

        # reshape numpy array
        mep_raw_arr = np.zeros((len(cfs_data_column), n_sweeps, n_samples))

        for i in cfs_data_column:
            mep_raw_arr[i, :, :] = np.reshape(mep_raw_data_tmp[:, i], (n_sweeps, n_samples))

        sampling_rate = get_mep_sampling_rate(mep_fn)

    elif mep_fn.endswith('.mat'):
        mep_data = spio.loadmat(mep_fn, struct_as_record=False, squeeze_me=True)

        # find data
        for k in mep_data.keys():
            if isinstance(mep_data[k], spio.matlab.mio5_params.mat_struct):
                mep_data = mep_data[k].__dict__
                break

        n_samples = mep_data['points']
        mep_raw_arr = mep_data['values'].transpose(1, 2, 0)
        time_mep_list = [datetime.timedelta(seconds=f.__dict__['start']) for f in mep_data['frameinfo']]
        sampling_rate = get_mep_sampling_rate(mep_fn)

    elif mep_fn.endswith('.txt'):
        warnings.warn(".txt import is deprecated - use .mat or .cfs.", DeprecationWarning)
        print("Reading MEP from .txt file")
        # The Signal text export looks like this:
        #
        # "s"\t"ADC 0"\t"ADC 1"
        # 0.00000000\t-0.066681\t-0.047607
        # 0.00025000\t-0.066376\t-0.049286
        # 0.00050000\t-0.066528\t-0.056610
        #
        # "s"\t"ADC 0"\t"ADC 1"
        # 0.00000000\t-0.066681\t-0.047607
        # 0.00025000\t-0.066376\t-0.049286
        # 0.00050000\t-0.066528\t-0.056610
        #
        # With first column = time, second = 1st electrode, ...
        # This is an example of 2 sweeps, 3 samples each, sampling rate = 4000

        # Find number of samples per sweep
        pattern = '"s"'
        with open(mep_fn, 'r') as f:
            for line_nr, line in enumerate(f):
                print(f'{line_nr}: {line}')
                if pattern in line and line_nr > 0:
                    # find second occurance of "s" -> end of first sweep
                    n_samples = line_nr
                    print(f'{line_nr}: {line}')
                if line != '\n':
                    last_sample_time = line

        # extract time (first column) of last samples
        last_sample_time = float(last_sample_time[0:last_sample_time.find('\t')])

        # subtract 2 because first row is header ("s"\t"ADC 0"\t"ADC 1") and last row is blank
        n_samples = n_samples - 2

        df_mep = pd.read_csv(mep_fn,
                             delimiter="\t",
                             skip_blank_lines=True,
                             skiprows=lambda x: x % (n_samples + 2) == 0 and x > 0)

        n_sweeps = int(df_mep.shape[0] / n_samples)
        mep_raw_arr = np.zeros((len(cfs_data_column), n_sweeps, n_samples))

        for i in range(n_sweeps):
            mep_raw_arr[:, i, :] = df_mep.iloc[i * n_samples:(i + 1) * n_samples, 1:].transpose()

        # get sampling rate by dividing number of sweeps by timing
        sampling_rate = int(mep_raw_arr.shape[2] - 1) / last_sample_time

        # build time_mep_list
        # we only have information about the single mep timings, so let's assume signal sticks strictly to the protocol
        sample_len = last_sample_time + 1 / sampling_rate

        # TODO: The ISI is missing here, do we want to add it to the subject object?
        time_mep_list = [datetime.timedelta(seconds=i * sample_len) +
                         tms_pulse_timedelta for i in range(mep_raw_arr.shape[1])]

    else:
        raise ValueError("Unknown MEP file extension. Use .cfs or .txt.")

    # get peak to peak value of every sweep and plot results in mep/plots/channels
    if channels is None:
        channels = [str(i) for i in cfs_data_column]

    tmp = np.zeros((mep_raw_arr.shape[0], mep_raw_arr.shape[1], 3)).astype(object)
    for i_channel in range(mep_raw_arr.shape[0]):
        print(f"Calculating p2p values for channel: {channels[i_channel]}")

        for i_zap in range(mep_raw_arr.shape[1]):
            tmp[i_channel, i_zap, 0], \
                tmp[i_channel, i_zap, 1], \
                tmp[i_channel, i_zap, 2] = calc_p2p(sweep=mep_raw_arr[i_channel, i_zap, :],
                                                    tms_pulse_time=tms_pulse_time,
                                                    sampling_rate=sampling_rate,
                                                    fn_plot=None,
                                                    start_mep=start_mep,
                                                    end_mep=end_mep)

    p2p_arr = np.zeros((tmp.shape[0], tmp.shape[1]))
    mep_onset_arr = np.zeros((tmp.shape[0], tmp.shape[1]))
    mep_filt_arr = np.zeros(mep_raw_arr.shape)

    time = np.arange(mep_raw_arr.shape[2]) / sampling_rate

    for idx_channel in cfs_data_column:
        for i, t in enumerate(tmp[idx_channel, :, :]):
            p2p_arr[idx_channel, i] = tmp[idx_channel, i, 0]
            mep_onset_arr[idx_channel, i] = tmp[idx_channel, i, 2]
            mep_filt_arr[idx_channel, i, :] = tmp[idx_channel, i, 1]

    if time_format == "delta":
        time_mep_list = [time_mep_list[i] - time_mep_list[0] for i in range(len(time_mep_list))]
    elif time_format == "hms":
        pass

    # remove MEPs according to drop_mep_idx and reset time
    if drop_mep_idx is not None:
        p2p_arr = np.delete(p2p_arr, drop_mep_idx)
        mep_onset_arr = np.delete(mep_onset_arr, drop_mep_idx)
        time_mep_list = np.delete(time_mep_list, drop_mep_idx)

    keep_mep_idx = [i for i in range(mep_raw_arr.shape[1]) if i not in np.array(drop_mep_idx)]
    mep_raw_arr = mep_raw_arr[:, keep_mep_idx, :]
    mep_filt_arr = mep_filt_arr[:, keep_mep_idx, :]

    return p2p_arr, time_mep_list, mep_raw_arr, mep_filt_arr, time, mep_onset_arr


def calc_p2p_old_exp0(sweep, start_mep=None, end_mep=None, tms_pulse_time=None, sampling_rate=None):
    """
    Calc peak-to-peak values of an mep sweep.
    This version was probably used in the ancient times of experiment 0.

    Parameters
    ----------
    sweep :  np.ndarray of float
        (Nx1) Input curve.
    start_mep : None
        Not used.
    end_mep : None
        Not used.
    tms_pulse_time : None
        Not used.
    sampling_rate : None
        Not used.

    Returns
    -------
    p2p : float
        Peak-to-peak value of input curve.
    """
    warnings.warn(DeprecationWarning("Use calc_p2p(). calc_p2p_old_exp0 only used for data-reproducibility"))

    # Filter requirements.
    order = 6
    fs = 16000  # sample rate, Hz
    cutoff = 2000  # desired cutoff frequency of the filter, Hz

    # Get the filter coefficients so we can check its frequency response.
    # import matplotlib.pyplot as plt
    # b, a = butter_lowpass(cutoff, fs, order)
    #
    # # Plot the frequency response.
    # w, h = freqz(b, a, worN=8000)
    # plt.subplot(2, 1, 1)
    # plt.plot(0.5 * fs * w / np.pi, np.abs(h), 'b')
    # plt.plot(cutoff, 0.5 * np.sqrt(2), 'ko')
    # plt.axvline(cutoff, color='k')
    # plt.xlim(0, 0.5 * fs)
    # plt.title("Lowpass Filter Frequency Response")
    # plt.xlabel('Frequency [Hz]')
    # plt.grid()

    sweep_filt = butter_lowpass_filter(sweep, cutoff, fs, order)

    # get indices for max
    index_max_begin = np.argmin(sweep) + 40  # get TMS impulse # int(0.221 / 0.4 * sweep.size)
    index_max_begin = int(0.221 / 0.4 * sweep.size)

    index_max_end = sweep_filt.size  # int(0.234 / 0.4 * sweep.size) + 1
    if index_max_begin >= index_max_end:
        index_max_begin = index_max_end - 1
    # index_max_end = index_max_begin + end_mep

    # get maximum and max index
    sweep_max = np.amax(sweep_filt[index_max_begin:index_max_end])
    sweep_max_index = index_max_begin + np.argmax(sweep_filt[index_max_begin:index_max_end])

    # if list of indices then get last value
    if sweep_max_index.size > 1:
        sweep_max_index = sweep_max_index[0]

    # get minimum and mix index
    index_min_begin = sweep_max_index  # int(sweep_max_index + 0.002 / 0.4 * sweep_filt.size)
    index_min_end = sweep_max_index + 40  # int(sweep_max_index + 0.009 / 0.4 * sweep_filt.size) + 1

    # Using the same window as the max should make this more robust
    # index_min_begin = index_max_begi
    sweep_min = np.amin(sweep_filt[index_min_begin:index_min_end])

    return sweep_max - sweep_min


def calc_p2p_old_exp1(sweep, start_mep=18, end_mep=35, tms_pulse_time=None, sampling_rate=2000):
    """
    Calc peak-to-peak values of an mep sweep.
    This version was probably used for the first fits of experiment 1.

    Parameters
    ----------
    sweep :  np.ndarray of float
        (Nx1) Input curve.
    start_mep: float, default: 18
        Starttime in [ms] after TMS for MEP search window.
    end_mep: float, default: 35
        Endtime in [ms] after TMS for MEP search window.
    tms_pulse_time : None
        Not used.
    sampling_rate : int, default: 2000
        Sampling rate in Hz.

    Returns
    -------
    p2p : float
        Peak-to-peak value of input curve.
    """
    warnings.warn(DeprecationWarning("Use calc_p2p(). calc_p2p_old_exp1 only used for data-reproducibility"))

    # Compute start and stop idx according to sampling rate
    start_mep = int((start_mep / 1000.) * sampling_rate)
    end_mep = int((end_mep / 1000.) * sampling_rate)

    # Filter requirements.
    order = 6
    fs = 16000  # sample rate, Hz
    cutoff = 2000  # desired cutoff frequency of the filter, Hz

    sweep_filt = butter_lowpass_filter(sweep, cutoff, fs, order)

    # get indices for max
    index_max_begin = np.argmin(sweep) + start_mep  # get TMS impulse # int(0.221 / 0.4 * sweep.size)
    if index_max_begin >= sweep_filt.size:
        index_max_begin = sweep_filt.size - 1
    # index_max_end = sweep_filt.size  # int(0.234 / 0.4 * sweep.size) + 1
    index_max_end = index_max_begin + end_mep

    # get maximum and max index
    sweep_max = np.amax(sweep_filt[index_max_begin:index_max_end])

    # Using the same window as the max should make this more robust
    index_min_begin = index_max_begin
    index_min_end = index_max_end
    sweep_min = np.amin(sweep_filt[index_min_begin:index_min_end])

    return sweep_max - sweep_min


def calc_p2p(sweep, tms_pulse_time=.2, start_mep=20, end_mep=35, measurement_start_time=0, sampling_rate=4000,
             cutoff_freq=500, fn_plot=None):
    """
    Calc peak-to-peak values of and mep sweep.

    Parameters
    ----------
    sweep :  np.ndarray of float
        (Nx1) Input curve.
    tms_pulse_time : float, default: .2
        Onset time of TMS pulse trigger in [s].
    start_mep : int, default: 18
        Start of p2p search window after TMS pulse in [ms].
    end_mep : int, default: 35
        End of p2p search window after TMS pulse in [ms].
    measurement_start_time : float, default: 0
        Start time of the EMG measurement in [ms].
    sampling_rate : int, default: 2000
        Sampling rate in Hz.
    cutoff_freq : int, default: 500
        Desired cutoff frequency of the filter in Hz.
    fn_plot : str, optional
        Filename of sweep to plot (.png). If None, plot is omitted.

    Returns
    -------
    p2p : float
        Peak-to-peak value of input curve.
    sweep_filt :  np.ndarray of float
        Filtered input curve (Butter lowpass filter with specified cutoff_freq).
    onset : float
        MEP onset after tms_pulse_time.
    """

    def time_to_idx_conversion(t):
        return int((t - measurement_start_time) * sampling_rate / 1000)

    def idx_to_time_conversion(i):
        return i * 1000 / sampling_rate + measurement_start_time

    # Compute start and stop idx according to sampling rate
    if tms_pulse_time > 1:
        warnings.warn(f"Is tms_pulse_time={tms_pulse_time} really in seconds?")

    # Filter requirements.
    order = 6

    sweep_filt = butter_lowpass_filter(sweep, cutoff_freq, sampling_rate, order)

    # beginning of mep search window
    srch_win_start = time_to_idx_conversion(tms_pulse_time * 1000 + start_mep)  # get TMS impulse

    if srch_win_start >= sweep_filt.size:
        srch_win_start = sweep_filt.size - 1
    srch_win_end = time_to_idx_conversion(tms_pulse_time * 1000 + end_mep)

    # get maximum and max index
    sweep_max = np.amax(sweep_filt[srch_win_start:srch_win_end])

    # Using the same window as the max should make this more robust
    sweep_min = np.amin(sweep_filt[srch_win_start:srch_win_end])
    p2p = sweep_max - sweep_min

    # find onset in [s] of mep after tms pulse
    onset_max = np.argmax(sweep[srch_win_start:srch_win_end])
    onset_min = np.argmin(sweep[srch_win_start:srch_win_end])
    if onset_min < onset_max:
        onset_max = onset_min
    onset_max += srch_win_start
    onset_max /= sampling_rate
    onset_max -= tms_pulse_time

    if fn_plot is not None:
        timepoints = np.asarray([idx_to_time_conversion(i) for i in np.arange(len(sweep))], dtype=np.float32)
        sweep_min_idx = np.argmin(sweep_filt[srch_win_start:srch_win_end]) + srch_win_start
        sweep_max_idx = np.argmax(sweep_filt[srch_win_start:srch_win_end]) + srch_win_start

        timepoints /= 1000
        plt.figure(figsize=[4.07, 3.52])
        plt.plot(timepoints, sweep)
        plt.plot(timepoints, sweep_filt)
        plt.scatter(timepoints[sweep_min_idx], sweep_min, 15, color="r")
        plt.scatter(timepoints[sweep_max_idx], sweep_max, 15, color="r")
        plt.plot(timepoints, np.ones(len(timepoints)) * sweep_min, linestyle="--", color="r", linewidth=1)
        plt.plot(timepoints, np.ones(len(timepoints)) * sweep_max, linestyle="--", color="r", linewidth=1)
        plt.grid()
        plt.legend(["raw", "filtered", "p2p"], loc='upper right')

        plt.xlim([np.max((tms_pulse_time - 0.01, np.min(timepoints))),
                  np.min((timepoints[srch_win_end] + .1, np.max(timepoints)))])
        plt.ylim([-1.1 * np.abs(sweep_min), 1.1 * np.abs(sweep_max)])

        plt.xlabel("time in s", fontsize=11)
        plt.ylabel("MEP in mV", fontsize=11)
        plt.tight_layout()

        plt.savefig(fn_plot, dpi=300, transparent=True)
        plt.close()

    return p2p, sweep_filt, onset_max


def get_mep_sampling_rate(cfs_path):
    """
    Returns sampling rate [Hz] for CED Signal EMG data in .cfs, .mat or .txt file.

    The sampling rate is saved in the cfs header like this:

    .. code-block:: sh

       ``Samplingrate"\t: 3999.999810,\n``

    Parameters
    ----------
    cfs_path : str
        Path to .cfs file or .txt file.

    Returns
    -------
    float : sampling rate
    """
    if cfs_path.endswith('.cfs'):
        # get header from cfs file
        cfs_header = biosig.header(cfs_path)

        # get start and end idx of 'samplingrate'
        idx_a = re.search('Samplingrate', cfs_header)

        # get idx of first '\n' after 'samplingrate'
        idx_b = re.search(',\n', cfs_header[idx_a.end():])

        sr_start = idx_a.end() + 4  # 'Samplingrate"\t: '
        return float(cfs_header[sr_start:idx_b.start() + idx_a.end()])

    elif cfs_path.endswith('.mat'):
        mep_data = spio.loadmat(cfs_path, struct_as_record=False, squeeze_me=True)
        for k in mep_data.keys():
            if isinstance(mep_data[k], spio.matlab.mio5_params.mat_struct):
                mep_data = mep_data[k].__dict__
                break
        return 1 / mep_data['interval']

    elif cfs_path.endswith('.txt'):
        # search for end of first frame / sweep
        pattern = '"s"'
        with open(cfs_path, 'r') as f:
            for line_nr, line in enumerate(f):
                if pattern in line and line_nr > 0:
                    # find second occurance of "s" -> end of first sweep
                    n_samples = line_nr
                    break
                if line != '\n':
                    last_sample_time = line
        # extract time (first column) of last samples
        last_sample_time = float(last_sample_time[0:last_sample_time.find('\t')])

        # subtract 2 because first row is header ("s"\t"ADC 0"\t"ADC 1") and last row is blank
        n_samples -= 2

        # get sampling rate by dividing number of sweeps by timing
        return n_samples / last_sample_time
    else:
        raise ValueError(f"cfs_path={cfs_path} must be .csf or .txt filename.")


def butter_lowpass(cutoff, fs, order=5):
    """
    Setup Butter low-pass filter and return filter parameters.

    Parameters
    ----------
    cutoff : float
        Cutoff frequency in [Hz].
    fs : float
        Sampling frequency in [Hz].
    order : int, default: 5
        Filter order.

    Returns
    -------
    b, a : np.ndarray, np.ndarray
        Numerator (b) and denominator (a) polynomials of the IIR filter.
    """

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def butter_lowpass_filter(data, cutoff, fs, order=5):
    """
    Applies Butterworth lowpass filter.

    Parameters
    ----------
    data : np.ndarray of float
        (N_samples) Input of the digital filter.
    cutoff : float
        Cutoff frequency in [Hz].
    fs : float
        Sampling frequency in [Hz].
    order : int
        Filter order.

    Returns
    -------
    y : np.ndarray
        (N_samples) Output of the digital filter.
    """

    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


def get_time_date(cfs_paths):
    """
    Get time and date of the start of the recording out of .cfs file.

    Parameters
    ----------
    cfs_paths : str
        Path to .cfs mep file.

    Returns
    -------
    time_date : str
        Date and time.
    """

    cfs_header = biosig.header(cfs_paths[0])
    index = cfs_header.find('StartOfRecording')
    time_date = cfs_header[index + 21:index + 40]
    return time_date


def scale_e_for_dvs(e, mt=60, upper_limit=100):
    """
    Scale the electric field for DVS and TVS to 0-1 range, with 0 being motor threshold.

    Parameters
    ----------
    e : np.array
        Electric field in V/m.
    mt : float, default: 60
        Desired motor threshold in V/m.
    upper_limit : float, default: 100
        Upper limit of the activation curve in V/m.

    Returns
    -------
    float : scaled electric field in V/m.
    """
    return (e - mt)/(upper_limit - mt)