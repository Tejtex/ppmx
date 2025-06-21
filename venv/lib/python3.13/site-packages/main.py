import click
import rich
import questionary
import init as init_module
import run as run_module

@click.group()
def cli():
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

    if not names:
        rich.print("[red]No package names provided. Please specify at least one package.[/red]")
        return

    try:
        from package import add as add_package
        add_package(names, venv_path="venv") 
    except ImportError as e:
        rich.print(f"[red]Error importing package module: {e}[/red]")
        raise click.ClickException("Failed to import the package module.")
    except FileNotFoundError as e:
        rich.print(f"[red]File not found: {e}[/red]")
        raise click.ClickException("The specified file was not found.")
    except RuntimeError as e:
        rich.print(f"[red]Runtime error: {e}[/red]")
        raise click.ClickException("An error occurred while installing packages.")
    except Exception as e:
        rich.print(f"[red]An unexpected error occurred: {e}[/red]")
        raise click.ClickException("An unexpected error occurred while adding packages.")

if __name__ == "__main__":
    try:
        cli()
    except Exception as e:
        rich.print(f"[red]Error:[/red] {e}")
        raise click.ClickException("An error occurred while executing the command.")