"""A command-line interface for managing a Python project with a virtual
environment."""

import click
import rich

import init as init_module
import run as run_module
from package import add as add_package
from package import remove as remove_package
from package import install as install_package


@click.group()
def cli():
    """A command-line interface for managing a Python project with a virtual
    environment."""
    pass


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
        raise click.ClickException("Failed to import the required module.")
    except ValueError as e:
        rich.print(f"[red]Error: {e}[/red]")


@cli.command()
@click.argument("names", nargs=-1)
def add(names: list[str]):
    """Add packages to the virtual environment."""

    if not names:
        rich.print(
            "[red]No package names provided. Please specify at least one\
                   package.[/red]"
        )
        return

    try:
        add_package(names, venv_path="venv")
    except FileNotFoundError as e:
        rich.print(f"[red]File not found: {e}[/red]")
        raise click.ClickException("The specified file was not found.")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
        raise click.ClickException(
            "An error occurred while installing\
                                    packages."
        )
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise click.ClickException(
            "An unexpected error occurred while adding packages."
        )

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
        raise click.ClickException("The specified file was not found.")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
        raise click.ClickException(
            "An error occurred while removing packages."
        )
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise click.ClickException(
            "An unexpected error occurred while removing packages."
        )

@cli.command()
def install():
    """Install all dependencies from the ppmx.lock file."""
    install_package(venv_path="venv")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        rich.print(f"[red]Error:[/red] {e}")
        raise click.ClickException(
            "An error occurred while executing\
                                    the command."
        )
