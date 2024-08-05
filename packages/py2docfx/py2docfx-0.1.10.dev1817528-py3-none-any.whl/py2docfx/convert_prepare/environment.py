import os
import subprocess
import sys
import time

from py2docfx import PACKAGE_ROOT
from py2docfx.convert_prepare.get_source import get_source
from py2docfx.convert_prepare.install_package import install_package

REQUIREMENT_MODULES = ["setuptools", "sphinx==6.1.3", "pyyaml", "jinja2==3.0.3"]

def install_converter_requirements(executable: str):
    """
    Install setuptools/sphinx/pyyaml/jinja2
    Replacing logic of
    https://apidrop.visualstudio.com/Content%20CI/_git/ReferenceAutomation?path=/Python/InstallPackage.ps1&line=15&lineEnd=35&lineStartColumn=1&lineEndColumn=87&lineStyle=plain&_a=contents
    """
    pip_install_cmd = [executable, "-m", "pip", "install", "--upgrade"]

    pip_install_common_options = [
        # "--no-cache-dir",
        "--quiet",
        "--no-compile",
        "--no-warn-conflicts",
        "--disable-pip-version-check",
    ]

    for module in REQUIREMENT_MODULES:
        subprocess.run(
            pip_install_cmd + [module] + pip_install_common_options, check=True
        )

class VirtualEnvironmentManager:
    package_info_list = []
    required_package_list = []
    github_token = None
    ado_token = None

    def __init__(self, package_info_list, required_package_list, github_token, ado_token):
        self.package_info_list = package_info_list
        self.required_package_list = required_package_list
        self.github_token = github_token
        self.ado_token = ado_token

    def install_required_packages(self, executable: str) -> None:
            for idx, package in enumerate(self.required_package_list):
                if package.install_type == package.InstallType.SOURCE_CODE:
                    get_source(package, idx, executable, vststoken=self.ado_token, githubtoken=self.github_token)
                install_package(package, executable)

    def create_template_venv(self, venv_name: str) -> str:
        start_time = time.time()
        venv_dir = os.path.join(PACKAGE_ROOT, "venv", venv_name)

        try:
            subprocess.run([sys.executable, "-m", "venv", venv_dir], check=True)
        except subprocess.CalledProcessError as e:
            raise RuntimeError(f"Failed to create virtual environment: {e}")

        if os.name == "nt":
            env_executable = os.path.join(venv_dir, "Scripts", "python.exe")

        install_converter_requirements(env_executable)
        if (self.required_package_list is not None) and (len(self.required_package_list) > 0):
            self.install_required_packages(env_executable)
        end_time = time.time()
        with open(os.path.join(PACKAGE_ROOT, "time.txt"), "a") as f:
            f.write(f"Time taken to create virtual environment ID {venv_name}: {end_time - start_time} seconds\n")
        print(f"<CI INFO>: Time taken to create virtual environment ID {venv_name}: {end_time - start_time} seconds")
        return venv_dir