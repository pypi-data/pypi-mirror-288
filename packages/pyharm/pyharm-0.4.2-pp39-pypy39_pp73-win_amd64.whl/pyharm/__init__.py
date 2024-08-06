"""
PyHarm is a Python wrapper for CHarm.
"""


# start delvewheel patch
def _delvewheel_patch_1_7_2():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'pyharm.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-pyharm-0.4.2')
        if os.path.isfile(load_order_filepath):
            with open(os.path.join(libs_dir, '.load-order-pyharm-0.4.2')) as file:
                load_order = file.read().split()
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(ctypes.c_wchar_p(lib_path), None, 0x00000008):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


_delvewheel_patch_1_7_2()
del _delvewheel_patch_1_7_2
# end delvewheel patch

import os as _os
from ._lib import _load_lib

# Name of the shared CHarm library to load
_libcharmname = 'libcharm'

# Directory of "_libcharmname"
_libcharmdir = _os.path.join(_os.path.dirname(__file__), '')

# Load the shared CHarm library
_libcharm = _load_lib(_libcharmdir, _libcharmname)

# Prefix to be added to the CHarm function names.  Depends on the format of
# floating point numbers used to compile CHarm (single or double precision).
_CHARM = 'charm_'

# Prefix to be added to the PyHarm functions when calling "__repr__" methods
_pyharm = 'pyharm'

# The "err" module is intentionally not imported, as users do not interact with
# it in PyHarm.
from . import crd, glob, integ, leg, misc, sha, shc, shs
__all__ = ['crd', 'glob', 'integ', 'leg', 'misc', 'sha', 'shc', 'shs']
