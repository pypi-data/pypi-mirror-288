import os
import copy
import time
import h5py
import inspect
import warnings
import itertools
import subprocess
import numpy as np
from scipy.special import binom
from sklearn.neighbors import KernelDensity
import pynibs


def tal2mni(coords, direction='tal2mni', style='nonlinear'):
    """
    Transform Talairach coordinates into (SPM) MNI space and vice versa.

    This is taken from https://imaging.mrc-cbu.cam.ac.uk/imaging/MniTalairach and
    http://gibms.mc.ntu.edu.tw/bmlab/tools/data-analysis-codes/mni2tal-m/

    Parameters
    ----------
    coords : np.ndarray or list
        x,y,z coordinates.
    direction : str, default: 'tal2mni
        Transformation direction. One of ('tal2mni', 'mni2tal').
    style : str, default: 'nonlinear'
        Transformation style. One of ('linear', 'nonlinear').

    Returns
    -------
    coords_trans : np.ndarray

    """
    assert direction in ['tal2mni',
                         'mni2tal'], f"direction parameter '{direction}' invalid. Choose 'tal2mni' or 'mni2tal'."
    assert style in ['linear', 'nonlinear'], f"style parameter '{style}' invalid. Choose 'linear' or 'nonlinear'."
    if len(coords) == 3:
        coords = np.hstack((coords, 1))
    if style == 'linear':
        mat = np.array([[0.88, 0, 0, -0.8], [0, 0.97, 0, -3.32], [0, 0.05, 0.88, -0.44], [0, 0, 0, 1]])
        if direction == 'mni2tal':
            return np.dot(mat, coords)[:3]
        elif direction == 'tal2mni':
            return np.dot(np.linalg.inv(mat), coords)[:3]
    elif style == 'nonlinear':
        upper_mat = np.array([[0.99, 0, 0, 0],
                              [0, 0.9688, 0.0460, 0],
                              [0, -0.0485, 0.9189, 0],
                              [0, 0, 0, 1]])

        lower_mat = np.array([[0.99, 0, 0, 0],
                              [0, 0.9688, 0.042, 0],
                              [0, -0.0485, 0.839, 0],
                              [0, 0, 0, 1]])
        if direction == 'mni2tal':
            pass
        elif direction == 'tal2mni':
            upper_mat = np.linalg.inv(upper_mat)
            lower_mat = np.linalg.inv(lower_mat)
        if coords[2] > 0:
            # above AC
            return np.dot(upper_mat, coords)[:3]
        else:
            # below AC
            return np.dot(lower_mat, coords)[:3]


def rd(array, array_ref):
    """
    Determine the relative difference between input data and reference data.

    Parameters
    ----------
    array : np.ndarray
        input data [ (x), y0, y1, y2 ... ].
    array_ref : np.ndarray
        reference data [ (x_ref), y0_ref, y1_ref, y2_ref ... ]
        if array_ref is 1D, all sizes have to match.

    Returns
    -------
    rd : ndarray of float
        (array.shape[1]) Relative difference between the columns of array and array_ref.
    """

    return np.linalg.norm(array - array_ref) / np.linalg.norm(array_ref)


def generalized_extreme_value_distribution(x, mu, sigma, k):
    """
    Generalized extreme value distribution.

    Parameters
    ----------
    x : ndarray of float
        (n_x) Events.
    mu : float
        Mean value.
    sigma : float
        Standard deviation.
    k : float
        Shape parameter.

    Returns
    -------
    y : ndarray of float
        (n_x) Probability density of events
    """
    y = 1 / sigma * np.exp(-(1 + (k * (x - mu)) / sigma) ** (-1 / k)) * (1 + (k * (x - mu)) / sigma) ** (-(1 + 1 / k))

    return y


def differential_evolution(fobj, bounds, mut=0.8, crossp=0.7, popsize=20, its=1000, **kwargs):
    """
    Differential evolution optimization algorithm

    Parameters
    ----------
    fobj : function object
        Function to optimize.
    bounds : dict
        Dictionary containing the bounds of the free variables to optimize.
    mut : float, default: 0.8
        Mutation factor.
    crossp : float, default: 0.7
        Cross population factor.
    popsize : int, default: 20
        Population size.
    its : int, default: 1000
        Number of iterations.
    kwargs : dict
        Arguments passed to fobj (constants etc...).

    Returns
    -------
    best : dict
        Dictionary containing the best values.
    fitness : float
        Fitness value of best solution.
    """
    if kwargs is None:
        kwargs = dict()

    fobj_args = inspect.getfullargspec(fobj).args

    if "bounds" in fobj_args:
        kwargs["bounds"] = bounds
    params_str = list(bounds.keys())

    # set up initial simulations
    dimensions = len(bounds)
    pop = np.random.rand(popsize, dimensions)

    min_b = np.zeros(dimensions)
    max_b = np.zeros(dimensions)

    for i, key in enumerate(bounds):
        min_b[i] = bounds[key][0]
        max_b[i] = bounds[key][1]

    diff = np.fabs(min_b - max_b)
    pop_denorm = min_b + pop * diff

    print("Initial simulations:")
    print("====================")

    fitness = np.zeros(len(pop_denorm))

    for i, po in enumerate(pop_denorm):

        for i_key, key in enumerate(params_str):
            kwargs[key] = po[i_key]

        fitness[i] = fobj(**kwargs)

    best_idx = np.argmin(fitness)
    best = pop_denorm[best_idx]

    parameter_str = [f"{params_str[i_p]}={p_:.5f}" for i_p, p_ in enumerate(pop_denorm[best_idx])]
    print(f"-> Fittest: {fitness[best_idx]:.3f} / " + ", ".join(parameter_str))

    for i in range(its):
        print(f"Iteration: {i}")
        print(f"==============")

        trial_denorm = []
        trial = []

        # create new parameter sets
        for j in range(popsize):
            idxs = [idx for idx in range(popsize) if idx != j]
            a, b, c = pop[np.random.choice(idxs, 3, replace=False)]
            mutant = np.clip(a + mut * (b - c), 0, 1)
            cross_points = np.random.rand(dimensions) < crossp

            if not np.any(cross_points):
                cross_points[np.random.randint(0, dimensions)] = True

            trial.append(np.where(cross_points, mutant, pop[j]))
            trial_denorm.append(min_b + trial[j] * diff)

        # run likelihood function
        f = np.zeros(len(trial))

        for j, tr in enumerate(trial_denorm):
            for i_key, key in enumerate(params_str):
                kwargs[key] = tr[i_key]
            f[j] = fobj(**kwargs)

        for j in range(popsize):
            if f[j] < fitness[j]:
                fitness[j] = copy.deepcopy(f[j])
                pop[j] = trial[j]
                if f[j] < fitness[best_idx]:
                    best_idx = j
                    best = trial_denorm[j]

        parameter_str = [f"{params_str[i_p]}={p_:.5f}" for i_p, p_ in enumerate(best)]
        print(f"-> Fittest: {fitness[best_idx]:.3f} / " + ", ".join(parameter_str))

    best_dict = dict()
    for i_key, key in enumerate(params_str):
        best_dict[key] = best[i_key]

    return best_dict, fitness[best_idx]


def sigmoid_log_p(x, p):
    y = np.log10(p[0] / (1 + np.exp(-p[1] * (x - p[2]))))
    return y


def likelihood_posterior(x, y, fun, bounds=None, verbose=True, normalized_params=False, **params):
    """
    Determines the likelihood of the data following the function "fun" assuming a two
    variability source of the data pairs (x, y) using the posterior distribution.

    Parameters
    ----------
    x : ndarray of float
        (n_points) x data.
    y : ndarray of float
        (n_points) y data
    fun : function
        Function to fit the data to (e.g. sigmoid).
    bounds : dict, optional
        Dictionary containing the bounds of "sigma_x" and "sigma_y" and the free parameters of fun.
    verbose : bool, default: True
        Print function output after every calculation.
    normalized_params : bool, default: False
        Are the parameters passed in normalized space between [0, 1]? If so, bounds are used to
        denormalize them before calculation.
    **params : dict
        Free parameters to optimize. Contains "sigma_x", "sigma_y", and the free parameters of fun.

    Returns
    -------
    l : float
        Negative likelihood.
    """
    start = time.time()

    # read arguments from function
    # args = inspect.getfullargspec(fun).args

    # extract parameters
    sigma_x = params["sigma_x"]
    sigma_y = params["sigma_y"]

    del params["sigma_x"], params["sigma_y"]

    # denormalize parameters from [0, 1] to bounds
    if normalized_params:
        if bounds is None:
            raise ValueError("Please provide bounds if parameters were passed normalized!")
        sigma_x = sigma_x * (bounds["sigma_x"][1] - bounds["sigma_x"][0]) + bounds["sigma_x"][0]
        sigma_y = sigma_y * (bounds["sigma_y"][1] - bounds["sigma_y"][0]) + bounds["sigma_y"][0]

        for key in enumerate(params):
            params[key] = params[key] * (bounds[key][1] - bounds[key][0]) + bounds[key][0]

    if sigma_x < 0:
        sigma_x = 0

    if sigma_y < 0:
        sigma_y = 0

    # determine posterior of DVS model with test data
    x_pre = np.linspace(np.min(x), np.max(x), 500000)
    x_post = x_pre + np.random.normal(loc=0., scale=sigma_x, size=len(x_pre))
    y_post = fun(x_post, **params) + np.random.normal(loc=0., scale=sigma_y, size=len(x_pre))

    # bin data
    n_bins = 50
    dx_bins = (np.max(x_pre) - np.min(x_pre)) / n_bins
    x_bins_loc = np.linspace(np.min(x_pre) + dx_bins / 2, np.max(x_pre) - dx_bins / 2, n_bins)

    # determine probabilities of observations
    kde = KernelDensity(bandwidth=0.01, kernel='gaussian')

    likelihood = []

    for i in range(n_bins):
        mask = np.logical_and(x_pre >= (x_bins_loc[i] - dx_bins / 2), x_pre < (x_bins_loc[i] + dx_bins / 2))
        mask_data = np.logical_and(x >= (x_bins_loc[i] - dx_bins / 2), x < (x_bins_loc[i] + dx_bins / 2))

        if np.sum(mask_data) == 0:
            continue

        # determine kernel density estimate
        try:
            kde_bins = kde.fit(y_post[mask][:, np.newaxis])
        except ValueError:
            warnings.warn("kde.fit(y_post[mask][:, np.newaxis]) yield NaN ... skipping bin")
            continue

        # get probability densities at data
        kde_y_post_bins = np.exp(kde_bins.score_samples(y[mask_data][:, np.newaxis]))

        likelihood.append(kde_y_post_bins)

    likelihood = np.concatenate(likelihood)

    # mask out zero probabilities
    likelihood[likelihood == 0] = 1e-100

    # determine log likelihood
    likelihood = np.sum(np.log10(likelihood))

    stop = time.time()

    if verbose:
        parameter_str = [f"{p_}={params[p_]:.5f}" for p_ in params]
        print(f"Likelihood: {likelihood:.1f} / sigma_x={sigma_x:.5f}, sigma_y={sigma_y:.5f}, " +
              ", ".join(parameter_str) + f"({stop - start:.2f} sec)")

    return -likelihood


def mutual_coherence(array):
    """
    Calculate the mutual coherence of a matrix A. It can also be referred as the cosine of the smallest angle
    between two columns.

    mutual_coherence = mutual_coherence(array)

    Parameters
    ----------
    array : ndarray of float
        Input matrix.

    Returns
    -------
    mutual_coherence : float
        Mutual coherence.
    """

    array = array / np.linalg.norm(array, axis=0)[np.newaxis, :]
    t = np.matmul(array.conj().T, array)
    np.fill_diagonal(t, 0.0)
    mu = np.max(t)

    # s = np.sqrt(np.diag(t))
    # s_sqrt = np.diag(s)
    # mu = np.max(1.0*(t-s_sqrt)/np.outer(s, s))

    return mu


def get_cartesian_product(array_list):
    """
    Generate a cartesian product of input arrays (all combinations).

    cartesian_product = get_cartesian_product(array_list)

    Parameters
    ----------
    array_list : list of 1D ndarray of float
        Arrays to compute the cartesian product with.

    Returns
    -------
    cartesian_product : ndarray of float
        (M, len(arrays)) Array containing the cartesian products (all combinations of input vectors).

    Examples
    --------
     .. code-block:: python
        import pygpc
        out = pygpc.get_cartesian_product(([1, 2, 3], [4, 5], [6, 7]))
        out
    """
    cartesian_product = [element for element in itertools.product(*array_list)]
    return np.array(cartesian_product)


def norm_percentile(data, percentile):
    """
    Normalizes data to a given percentile.

    Parameters
    ----------
    data : np.ndarray
        (n_data, ) Dataset to normalize.
    percentile : float
        Percentile of normalization value [0 ... 100].

    Returns
    -------
    data_norm : np.ndarray
        (n_data, ) Normalized dataset.
    """
    return data / np.percentile(data, percentile)


def compute_chunks(seq, num):
    """
    Splits up a sequence _seq_ into _num_ chunks of similar size.
    If len(seq) < num, (num-len(seq)) empty chunks are returned so that len(out) == num.

    Parameters
    ----------
    seq : list of something
        (n_ele) List containing data or indices, which is divided into chunks.
    num : int
        Number of chunks to generate.

    Returns
    -------
    out : list of num sublists
        num sub-lists of seq with each of a similar number of elements (or empty).
    """
    assert len(seq) > 0
    assert num > 0
    assert isinstance(seq, list), f"{type(seq)} can't be chunked. Provide list."
    avg = len(seq) / float(num)
    n_empty = 0  # if len(seg) < num, how many empty lists to append to return?

    if avg < 1:
        # raise ValueError("seq/num ration too small: " + str(avg))
        avg = 1
        n_empty = num - len(seq)

    out = []
    last = 0.0

    while last < len(seq):
        # if only one element would be left in the last run, add it to the current
        if (int(last + avg) + 1) == len(seq):
            last_append_idx = int(last + avg) + 1
        else:
            last_append_idx = int(last + avg)

        out.append(seq[int(last):last_append_idx])

        if (int(last + avg) + 1) == len(seq):
            last += avg + 1
        else:
            last += avg

    # append empty lists if len(seq) < num
    out += [[]] * n_empty

    return out


def bash(command):
    """
    Executes bash command and returns output message in stdout (uses os.popen).

    Parameters
    ----------
    command : str
        Bash command.

    Returns
    -------
    output : str
        Output from stdout.
    error : str
        Error message from stdout.
    """
    print(("Running " + command))
    return os.popen(command).read()
    # process = subprocess.Popen(command.split(), stdout=subprocess.PIPE, shell=True)
    # output, error = process.communicate()
    # return output, error


def bash_call(command):
    """
    Executes bash command and returns output message in stdout (uses subprocess.Popen).

    Parameters
    ----------
    command : str
        bash command.
    """
    subprocess.Popen(command, shell=True)


def invert(trans):
    """
    Invert rotation matrix.

    Parameters
    ----------
    trans : np.ndarray of float
        (3, 3) Rotation matrix.

    Returns
    -------
    rot_inv : np.ndarray of float
        (3, 3) Inverse rotation matrix.
    """
    rot = pynibs.normalize_rot(trans[:3, :3].flatten())
    result = np.zeros((4, 4))
    result[3, 3] = 1.0
    t = -rot.T.dot(trans[:3, 3])
    result[:3, :3] = rot.T
    result[:3, 3] = t
    return result


def list2dict(l):
    """
    Transform list of dicts with same keys to dict of list

    Parameters
    ----------
    l : list of dict
        List containing dictionaries with same keys.

    Returns
    -------
    d : dict of lists
        Dictionary containing the entries in a list.
    """
    n = len(l)
    keys = l[0].keys()
    d = dict()

    for key in keys:
        d[key] = [0 for _ in range(n)]
        for i in range(n):
            d[key][i] = l[i][key]

    return d


def recursive_len(item):
    """
    Determine len of list of lists (recursively).

    Parameters
    ----------
    item : list of list
        List of list.

    Returns
    -------
    len : int
        Total length of list of lists.
    """
    if type(item) == list:
        return sum(recursive_len(subitem) for subitem in item)
    else:
        return 1


def add_center(var):
    """
    Adds center to argument list.

    Parameters
    ----------
    var : list of float
        (2) List containing two values [f1,f2].

    Returns
    -------
    out: list of float
        (3) List containing the average value in the middle [f1, mean(f1,f2), f2].
    """
    return [var[0], sum(var) / 2, var[1]]


def unique_rows(a):
    """
    Returns the unique rows of np.array(a).

    Parameters
    ----------
    a : np.ndarray of float
        (m, n) Array to search for double row entries.

    Returns
    -------
    a_unique : np.array
        (k, n) array a with only unique rows.
    """
    b = np.ascontiguousarray(a).view(np.dtype((np.void, a.dtype.itemsize * a.shape[1])))
    _, idx = np.unique(b, return_index=True)
    return a[idx]
    # alternative but ~10x slower:
    # surface_points=np.vstack({tuple(row) for row in surface_points})


def calc_n_network_combs(n_e, n_c, n_i):
    """
    Determine number of combinations if all conditions may be replaced between N_i elements (mixed interaction).

    Parameters
    ----------
    n_e : int
        Number of elements in the ROI.
    n_c : int
        Number of conditions (I/O curves).
    n_i : int
        Number of maximum interactions.

    Returns
    -------
    n_comb : int
        Number of combinations.
    """
    return binom(n_e, n_i) * np.sum([((n_i - 1) ** k) * binom(n_c, k) for k in range(1, n_c)])


def load_muaps(fn_muaps, fs=1e6, fs_downsample=1e5):
    # load MUAPs and downsample
    with h5py.File(fn_muaps, "r") as f:
        muaps_orig = f["MUAPShapes"][:]
    N_MU = muaps_orig.shape[1]

    t_muap_orig = np.linspace(0, 1 / fs * (muaps_orig.shape[0] - 1), muaps_orig.shape[0])
    t_muap = np.linspace(0, t_muap_orig[-1], int(t_muap_orig[-1] * fs_downsample + 1))
    muaps = np.zeros((len(t_muap), N_MU))

    for i in range(N_MU):
        muaps[:, i] = np.interp(t_muap, t_muap_orig, muaps_orig[:, i])

    return muaps, t_muap


def cross_product(A, B):
    """
    Evaluates the cross product between the vector pairs in a and b using pure Python.

    Parameters
    ----------
    A : np.ndarray of float
        (2, (N, 3))
    B : np.ndarray of float
        (2, (N, 3)) Input vectors, the cross product is evaluated between.

    Returns
    -------
    c : np.ndarray of float
        (N, 3) Cross product between vector pairs in a and b.
    """
    c1 = np.multiply(A[:, 1], B[:, 2]) - np.multiply(A[:, 2], B[:, 1])
    c2 = np.multiply(A[:, 2], B[:, 0]) - np.multiply(A[:, 0], B[:, 2])
    c3 = np.multiply(A[:, 0], B[:, 1]) - np.multiply(A[:, 1], B[:, 0])
    # C=np.array(np.multiply(A[:, 1], B[:, 2]) - np.multiply(A[:, 2], B[:, 1]),
    #            np.multiply(A[:, 2], B[:, 0]) - np.multiply(A[:, 0], B[:, 2]),
    #            np.multiply(A[:, 0], B[:, 1]) - np.multiply(A[:, 1], B[:, 0]))
    return np.vstack([c1, c2, c3]).transpose()


def cross_product_einsum2(a, b):
    """
    Evaluates the cross product between the vector pairs in a and b using the double Einstein sum.

    Parameters
    ----------
    a : np.ndarray of float
        (2, (N, 3))
    b : np.ndarray of float
        (2, (N, 3)) Input vectors, the cross product is evaluated between.

    Returns
    -------
    c : np.ndarray of float
        (N, 3) Cross product between vector pairs in a and b.
    """
    eijk = np.zeros((3, 3, 3))
    eijk[0, 1, 2] = eijk[1, 2, 0] = eijk[2, 0, 1] = 1
    eijk[0, 2, 1] = eijk[2, 1, 0] = eijk[1, 0, 2] = -1

    return np.einsum('iak,ak->ai', np.einsum('ijk,aj->iak', eijk, a), b)


def intersection_vec_plan(ray_dir, ray_origin, plane_n, plane_p, eps=1e-6):
    """
    Computes intersection between vector ('ray') and plane.

    Parameters
    ----------
    ray_dir : np.ndarray
        (3,) (Rotated) vector direction.
    ray_origin : np.ndarray
        (3,) Any point on the ray.
    plane_n : np.ndarray
        (3,) Plane normal.
    plane_p : np.ndarray
        (3,) Any point on the plane.
    eps : float, default=1e-6
        Resolution.

    Returns
    -------
    inters : np.ndarray
        (3,) Intersection location. (np.inf, np.inf, np.inf) if no intersection.
    """
    ndotu = plane_n.dot(ray_dir)

    if abs(ndotu) < eps:
        return np.array([np.inf, np.inf, np.inf])
    w = ray_origin - plane_p
    si = -plane_n.dot(w) / ndotu
    intersec = w + si * ray_dir + plane_p

    return intersec
