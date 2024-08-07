from pathlib import Path
import sys
import os
import shutil

MKL_DLLS = ['libiomp5md.dll',
            'mkl_core.2.dll',
            'mkl_intel_thread.2.dll',
            'mkl_rt.2.dll']
FORTRAN_DLLS = ['libifcoremd.dll',
                'libifcoremdd.dll',
                'libmmd.dll',
                'libifportmd.dll',
                'libmmdd.dll',
                'svml_dispmd.dll',
                'libiomp5md.dll']
# VC_RUNTIME_DLLS = ['vcruntime140.dll',
#                    'vcruntime140_1.dll']
# HDF5_DLLS = ['hdf5.dll',
#              'hdf5_hl.dll']

interpreter_path = Path(sys.executable).parent
library_bin_path = interpreter_path / 'Library' / 'bin'
if not library_bin_path.exists():
    if 'Scripts' in interpreter_path.parts:
        library_bin_path = interpreter_path.parent / 'Library' / 'bin'

h5py_path = interpreter_path / 'Lib' / 'site-packages' / 'h5py'
mydir = Path(__file__).parent


error = False
if library_bin_path.exists():
    for dll in MKL_DLLS:
        dll_path = library_bin_path / dll
        if not dll_path.exists():
            error = True
            print(f"Missing DLL: {dll}")
        else:
            if not (mydir / dll).exists():
                shutil.copy(dll_path, mydir / dll)

    # for dll in VC_RUNTIME_DLLS:
    #     dll_path = interpreter_path / dll
    #     if not dll_path.exists():
    #         error = True
    #         print(f"Missing DLL: {dll}")
    #     else:
    #         if not (mydir / dll).exists():
    #             shutil.copy(dll_path, mydir / dll)

    for dll in FORTRAN_DLLS:
        dll_path = library_bin_path / dll
        if not dll_path.exists():
            error = True
            print(f"Missing DLL: {dll}")
        else:
            if not (mydir / dll).exists():
                shutil.copy(dll_path, mydir / dll)

else:
    error = True
    print("Library/bin directory not found -- Impossible to copy DLLs.")

# if h5py_path.exists():
#     for dll in HDF5_DLLS:
#         dll_path = h5py_path / dll
#         if not dll_path.exists():
#             error = True
#             print(f"Missing DLL: {dll}")
#         else:
#             if not (mydir / dll).exists():
#                 shutil.copy(dll_path, mydir / dll)
# else:
#     error = True
#     print("h5py directory not found.")

if error:
    raise FileNotFoundError("Missing DLLs. Please check the output above.")