"""
Run a task from the pyproject.toml file
"""

import pathlib
import subprocess
import toml

import rich

# pylint: skip-file


def run(command: str):
    """
    Run the task defined in the pyproject.toml file.
    Args:
        command (str): The name of the command to run, as defined in the tasks section of pyproject.toml.
    Raises:
        ValueError: If the command is not found in the tasks section of pyproject.toml.
        subprocess.CalledProcessError: If the command fails to execute.
    """

    cwd = pathlib.Path.cwd()

    file = toml.load(cwd.joinpath("pyproject.toml"))

    tasks = file["tool"]["ppmx"]["tasks"]

    if command in tasks:
        cmd = tasks[command]["command"]
        rich.print(f"[blue]Running command:[/blue] {cmd}")
        try:
            subprocess.run(cmd, shell=True, check=True)
            rich.print(f"[green]Command '{cmd}' executed successfully.[/green]")
        except subprocess.CalledProcessError as e:
            rich.print(f"[red]Error executing command '{cmd}': {e}[/red]")
    else:
        rich.print(f"[red]Command '{command}' not found in tasks.[/red]")
        raise ValueError(f"Command '{command}' not found in tasks.")
