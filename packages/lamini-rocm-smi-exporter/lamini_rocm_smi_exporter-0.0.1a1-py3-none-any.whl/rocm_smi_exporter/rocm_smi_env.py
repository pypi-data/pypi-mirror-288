from dataclasses import dataclass
import shutil
import os

def _check_rocm_smi_version():
    """
    Raises exception if the version does not match the expected version
    """
    # TODO: Check rocm-smi version and make sure we only work with tested version.
    # The goal is be conservative, and report any unexpected ROCm versions.
    pass

def _resolve_binary_abspath(binary_name: str):
    """
    Given a binary's name, find its absolute path.
    """
    path_env = os.environ.get('PATH', "<NONE>")
    try:
        binary_path = shutil.which(binary_name)
        if binary_path is None:
            raise FileNotFoundError(f"'{binary_name}' was not found in PATH: {path_env}.")
        
        # Resolve symlinks to get the actual path
        return os.path.realpath(binary_path)
    except Exception as e:
        raise FileNotFoundError(f"'{binary_name}' could not be resolved in PATH: {path_env}, error: {e}.")


ROCM_SMI_CLI_NAME = 'rocm-smi'
ROCM_SMI_PY = 'rocm_smi.py'
RSMI_BINDINGS_PY = 'rsmiBindings.py'

@dataclass
class ROCmSMIEnv:
    """
    ROCmSMIEnv describes the runtime information of the rocm-smi CLI.

    Include rocm_smi_abspath 
    """
    rocm_smi_abspath: str = None
    rsmi_bindings_abspath: str = None

    @classmethod
    def resolve(cls):
        _check_rocm_smi_version()
        rocm_smi_abspath = _resolve_binary_abspath(ROCM_SMI_CLI_NAME)
        
        rocm_smi_py = os.path.basename(rocm_smi_abspath)
        if rocm_smi_py != ROCM_SMI_PY:
            # rocm-smi must be a symlink to rocm_smi.py.
            # This behavior has to be tested on each time we want to upgrade rocm version.
            raise FileNotFoundError(f"{ROCM_SMI_CLI_NAME} is found, but resolves to {rocm_smi_abspath} instead of {ROCM_SMI_PY}")
        
        rsmi_binding_pypath = os.path.join(os.path.dirname(rocm_smi_abspath), RSMI_BINDINGS_PY)
        if not os.path.isfile(rsmi_binding_pypath):
            raise FileNotFoundError(f"{rsmi_binding_pypath} is not found")
        return cls(rocm_smi_abspath, rsmi_binding_pypath)

import importlib.util as importutil
import sys

def _import_abspath(abspath: str, exec: bool = False):
    PY_EXT = ".py"
    assert abspath.endswith(PY_EXT)

    module_name = os.path.basename(abspath).removesuffix(PY_EXT)
    spec = importutil.spec_from_file_location(module_name, abspath)
    module = importutil.module_from_spec(spec)
    sys.modules[module_name] = module
    if exec:
        spec.loader.exec_module(module)
    return module


_env = ROCmSMIEnv.resolve()
# rsmi_bindings_abspath has to be imported first,
# because rsmi_abspath references it.
_rsmi_bindings = _import_abspath(_env.rsmi_bindings_abspath, True)
_rsmi = _import_abspath(_env.rocm_smi_abspath, True)


# Initialize rsmi
_rsmi.PRIN_JSON = True
_rsmi.rocmsmi = _rsmi_bindings.initRsmiBindings(silent=True)
_rsmi.initializeRsmi()

def get_rsmi():
    assert _rsmi.driverInitialized()
    return _rsmi