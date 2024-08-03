import numpy as np


def dummy_fun(x, a):
    """
    Dummy function for congruence factor calculation.
    """
    return x


def sigmoid(x, x0, r, amp):
    """
    Parametrized sigmoid function.

    .. math::
        y = \\frac{amp}{1+e^{-r(x-x_0)}}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    amp : float
        Maximum value the sigmoid converges to.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at argument x.
    """
    y = amp / (1 + np.exp(-r * (x - x0)))
    return y


def sigmoid4(x, x0, r, amp, y0):
    """
    Parametrized sigmoid function with 4 parameters.

    .. math::
        y = y_0 + \\frac{amp - y_0}{1+e^{-r(x-x_0)}}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) x-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    amp : float
        Maximum value the sigmoid converges to.
    y0 : float
        Offset value of the sigmoid.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at argument x.
    """
    exp = -r * (x - x0)

    # avoid numpy RuntimeWarning: overflow encountered in exp
    if np.all(exp < 500):
        y = y0 + (amp - y0) / (1 + np.exp(exp))
    else:
        # return a flat line; high value to maximally impair fits
        y = np.ones(x.shape)
        y *= np.iinfo(np.int32).max

    return y


def sigmoid_log(x, x0, r, amp):
    """
    Parametrized log transformed sigmoid function.

    .. math::
        y = \\log\\left(\\frac{amp}{1+e^{-r(x-x_0)}}\\right)

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) x-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    amp : float
        Maximum value the sigmoid converges to.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at argument x.
    """
    y = np.log10(1e-12 + (amp - 1e-12) / (1 + np.exp(-r * (x - x0))))
    return y


def sigmoid4_log(x, x0, r, amp, y0):
    """
    Parametrized log transformed sigmoid function with 4 parameters.

    .. math::
        y = \\log\\left(y_0 + \\frac{amp - y_0}{1+e^{-r(x-x_0)}}\\right)

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    amp : float
        Maximum value the sigmoid converges to (upper saturation).
    y0 : float
        Y-offset value of the sigmoid.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at argument x.
    """
    return np.log10(sigmoid4(y0=y0, amp=amp, x=x, x0=x0, r=r))


def linear(x, m, n):
    """
    Parametrized linear function.

    .. math::
        y = mx+n

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    m : float
        Slope parameter.
    n : float
        Y-offset.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at argument x.
    """
    y = m * x + n
    return y


def linear_log(x, m, n):
    """
    Parametrized log linear function.

    .. math::
        y = mx+n

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    m : float
        Slope parameter (steepness).
    n : float
        Y-offset.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at x.
    """
    y = m * x + n
    y[y <= 0] = 1e-16
    y = np.log10(y)
    y[y == -np.inf] = -16
    y[y == np.inf] = 16

    return y


def exp(x, x0, r, y0):
    """
    Parametrized exponential function.

    .. math::
        y = y_0 + e^{r(x-x_0)}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    y0: float
        Offset parameter.

    Returns
    -------
    y : np.ndarray of float
        (N_x,) Function value at x.
    """
    y = y0 + np.exp(r * (x - x0))
    return y


def exp_log(x, x0, r, y0):
    """
    Parametrized exponential function (log).

    .. math::
        y = y_0 + e^{r(x-x_0)}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).
    y0: float
        y-offset parameter.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at x.
    """
    y = np.log10(y0 + np.exp(r * (x - x0)))
    return y


def exp0(x, x0, r):
    """
    Parametrized exponential function w/o offset.

    .. math::
        y = e^{r(x-x_0)}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter (steepness).

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at x.
    """
    y = np.exp(r * (x - x0))
    return y


def exp0_log(x, x0, r):
    """
    Parametrized exponential function w/o offset.

    .. math::
        y = e^{r(x-x_0)}

    Parameters
    ----------
    x : np.ndarray of float
        (N_x) X-values the function is evaluated in.
    x0 : float
        Horizontal shift along the abscissa.
    r : float
        Slope parameter.

    Returns
    -------
    y : np.ndarray of float
        (N_x) Function value at x.
    """
    y = np.log10(np.exp(r * (x - x0)))
    return y
