# ppmx – The Best Package Manager for Python
![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Status](https://img.shields.io/badge/status-alpha-red)
![Platform](https://img.shields.io/badge/platform-cross--platform-lightgrey)
![Coverage](https://img.shields.io/badge/coverage-100%25-brightgreen)
![Downloads](https://img.shields.io/badge/downloads-∞-blueviolet)
**Ppmx** is a simple, user-friendly package manager for Python.  
It aims to make managing dependencies and project scripts easier and cleaner.

## Features

- Easy CLI interface  
- Project initialization (`ppmx init`)  
- Dependency management (`ppmx add`)  
- Task runner from `pyproject.toml` (`ppmx run`)  
- Minimal setup, no boilerplate

## Installation

To install `ppmx`, clone the repository and run:

```bash
pip install .
```

Once installed, you can use `ppmx` directly from the command line.

## Usage

To create a new project with `ppmx`:

```bash
mkdir my-project
cd my-project
ppmx init
```

Then you can:

```bash
ppmx add <dependency>   # Add dependencies
ppmx run <task>         # Run a task from pyproject.toml
```

## Contributions

If you'd like to contribute to **ppmx**, please follow these guidelines:

- Fork the repository, make your changes, and submit a pull request.
- Keep your commits clear and focused.
- Provide detailed descriptions in your pull requests.
- Ensure all tests pass and coverage stays consistent before submitting.

## Issues

- Feel free to open an issue if you find a bug or have a feature request.
- Please include clear descriptions and examples to help us understand the problem.

## License

This project is licensed under the MIT License. You’re free to use, modify, and distribute it, but please give appropriate credit.

---

Thanks for helping improve **ppmx**!
