"""Initialize the virtual environment and create project files."""

import pathlib
import venv

import questionary
import rich


def init():
    """
    Initialize the virtual environment.
    Create the necessary project files including README.md, pyproject.toml,
    and src/main.py.
    Optionally initialize a Git repository.
    This function prompts the user for various project details such as
    project name, author, description, and license type.
    It also creates a virtual environment in the specified path
    and sets up a basic project structure.
    """

    cwd = pathlib.Path.cwd()
    path = questionary.text(
        "Enter the path to the virtual environment (default: ./venv):", default="./venv"
    ).ask()

    venv.create(path, with_pip=True)
    rich.print(f"[green]Virtual environment created at {path}[/green]")
    create_readme = questionary.confirm("Create README.md?", default=True).ask()
    if create_readme:

        cwd.joinpath("README.md").touch()
        rich.print("[green]README.md file created.[/green]")

    project_name = questionary.text("Project name:", default=cwd.name).ask()
    author = questionary.text("Author:", default="someone").ask()
    description = questionary.text("Description:").ask()
    license_type = questionary.select(
        "License type:",
        choices=["MIT", "Apache-2.0", "GPL-3.0", "BSD-3-Clause", "None"],
        default="MIT",
    ).ask()

    with open(cwd.joinpath("pyproject.toml"), "w", encoding="UTF-8") as file:
        file.write(
            f"""[project]
name = "{project_name}"
version = "0.1.0"
description = "{description}"
authors = ["{author}"]
license = "{license_type}"
dependencies = []
[build-system]
requires = ["setuptools", "wheel"]
build-backend = "setuptools.build_meta"
[tool.ppmx]
venv_path = "{path}"
[tool.ppmx.tasks.dev]
command = "python src/main.py"
[tool.ppmx.tasks.test]
command = "pytest" """
        )
    rich.print("[green]pyproject.toml file created.[/green]")

    git = questionary.confirm("Initialize a Git repository?", default=True).ask()
    if git:
        try:
            import git  # pylint: disable=import-outside-toplevel

            git.Repo.init(cwd)
            rich.print("[green]Git repository initialized.[/green]")
        except ImportError:
            rich.print(
                "[red]GitPython is not installed. \
                    Skipping Git initialization.[/red]"
            )
        except Exception as error:  # pylint: disable=broad-except
            rich.print(
                f"[red]Error initializing Git repository:\
                        {error}[/red]"
            )

    cwd.joinpath("ppmx.lock").touch()
    rich.print("[green]ppmx.lock file created.[/green]")
    cwd.joinpath("src").mkdir(exist_ok=True)
    rich.print("[green]src directory created.[/green]")
    cwd.joinpath("src", "main.py").touch()
    rich.print("[green]src/main.py file created.[/green]")

    rich.print("[green]Project initialized successfully![/green]")
