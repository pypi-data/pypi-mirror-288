import pynibs
import matplotlib
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker


try:
    matplotlib.use("Qt5Agg")
except ImportError:
    pass


def plot_io_curve(
        mep_data,
        local_mag_e,
        title="I/O curve",
        y_axis_label="EMG p2p-amplitude, µV",
        x_axis_label="mag(E), V/m, scaled",
        fit_fun=None,
        screenshot_fn=None,
        interactive=False,
        mso=None):
    """
    Plot scattered data of MEP-mag(E) pairs (=> I/O curve).
    Optionally the fit of the proided fit function can be overlaid.

    Parameters
    ----------
    mep_data: np.ndarray[float], [n_stims]
        The acquired MEPs fo each stimulation.
    local_mag_e: np.ndarray[float], [n_stims]
        The local electric field magnitude at the ROI element the I/O curve should be plotted from.
    title: str, optional
        The title of the plot; default: "I/O curve"
    y_axis_label: str, optional
        The title of the y-axis; default: "EMG p2p-amplitude, µV"
    x_axis_label: str, optional
        The title of the x-axis; default: "mag(E), V/m, scaled"
    fit_fun: Callable, optional
        If provided, the fit of the I/O curve with the provided function will be computed and displayed.
        Currently supported: pynibs.simgoid4, pynibs.sigmoid4_log, pynibs.linear
    screenshot_fn: str, optional
        If provided, output the plotted image to that file location.
    interactive: bool
        If True, spawn plot in blocking window.
    mso : np.ndarray or list, optional
        MSO values.

    Returns
    -------
        True if successful, False otherwise.
    """
    if interactive:
        matplotlib.use('Qt5Agg')
    else:
        matplotlib.use('Agg')

    plt.figure(figsize=(11, 11))
    plt.scatter(y=np.log10(mep_data) if fit_fun == pynibs.expio.fit_funs.sigmoid4_log else mep_data,
                x=local_mag_e,
                cmap=plt.cm.get_cmap('spring_r'),
                c=mso if mso is not None else list(range(len(local_mag_e))),
                vmin=0, vmax=100 if mso is not None else len(local_mag_e))

    plt.scatter(y=np.log10(mep_data[-1]) if fit_fun == pynibs.expio.fit_funs.sigmoid4_log else mep_data[-1],
                x=local_mag_e[-1],
                cmap=plt.cm.get_cmap('spring_r'),
                c=mso[-1] if mso is not None else len(local_mag_e),
                s=500,
                vmin=0, vmax=100 if mso is not None else len(local_mag_e))

    if fit_fun is not None:
        local_mag_e_np = np.zeros((len(local_mag_e), 1))
        local_mag_e_np[:, 0] = local_mag_e

        fit_scores, fit_params = pynibs.regression.regress_data(
                e_matrix=np.array(local_mag_e_np),
                mep=mep_data,
                fun=fit_fun,
                n_cpu=16,
                con=None,
                n_refit=10,
                return_fits=True,
                verbose=False,
                pool=None,
                refit_discontinuities=False,
                select_signed_data=False
        )

        num_samples = 100
        x = np.linspace(0, np.min((120, np.max(local_mag_e))), num_samples)
        if fit_fun == pynibs.expio.fit_funs.sigmoid4_log or fit_fun == pynibs.expio.fit_funs.sigmoid4:
            y = fit_fun(x,
                        x0=fit_params[0]['x0'],
                        r=fit_params[0]['r'],
                        amp=fit_params[0]['amp'],
                        y0=fit_params[0]['y0']
                        )
        elif fit_fun == pynibs.expio.fit_funs.linear:
            y = fit_fun(x,
                        m=fit_params[0]["m"],
                        n=fit_params[0]["n"]
                        )
        else:
            y = np.zeros(num_samples)

        title += f", R2: {round(fit_scores[0], 5): <5}"
        plt.plot(x, y, color='black')
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        # for k, v in fit_params.items()
        text = '\n'.join(f'{k: >7}: {np.round(v,2):2.2f}' for k, v in fit_params[0].items())
        text = f'Fitted params:\n‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾\n{text}\n   n_zaps: {len(mep_data): >6}'
        text += f'\n% MSO: {int(mso[-1]): >5}' if mso is not None else ''
        plt.text(local_mag_e.max() - 5, 2, text, fontsize=18,
                 verticalalignment='top', bbox=props, horizontalalignment='right')
        cb = plt.colorbar()
        cb.ax.set_ylabel("% MSO" if mso is not None else "Stimulation Id", fontsize=18)

    if screenshot_fn is not None:
        if fit_fun == pynibs.expio.fit_funs.sigmoid4_log:
            tick_log_rev = lambda x, y: int(pow(10, x))
            ytick_formatter = ticker.FuncFormatter(tick_log_rev)
            y_axis_label += ",\n log10-scaled"
            ax = plt.gca()
            ax.yaxis.set_major_formatter(ytick_formatter)

        plt.title(title, fontsize=32)
        plt.xlabel(x_axis_label, fontsize=30)
        plt.ylabel(y_axis_label, fontsize=30)
        plt.xticks(fontsize=28)
        plt.yticks(fontsize=28)
        plt.savefig(screenshot_fn)

    if interactive:
        plt.show()
    plt.close()
