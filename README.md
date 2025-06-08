<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/SpaceShaman/epub-translate/refs/heads/master/assets/logo-light.png" width="100" alt="epub-translate">
    <img src="https://raw.githubusercontent.com/SpaceShaman/epub-translate/refs/heads/master/assets/logo-dark.png" width="100" alt="epub-translate">
  </picture>
  <p><strong>epub-translate:</strong> a simple cli tool for translating ebooks in EPUB format into any language</p>
</div>

----
<div align="center">

[![GitHub License](https://img.shields.io/github/license/SpaceShaman/epub-translate)](https://github.com/SpaceShaman/epub-translate?tab=MIT-1-ov-file)
[![Tests](https://img.shields.io/github/actions/workflow/status/SpaceShaman/epub-translate/release.yml?label=tests)](https://app.codecov.io/github/SpaceShaman/epub-translate)
[![Codecov](https://img.shields.io/codecov/c/github/SpaceShaman/epub-translate)](https://app.codecov.io/github/SpaceShaman/epub-translate)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/epub-translate)](https://pypi.org/project/epub-translate)
[![PyPI - Version](https://img.shields.io/pypi/v/epub-translate)](https://pypi.org/project/epub-translate)
[![Typer](https://img.shields.io/badge/cli-Typer-blue?logo=typer&logoColor=blue)](https://typer.tiangolo.com/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-black)](https://github.com/psf/black)
[![Linting: Ruff](https://img.shields.io/badge/linting-Ruff-black?logo=ruff&logoColor=black)](https://github.com/astral-sh/ruff)
[![Pytest](https://img.shields.io/badge/testing-Pytest-red?logo=pytest&logoColor=red)](https://docs.pytest.org/)

</div>

## Installation

You can install `epub-translate` using pip:

```bash
pip install epub-translate
```

## Usage

You can use `epub-translate` from the command line:

```bash
epub-translate translate <input_file> <output_language>
```

## Configuration

Before you can use `epub-translate`, you need to configure it with your OpenAI API key. You can do this using the following command:

```bash
epub-translate configure --api-key <your_openai_api_key>
```

You can also set the specific model you want to use for translation:

```bash
epub-translate configure --model <your_model_name>
```
