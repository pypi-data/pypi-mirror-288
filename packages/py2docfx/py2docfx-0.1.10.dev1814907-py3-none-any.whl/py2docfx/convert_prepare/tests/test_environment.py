import os
import shutil
import pytest
import subprocess

from py2docfx import PACKAGE_ROOT
from py2docfx.convert_prepare.environment import VirtualEnvironmentManager

def test_create_venv():

    venvManager = VirtualEnvironmentManager([], [], None, None)

    vitual_env_path = venvManager.create_template_venv("test_venv")
    vitual_env_executable_path = os.path.join(vitual_env_path, "Scripts", "python.exe")

    # Check if the virtual environment executable path is correct
    assert os.path.exists(os.path.join(PACKAGE_ROOT, "venv"))
    assert os.path.exists(vitual_env_executable_path)

    # Check if the venv executable is functional
    result = subprocess.run([vitual_env_executable_path, "-m", "pip", "--version"], capture_output=True, check=True)
    assert result.returncode == 0

    # Clean up the venv folder
    shutil.rmtree(os.path.join(PACKAGE_ROOT, "venv"))
