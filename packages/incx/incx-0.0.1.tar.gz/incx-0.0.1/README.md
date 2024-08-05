# Incx

IncX (**Inc**remental E**x**planations) is an innovative approach designed to incrementally generate saliency maps and explanations in real-time.

![Penguin Gif](blob/penguin.gif)

## Getting Started

To run this project, you will need to use `pyenv` for Python version management and `poetry` for dependency management. Below are the steps to set up your environment and run the project.

### Prerequisites

1. **Pyenv Installation**  
   Pyenv is a tool for managing multiple versions of Python on your system. Follow the instructions below to install it:
   
   - **Linux and macOS:** Follow the instructions in the [pyenv GitHub repository](https://github.com/pyenv/pyenv?tab=readme-ov-file#getting-pyenv) to install pyenv.
   - **Windows:** Use [pyenv-win](https://github.com/pyenv-win/pyenv-win?tab=readme-ov-file#installation) to install pyenv for Windows.

2. **Installing Python Version**  
   Once pyenv is installed, use it to install the Python version specified in the `.python-version` file located in the root directory of this project. Run the following command:

   ```shell
   pyenv install
   ```

3. Install [poetry](https://python-poetry.org/docs/#installation)

4. Configure poetry to create virtual environments in the current project directory. This will ensure that you can easily handle different environments for different projects.

   ```shell
   poetry config virtualenvs.in-project true
   ```

5. Use poetry to install the project dependencies and create a virtual environment:

   ```shell
   poetry install
   ```


## Experiments

To replicate the experiments comparing D-RISE and IncX, follow these steps:

1. 
poetry run pytest --cov=incrementalexplainer --cov-report=term-missing

python experiments/d_rise/get_blob_names.py

python experiments/d_rise/get_metrics.py

poetry run python experiments/incx/get_job_names.py

python experiments/incx/get_saliency_maps.py

# Unit Tests

To ensure the code is working correctly and is well-covered by tests, run the following command using poetry and pytest:

```shell
poetry run pytest
```
This command will execute all the tests defined in the `tests/` directory, providing feedback on code correctness and coverage.

# Linting and Formatting

To maintain code quality and style consistency, use the following commands:

1. **Linting**
    Use `ruff` to check for code issues and automatically fix them:

    ```shell
    poetry run ruff check . --fix
    ```
2. **Formatting**
    Use `ruff` to format the code according to style guidelines:

    ```shell
    poetry run ruff format .
    ```

# How to install the package

```shell
pip install incx
```