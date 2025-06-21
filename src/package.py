"""Install packages in a virtual environment and update the lock file and pyproject.toml."""

import os
import subprocess
from pathlib import Path

import rich
import toml

# pylint: skip-file


def add(names: list[str], venv_path: str):
    """
    Install packages in the virtual environment and update the lock file and pyproject.toml.
    Args:
        names (list[str]): List of package names to install.
        venv_path (str): Path to the virtual environment.
    Raises:
        FileNotFoundError: If pip is not found in the virtual environment.
        RuntimeError: If the pip install command fails.
        Exception: For any other unexpected errors.

    """
    venv: Path = Path(venv_path)
    if os.name == "nt":  # Windows
        pip_path = venv / "Scripts" / "pip.exe"
    else:  # Linux / macOS
        pip_path = venv / "bin" / "pip"

    if not pip_path.exists():
        raise FileNotFoundError(
            f"pip not found at {pip_path}. Ensure the virtual environment is set up correctly."
        )
    command = f'"{pip_path}" install ' + " ".join(names)
    print(f"Running command: {command}")
    result = os.system(command)
    if result != 0:
        raise RuntimeError(
            f"Failed to install packages: {names}. Command returned exit code {result}."
        )
    lock = Path("ppmx.lock")
    cmd_freeze = [str(pip_path), "freeze"]
    freeze_output = subprocess.run(cmd_freeze, capture_output=True, text=True)

    with lock.open("w") as f:
        f.write(freeze_output.stdout)

    # Update the pyproject.toml file with the new dependencies
    file = toml.load(Path("pyproject.toml"))
    if "dependencies" not in file["project"]:
        file["project"]["dependencies"] = []
    file["project"]["dependencies"].extend(names)
    with Path("pyproject.toml").open("w") as f:
        toml.dump(file, f)
    print(f"Packages {names} installed successfully and lock file updated at {lock}.")
    rich.print(
        f"[green]Packages {', '.join(names)} installed successfully and pyproject.toml updated.[/green]"
    )

def remove(names: list[str], venv_path: str):
    """Remove packages from the virtual environment and update the lock file and pyproject.toml."""
    venv: Path = Path(venv_path)
    if os.name == "nt":  # Windows
        pip_path = venv / "Scripts" / "pip.exe"
    else:  # Linux / macOS
        pip_path = venv / "bin" / "pip"

    if not pip_path.exists():
        raise FileNotFoundError(
            f"pip not found at {pip_path}. Ensure the virtual environment is set up correctly."
        )
    command = f'"{pip_path}" uninstall -y ' + " ".join(names)
    print(f"Running command: {command}")
    result = os.system(command)
    if result != 0:
        raise RuntimeError(
            f"Failed to uninstall packages: {names}. Command returned exit code {result}."
        )
    lock = Path("ppmx.lock")
    cmd_freeze = [str(pip_path), "freeze"]
    freeze_output = subprocess.run(cmd_freeze, capture_output=True, text=True)

    with lock.open("w") as f:
        f.write(freeze_output.stdout)

    # Update the pyproject.toml file by removing the dependencies
    file = toml.load(Path("pyproject.toml"))
    if "dependencies" in file["project"]:
        file["project"]["dependencies"] = [
            dep for dep in file["project"]["dependencies"] if dep not in names
        ]
    with Path("pyproject.toml").open("w") as f:
        toml.dump(file, f)
    print(f"Packages {names} removed successfully and lock file updated at {lock}.")
    rich.print(
        f"[green]Packages {', '.join(names)} removed successfully and pyproject.toml updated.[/green]"
    )

def install(venv_path: str):
    """Install all dependencies from the ppmx.lock file."""
    venv: Path = Path(venv_path)
    if os.name == "nt":  # Windows
        pip_path = venv / "Scripts" / "pip.exe"
    else:  # Linux / macOS
        pip_path = venv / "bin" / "pip"

    if not pip_path.exists():
        raise FileNotFoundError(
            f"pip not found at {pip_path}. Ensure the virtual environment is set up correctly."
        )
    
    lock = Path("ppmx.lock")
    if not lock.exists():
        raise FileNotFoundError(f"Lock file {lock} does not exist.")
    
    command = f'"{pip_path}" install -r {lock}'
    print(f"Running command: {command}")
    result = os.system(command)
    if result != 0:
        raise RuntimeError(
            f"Failed to install packages from lock file. Command returned exit code {result}."
        )
    
    print(f"All dependencies installed successfully from {lock}.")
    rich.print("[green]All dependencies installed successfully.[/green]")

def update(names: list[str], venv_path: str, all: bool = False):
    """
    Update packages in the virtual environment and update the lock file and pyproject.toml.
    Args:
        names (list[str]): List of package names to update.
        venv_path (str): Path to the virtual environment.
    Raises:
        FileNotFoundError: If pip is not found in the virtual environment.
        RuntimeError: If the pip install command fails.
        Exception: For any other unexpected errors.
    """
    venv: Path = Path(venv_path)
    if os.name == "nt":  # Windows
        pip_path = venv / "Scripts" / "pip.exe"
    else:  # Linux / macOS
        pip_path = venv / "bin" / "pip"

    if not pip_path.exists():
        raise FileNotFoundError(
            f"pip not found at {pip_path}. Ensure the virtual environment is set up correctly."
        )
    if all:
        command = f'"{pip_path}" install --upgrade --force-reinstall -r ppmx.lock'
        print(f"Running command: {command}")
        result = os.system(command)
        if result != 0:
            raise RuntimeError(
                f"Failed to update all packages. Command returned exit code {result}."
            )
        names = []
    else:
        command = f'"{pip_path}" install --upgrade ' + " ".join(names)
        print(f"Running command: {command}")
        result = os.system(command)
        if result != 0:
            raise RuntimeError(
                f"Failed to update packages: {names}. Command returned exit code {result}."
            )
    lock = Path("ppmx.lock")
    cmd_freeze = [str(pip_path), "freeze"]
    freeze_output = subprocess.run(cmd_freeze, capture_output=True, text=True)

    with lock.open("w") as f:
        f.write(freeze_output.stdout)
    rich.print(
        f"[green]Packages {', '.join(names)} updated successfully and ppmx.lock updated.[/green]"
    )