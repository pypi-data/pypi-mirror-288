"""
The hdf5_io subpackage provides utilities for reading and writing data in the HDF5 format,
as well as generating XDMF files for visualization of the data. It includes functions for
writing surface data, creating XDMF files for surfaces and fibers, overlaying data stored
in HDF5 files, and writing coordinates to an XDMF file for visualization. This subpackage
is primarily used for handling and visualizing data related to neuroimaging and brain
stimulation studies.
"""
from .hdf5_io import *
from .xdmf import *
