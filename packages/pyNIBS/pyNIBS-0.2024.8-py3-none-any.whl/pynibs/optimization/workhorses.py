import scipy
import numpy as np
from sklearn.neighbors import KernelDensity

import pynibs


def mc(idx_list, array, ele_idx_1, mode="cols", **kwargs):
    """
    Determines mutual coherence for given zap indices in idx_list.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the optimization is performed.
    mode : str, default: "cols"
        Set if the mutual coherence is calculated w.r.t. columns or rows ("cols", "rows").

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Mutual coherence. Lower values indicate more orthogonal e-field combinations (better).
    """

    res = []
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    for ind in idx_list:
        if mode == "cols":
            res.append(pynibs.mutual_coherence(array[ind, :]))
        elif mode == "rows":
            res.append(pynibs.mutual_coherence(array[ind, :].transpose()))
        else:
            raise NotImplementedError("Specified mode not implemented. Choose 'rows' or 'cols'.")

    return res


def roi_elmt_wise_corr(idx_list, e_mat, ele_idx_1, decorrelate_hotspot_only=False, backend=np, **kwargs):
    """
    Compute element wise correlation for sets of e-field.

    Parameters
    ----------
    idx_list : list of int
        List of efield indicies in e_mat.
    e_mat : np.ndarray
        All e-fields.
    ele_idx_1 : list of int
        All element indices to compute corcoeff for.
    decorrelate_hotspot_only : bool, default: False
        If true, ele_idx_1[-.1] is used for decorrelation.
    backend : module
        Package to use to compute correlation - probably either numpy or cuda.

    Returns
    -------
    res : np.ndarray
        (e_mat.shape[0], ) with correlations for all e-field sets in idx_list.
    """
    res = backend.zeros(len(idx_list))

    for result_list_idx, coil_conf_seq_idcs in enumerate(idx_list):
        # extract values of interest from e-field matrix
        e_selected_subsampled = e_mat[coil_conf_seq_idcs][:, ele_idx_1]

        # compute column-wise correlation: we want to reduce the e-field correlation between ROI elements
        correlation_mat = backend.corrcoef(e_selected_subsampled, rowvar=False)

        if decorrelate_hotspot_only:
            # assumption: hotspot index is always included at last position of 'ele_idx_1'
            res[result_list_idx] = backend.mean(backend.abs(correlation_mat[-1, :]))
        else:
            # temp_mat = backend.abs(correlation_mat)
            # res[result_list_idx] = backend.mean(correlation_mat[backend.triu_indices_from(temp_mat, k=1)])
            res[result_list_idx] = backend.mean(backend.abs(correlation_mat))

        # num_nonzero_elmts = backend.count_nonzero(temp_mat)
        # matrix score
        # score = 1 / num_nonzero_elmts * backend.sum(temp_mat)
    return res


def coil_wise_corr(idx_list, array, ele_idx_1, **kwargs):
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    res = []

    for ind in idx_list:
        r = np.corrcoef(array[ind, :])
        res.append(np.mean(r[np.triu_indices(r.shape[0], k=1)]))

    return res


def var(idx_list, array, ele_idx_1, **kwargs):
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    res = []

    for ind in idx_list:
        res.append(np.mean(np.var(array[ind, :], axis=0)))

    return res


def smooth(idx_list, array, ele_idx_1, **kwargs):
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    res = []

    for ind in idx_list:
        res.append(np.var(np.mean(array[ind, :], axis=0)))

    return res


def svd(idx_list, array, ele_idx_1, **kwargs):
    """
    Determines condition number for given zap indices in idx_list.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the optimization is performed.

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Condition number. Lower values indicate more orthogonal e-field combinations (better).
    """
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    res = []

    for ind in idx_list:
        s = scipy.linalg.svd(array[ind, :], compute_uv=False)
        res.append(np.max(s) / np.min(s))

    return res


def variability(idx_list, array, ele_idx_1, **kwargs):
    """
    Determines variability score for given zap indices in idx_list.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the optimization is performed.

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Condition number. Lower values indicate more orthogonal e-field combinations (better).
    """
    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    res = []

    for ind in idx_list:
        distances = np.zeros((array.shape[1], array.shape[1]))
        d = 0

        for col_idx in range(0, array.shape[1] - 1):
            for row_idx in range(col_idx + 1, array.shape[1]):
                distances[row_idx, col_idx] = np.linalg.norm(array[ind, row_idx] - array[ind, col_idx])
                d += distances[row_idx, col_idx]

        res.append(1 / d)

    return res


def rowvec_diff_prepare(idx_list, array, ele_idx_1, **kwargs):
    """
    Computes the part of the difference matrix of row-vectors specified by the row indices in idx_list.
    Assumption: 'idx_list' must be sorted and valid within 'array'.

    :param idx_list: typing.List[int]
        List of row indices whose difference should be determined.
    :param array: numpy.typing.ArrayLike [n_coil x n_ele]
        E-field matrix of all possible coil positions.
    :param ele_idx_1: numpy.typing.ArrayLike [n_ele]
        Indices of the ROI elements that should be considered for optimization.
    :return: numpy.typing.ArrayLike [array.shape[0] x array.shape[0]] = [n_rows x n_rows]
        The difference matrix with the lenght of the difference vectors between
        pairs of row vectors specified by idx_list. All other (not calculated)
        paris of row vectors have a score of 0 in this matrix.
    """
    efields_from_coil = array
    total_num_coil_pos = array.shape[0]

    # preparation:
    # for each pair of coil configuration, determine the difference of the associated rwo vectors in the e-field matrix
    efields_diff = np.zeros((efields_from_coil.shape[0], efields_from_coil.shape[0]))
    for coil_idx_outer in idx_list:
        for coil_idx_inner in range(coil_idx_outer + 1, total_num_coil_pos):
            diff_vec = efields_from_coil[coil_idx_outer, ele_idx_1] - efields_from_coil[coil_idx_inner, ele_idx_1]
            efields_diff[coil_idx_outer, coil_idx_inner] = np.linalg.norm(diff_vec, ord=2)

    return efields_diff


def dist(idx_list, array, ele_idx_1, **kwargs):
    """
    Determines distance score for given zap indices in idx_list.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the optimization is performed.

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Distance based score. Lower values indicate more equidistant sampling (better)
    """
    res = np.zeros(len(idx_list))

    array_dist = array[:, ele_idx_1]

    if array_dist.ndim == 1:
        array_dist = array_dist[:, np.newaxis]

    e_max = np.max(array_dist, axis=0)
    e_min = np.min(array_dist, axis=0)

    for j, ind in enumerate(idx_list):
        p = np.vstack((e_min, array_dist[ind, :], e_max))
        d_var = np.zeros(array_dist.shape[1])

        for i in range(array_dist.shape[1]):
            p_sort = np.sort(p[:, i])

            if p_sort[0] == p_sort[1]:
                p_sort = p_sort[1:]

            if p_sort[-2] == p_sort[-1]:
                p_sort = p_sort[:-1]

            d_var[i] = np.var(np.diff(p_sort))

        res[j] = np.mean(d_var)

    return res


def dist_svd(idx_list, array, ele_idx_1, ele_idx_2, **kwargs):
    """
    Determines distance score and condition number for given zap indices in idx_list. If c_max_idx is given,
    the distance based score is calculated only for this element.
    The condition number however is optimized for all elements in array

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the dist optimization is performed for.
    ele_idx_2 : np.ndarray of float [n_ele]
        Element indices for which the svd optimization is performed for.

    Returns
    -------
    res_dist : np.ndarray of float [n_combs]
        Distance based score. Lower values indicate more equidistant sampling (better).
    res_svd : np.ndarray of float [n_combs]
        Condition number. Lower values indicate more orthogonal e-field combinations (better).
    """
    res_dist = np.zeros(len(idx_list))
    res_svd = np.zeros(len(idx_list))

    array_dist = array[:, ele_idx_1]

    if array_dist.ndim == 1:
        array_dist = array_dist[:, np.newaxis]

    array_svd = array[:, ele_idx_2]

    if array_svd.ndim == 1:
        array_svd = array_svd[:, np.newaxis]

    e_max = np.max(array_dist, axis=0)
    e_min = np.min(array_dist, axis=0)

    for j, ind in enumerate(idx_list):

        # svd
        u, s, vh = scipy.linalg.svd(array_svd[ind, :])
        res_svd[j] = np.max(s) / np.min(s)

        # dist
        p = np.vstack((e_min, array_dist[ind, :], e_max))
        d_var = np.zeros(array_dist.shape[1])

        for i in range(array_dist.shape[1]):
            p_sort = np.sort(p[:, i])

            if p_sort[0] == p_sort[1]:
                p_sort = p_sort[1:]

            if p_sort[-2] == p_sort[-1]:
                p_sort = p_sort[:-1]

            d_var[i] = np.var(np.diff(p_sort))

        res_dist[j] = np.mean(d_var)

    return res_dist, res_svd


def dist_mc(idx_list, array, ele_idx_1, ele_idx_2, mode="cols", **kwargs):
    """
    Determines distance score and mutual coherence for given zap indices in idx_list. If c_max_idx is given,
    the distance based score is calculated only for this element.
    The condition number however is optimized for all elements in array.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    mode : str, default: "cols"
        Set if the mutual coherence is calculated w.r.t. columns or rows ("cols", "rows").
    ele_idx_1 : np.ndarray of float [n_ele]
        Element indices for which the dist optimization is performed for.
    ele_idx_2 : np.ndarray of float [n_ele]
        Element indices for which the mc optimization is performed for.

    Returns
    -------
    res_dist : np.ndarray of float [n_combs]
        Distance based score. Lower values indicate more equidistant sampling (better).
    res_mc : np.ndarray of float [n_combs]
        Mutual coherence. Lower values indicate more orthogonal e-field combinations (better).
    """
    res_dist = np.zeros(len(idx_list))
    res_mc = np.zeros(len(idx_list))

    array_dist = array[:, ele_idx_1]

    if array_dist.ndim == 1:
        array_dist = array_dist[:, np.newaxis]

    array_mc = array[:, ele_idx_2]

    if array_mc.ndim == 1:
        array_mc = array_mc[:, np.newaxis]

    e_max = np.max(array_dist, axis=0)
    e_min = np.min(array_dist, axis=0)

    for j, ind in enumerate(idx_list):

        # mc
        if mode == "cols":
            res_mc[j] = pynibs.mutual_coherence(array_mc[ind, :])
        elif mode == "rows":
            res_mc[j] = pynibs.mutual_coherence(array_mc[ind, :].transpose())
        else:
            raise NotImplementedError("Specified mode not implemented. Choose 'rows' or 'cols'.")

        # dist
        p = np.vstack((e_min, array_dist[ind, :], e_max))
        d_var = np.zeros(array_dist.shape[1])

        for i in range(array_dist.shape[1]):
            p_sort = np.sort(p[:, i])

            if p_sort[0] == p_sort[1]:
                p_sort = p_sort[1:]

            if p_sort[-2] == p_sort[-1]:
                p_sort = p_sort[:-1]

            d_var[i] = np.var(np.diff(p_sort))

        res_dist[j] = np.mean(d_var)

    return res_dist, res_mc


def coverage_prepare(idx_list, array, zap_idx, **kwargs):
    """Prepares coverage calculation.
    Determines coverage distributions for elements in idx_list given the zaps in zap_idx

    Parameters
    ----------
    idx_list : list [n_ele]
        Index lists of elements.
    array : ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    zap_idx : ndarray of int
        Included zaps in coverage distribution.

    Returns
    -------
    x : ndarray of float [200 x n_ele]
        x-values of coverage distributions, defined in interval [0, 1] (element wise normalized electric field).
    y : ndarray of float [200 x n_ele]
        y-values of coverage distributions (element wise probability of already included e-fields).
    """

    n_x = 200

    x = np.zeros((n_x, len(idx_list)))
    y = np.zeros((n_x, len(idx_list)))

    kde = KernelDensity(bandwidth=0.03, kernel='gaussian')

    for j, ind in enumerate(idx_list):
        e_min = np.min(array[:, ind])
        e_max = np.max(array[:, ind])
        e_samples = (array[zap_idx, ind] - e_min) / (e_max - e_min)

        if not isinstance(e_samples, np.ndarray):
            e_samples = np.array([e_samples])

        kde_ele = kde.fit(e_samples[:, np.newaxis])
        x[:, j] = np.linspace(0, 1, n_x)
        y[:, j] = np.exp(kde_ele.score_samples(x[:, j][:, np.newaxis]))

    return x, y


def coverage(idx_list, array, x, y, ele_idx_1, **kwargs):
    """
    Determine coverage score (likelihood) for given zap indices in idx_list

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    x : np.ndarray of float [200 x n_ele]
        x-values of coverage distributions, defined in interval [0, 1] (element wise normalized electric field).
    y : np.ndarray of float [200 x n_ele]
        y-values of coverage distributions (element wise probability of already included e-fields).
    ele_idx_1 : np.ndarray of float [n_roi]
        Element indices for which the coverage optimization is performed for.

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Coverage score (likelihood) for given electric field combinations. Lower values indicate that the
        new zap fills a gap which was not covered before.
    """

    p_e = np.zeros(len(idx_list))

    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    for j, ind in enumerate(idx_list):
        p_e_zap = np.zeros(array.shape[1])

        # normalized e-fields of this zap in all elements
        e_zap = (array[ind[-1], :] - np.min(array, axis=0)) / (np.max(array, axis=0) - np.min(array, axis=0))

        # determine e-field coverage probability for every element
        for i_ele in range(array.shape[1]):
            p_e_zap[i_ele] = np.interp(x=e_zap[i_ele], xp=x[:, i_ele], fp=y[:, i_ele])

        # accumulate e-field coverage over ever elements using log-likelihood
        p_e_zap[p_e_zap <= 0] = 1e-100
        p_e[j] = np.sum(p_e_zap)

    return p_e


def fim(idx_list, array, ele_idx_1, e_opt, c=None, **kwargs):
    """
    Determine difference between e-fields and optimal e-field determined using the Fisher Information Matrix.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_roi]
        Element indices for which the fim optimization is performed for.
    e_opt : np.ndarray of float [n_roi]
        Optimal electric field value(s) (target) determined by FIM method.
    c : np.ndarray of float [n_ele], optional
        Congruence factor map normalized to 1 (whole ROI) used to weight the difference between the optimal e-field
        and the candidate e-field. If None, no weighting is applied.

    Returns
    -------
    res : np.ndarray of float [n_combs]
        Difference between e-fields and optimal e-field.
    """

    if c is None:
        c = np.ones(array.shape[1])

    res = np.zeros(len(idx_list))

    array = array[:, ele_idx_1]

    if array.ndim == 1:
        array = array[:, np.newaxis]

    for j, ind in enumerate(idx_list):
        res[j] = np.linalg.norm((e_opt - array[ind[-1], ele_idx_1]) * c[ele_idx_1])

    return res


def fim_svd(idx_list, array, ele_idx_1, ele_idx_2, e_opt, c=None, **kwargs):
    """
    Determine difference between e-fields and optimal e-field determined using the Fisher Information Matrix and
    condition number.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_roi_1]
        Element indices for which the fim optimization is performed for.
    ele_idx_2 : np.ndarray of float [n_roi_2]
        Element indices for which the svd optimization is performed for.
    e_opt : float
        Optimal electric field value (target) determined by FIM method.
    c : np.ndarray of float [n_ele], optional
        Congruence factor map normalized to 1 (whole ROI) used to weight the difference between the optimal e-field
        and the candidate e-field. If None, no weighting is applied.

    Returns
    -------
    res_fim : np.ndarray of float [n_combs]
        Difference between e-fields and optimal e-field.
    res_svd : np.ndarray of float [n_combs]
        Condition number. Lower values indicate more orthogonal e-field combinations (better)
    """

    if c is None:
        c = np.ones(array.shape[1])

    res_fim = np.zeros(len(idx_list))
    res_svd = np.zeros(len(idx_list))

    array_fim = array[:, ele_idx_1]

    if array_fim.ndim == 1:
        array_fim = array_fim[:, np.newaxis]

    array_svd = array[:, ele_idx_2]

    if array_svd.ndim == 1:
        array_svd = array_svd[:, np.newaxis]

    for j, ind in enumerate(idx_list):
        # fim
        intensity = np.mean(array_fim[ind[-1], :] / e_opt)
        res_fim[j] = np.linalg.norm((e_opt - intensity * array_fim[ind[-1], :]) * c[ele_idx_1])

        # svd
        u, s, vh = scipy.linalg.svd(array_svd[ind, :])
        res_svd[j] = np.max(s) / np.min(s)

    return res_fim, res_svd


def fim_mc(idx_list, array, ele_idx_1, ele_idx_2, e_opt, c=None, mode="rows", **kwargs):
    """
    Determine difference between e-fields and optimal e-field determined using the Fisher Information Matrix and
    mutual coherence.

    Parameters
    ----------
    idx_list : list of lists [n_combs][n_zaps]
        Index lists of zaps containing different possible combinations. Usually only the last index changes.
    array : np.ndarray of float [n_zaps x n_ele]
        Electric field for different coil positions and elements.
    ele_idx_1 : np.ndarray of float [n_roi_1]
        Element indices for which the fim optimization is performed for.
    ele_idx_2 : np.ndarray of float [n_roi_2]
        Element indices for which the mc optimization is performed for.
    e_opt : float
        Optimal electric field value (target) determined by FIM method.
    c : np.ndarray of float [n_ele], optional
        Congruence factor map normalized to 1 (whole ROI) used to weight the difference between the optimal e-field
        and the candidate e-field. If None, no weighting is applied.
    mode : str

    Returns
    -------
    res_fim : np.ndarray of float [n_combs]
        Difference between e-fields and optimal e-field.
    res_mc : np.ndarray of float [n_combs]
        Mutual coherence. Lower values indicate more orthogonal e-field combinations (better)
    """

    if c is None:
        c = np.ones(array.shape[1])

    res_fim = np.zeros(len(idx_list))
    res_mc = np.zeros(len(idx_list))

    array_fim = array[:, ele_idx_1]

    if array_fim.ndim == 1:
        array_fim = array_fim[:, np.newaxis]

    array_mc = array[:, ele_idx_2]

    if array_mc.ndim == 1:
        array_mc = array_mc[:, np.newaxis]

    for j, ind in enumerate(idx_list):
        # fim
        res_fim[j] = np.linalg.norm((e_opt - array_fim[ind[-1], :]) * c[ele_idx_1])

        # mc
        if mode == "cols":
            res_mc[j] = pynibs.mutual_coherence(array_mc[ind, :])
        elif mode == "rows":
            res_mc[j] = pynibs.mutual_coherence(array_mc[ind, :].transpose())
        else:
            raise NotImplementedError("Specified mode not implemented. Choose 'rows' or 'cols'.")

    return res_fim, res_mc


def rowvec_diff(candidate_coil_idcs, selected_coil_idcs, efields_diff_mat):
    """
    Given a difference matrix (e.g. of row vectors/coil configurations) this function
    returns the coil configuration out of all available configurations exhibiting the
    highest minimum difference to the already selected configurations.

    Parameters
    ----------
    candidate_coil_idcs : np.ndarry[int]
        List of indices of coil configurations that are still available to pick for the optiized sequence.
    selected_coil_idcs : np.ndarray[int]
        List of indices of coil configurations that have already been selected for the optimized sequence.
    efields_diff_mat : np.ndarray[float], [n_coil,n_coil]
        Difference matrix, where each cell denotes the magnitude of the difference vector between
        two coil configurations (determined by row_idx,col_idx).

    Returns
    -------
    coil_idx: int
        Index of coil configuration with maximal minimal difference to the set of already selected coil configurations.
    """

    # min_diff_selected_to_all_coil_pos = matrix with:
    #   rows -> set of selected coil configurations (selected_coil_idcs)
    #   columns -> available coil configuration for optimization (candidate_coil_idcs)
    min_diff_selected_to_all_coil_pos = np.min(efields_diff_mat[selected_coil_idcs][:, candidate_coil_idcs], axis=0)

    # returned index valid in the "idx_list" array
    return np.argmax(min_diff_selected_to_all_coil_pos), np.max(min_diff_selected_to_all_coil_pos)
