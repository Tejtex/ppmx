"""A command-line interface for managing a Python project with a virtual
environment."""

import click
import rich

import init as init_module
import run as run_module
from package import add as add_package
from package import remove as remove_package
from package import install as install_package
from package import update as update_package
from build.lib.init import version


@click.group()
@click.option("--version", is_flag=True, help="Show the version of ppmx.")
def cli(version: bool):
    """A command-line interface for managing a Python project with a virtual
    environment."""
    if version:
        rich.print(f"[blue]ppmx version: {version}[/blue]")
        return


@cli.command()
def init():
    """Initialize the virtual environment."""
    init_module.init()

@cli.command()
@click.argument("command")
def run(command: str):
    """Run a command from the tasks defined in pyproject.toml."""

    try:
        run_module.run(command)
    except ImportError as e:
        rich.print(f"[red]Error importing module: {e}[/red]")
    except ValueError as e:
        rich.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("names", nargs=-1)
def add(names: list[str]):
    """Add packages to the virtual environment."""

    if not names:
        rich.print(
            "[red]No package names provided. Please specify at least one package.[/red]"
        )
        return

    try:
        add_package(names, venv_path="venv")
    except FileNotFoundError as e:
        rich.print(f"[red]File not found: {e}[/red]")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")

@cli.command()
@click.argument("names", nargs=-1)
def remove(names: list[str]):
    """Remove packages from the virtual environment."""

    if not names:
        rich.print(
            "[red]No package names provided. Please specify at least one\
                   package to remove.[/red]"
        )
        return

    try:
        remove_package(names, venv_path="venv")
    except FileNotFoundError as e:
        rich.print(f"[red]File not found: {e}[/red]")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")
    
@cli.command()
@click.argument("names", nargs=-1)
@click.option("--all", is_flag=True, help="Update all packages if no specific names are provided.")
def update(names: list[str], all: bool = False):
    """Update packages in the virtual environment."""

    if not names and not all:
        rich.print(
            "[red]No package names provided. Please specify at least one package to update.[/red]"
        )
        return

    try:
        update_package(names, venv_path="venv", all=all)
    except FileNotFoundError as e:
        rich.print(f"[red]File not found: {e}[/red]")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")

@cli.command()
def install():
    """Install all dependencies from the ppmx.lock file."""
    install_package(venv_path="venv")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        rich.print(f"[red]Error:[/red] {e}")
