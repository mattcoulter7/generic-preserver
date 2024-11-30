# mclib-sdk-python-template
This repository is a template for `mclib` packages, available both as a Command-Line Interface (CLI) and as a Python Package Dependency.

## Running the Application
The CLI application can currently be run **three** different environments:
- CLI
- Windows Executable
- Docker Container

Please ensure you system is setup with the following, for each environment respectively:

### Assumptions
To run this application, we assume you have the following setup system environment setup already:

1. For **CLI**:
   - **Python version**: Ensure Python 3.12.x is installed:
      ```bash
      py -3.12 --version
      ```
   - **Pip installation**: Make sure pip is installed:
      ```bash
      py -3.12 -m ensurepip
      ```
   - **Update pip**: Upgrade pip to the latest version:
      ```bash
      py -3.12 -m pip install --upgrade pip
      ```
   - **Install Poetry**: Install the Poetry package manager:
      ```bash
      py -3.12 -m pip install poetry
      ```
2. For **[Optional] Docker (*for docker environment only*)**:
   - **Docker**: Ensure Docker compose is available in the command line.
   - **Docker Compose**: Ensure Docker compose is available in the command line.
3. For **[Optional] Windows (*for Windows Executable environment only*)**:
   - **Support for .exe**: Ensure you can run windows executables.

### How to run the code
Start by cloning this repository:
```bash
git clone https://github.com/mattcoulter7/mclib-sdk-python-template
cd mclib-sdk-python-template
```

#### CLI
To run the CLI, first set up the environment:

1. **Install dependencies**: Install project dependencies:
   ```bash
   py -3.12 -m poetry install --with dev --extras *
   ```

Once the environment is set, you can explore the available commands by running:
```bash
py -3.12 -m poetry run mclib_template --help
```

To run the application in interactive mode:
```bash
py -3.12 -m poetry run mclib_template
```

Alternatively, calculate the output with a single command:
```bash
py -3.12 -m poetry run mclib_template --input-1 some_string --input-2 0.
```

#### Windows Executable

For Windows users, the compiled executable is available for download from the zip file in the [latest release](https://github.com/mattcoulter7/mclib-sdk-python-template/releases).

After unzipping, run the executable and the cli will run in interactive mode.

#### Docker Container

You can also run the application within a Docker container:
```bash
docker compose -f docker-compose.yml up --build
```
*Note: The Docker container runs in non-interactive mode, and inputs are hardcoded in the Docker Compose file.*

---

## Using this repository as a python package

To incorporate this package into your own python application, add this package as a dependency via the Github link.

### Installation

Install the package using pip as a git dependency:
```bash
pip install "git+https://github.com/mattcoulter7/mclib-sdk-python-template@master"
```

If you are using poetry, you can specify this git dependency like so:
```bash
[tool.poetry.dependencies]
mclib-sdk-python-template = { git = "https://github.com/mattcoulter7/mclib-sdk-python-template.git", tag= "0.1.0", extras = ["*"] }
```

### Usage Example
Then, you can use the code like below
```python
from mclib.template import ...

# TODO
```

---

## Development

### Running Tests

Tests are located in the `./tests` directory. To run the tests:
```bash
pytest
```

Alternatively, you can run tests within a Docker container for a release build:
```bash
docker compose -f docker-compose.yml up --build
```
