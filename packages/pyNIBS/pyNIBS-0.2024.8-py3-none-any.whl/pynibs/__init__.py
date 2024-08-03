from .tensor_scaling import rescale_lambda_centerized_workhorse
from .tensor_scaling import rescale_lambda_centerized
from .models import *
from .hdf5_io import *
from .coil import *
from .expio import *
from .util import *
from .hdf5_io import *
from .optimization import *
from .freesurfer import *
from .roi import *
from .subject import *
from .neuron import *
from .mesh import *
from .regression import *
from .visualization import *
from .tms_pulse import *

try:
    from .pckg import libeep
except (ImportError, SyntaxError):
    pass


__version__ = "0.2024.8"

# when pipped, datadir is under pynibs
__testdatadir__ = os.path.join(os.path.dirname(__file__), '..', 'tests', 'data')
__datadir__ = os.path.join(os.path.dirname(__file__), '..', 'data')
if not os.path.exists(__testdatadir__):
    __testdatadir__ = os.path.join(os.path.dirname(__file__), 'tests', 'data')
    __datadir__ = os.path.join(os.path.dirname(__file__), 'data')
if not os.path.exists(__testdatadir__):
    warnings.warn(f"Cannot find pynibs.__testdatadir__='{__testdatadir__}'")
