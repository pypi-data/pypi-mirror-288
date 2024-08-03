""" """
import os
import h5py
import numpy as np
import pynibs


def cfs2hdf5(fn_cfs, fn_hdf5=None):
    """
    Converts EMG data included in .cfs file to .hdf5 format.

    Parameters
    ----------
    fn_cfs : str
        Filename of .cfs file.
    fn_hdf5 : str, optional
        Filename of .hdf5 file (if not provided, a file with same name as fn_cfs will be created with .hdf5 extension).

    Returns
    -------
    <file> : .hdf5 File
        File containing:

        * EMG data in f["emg"][:]
        * Time axis in f["time"][:]
    """
    try:
        import biosig
    except ImportError:
        ImportError("Please install biosig from pynibs/pkg/biosig folder!")

    if fn_hdf5 is None:
        fn_hdf5 = os.path.splitext(fn_cfs)[0] + ".hdf5"

    # load header and data
    cfs_header = biosig.header(fn_cfs)
    emg = biosig.data(fn_cfs)[:, 0]

    sweep_index = cfs_header.find('NumberOfSweeps')
    comma_index = cfs_header.find(',', sweep_index)
    sweeps = int(cfs_header[sweep_index + 18:comma_index])
    records = emg.shape[0]
    samples = int(records / sweeps)
    sampling_rate = pynibs.get_mep_sampling_rate(fn_cfs)
    emg = np.reshape(emg, (sweeps, samples))
    time = np.linspace(0, samples, samples) / sampling_rate

    with h5py.File(fn_hdf5, "w") as f:
        f.create_dataset("emg", data=emg)
        f.create_dataset("time", data=time)
        f.create_dataset("sampling_rate", data=np.array([sampling_rate]))
