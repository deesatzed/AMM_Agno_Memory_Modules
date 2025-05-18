# AMM Agno Memory Modules

This repository contains the core AMM (Adaptive Memory Module) engine and models for the Agno platform.

## Structure

- `amm_project/`: Core package
  - `engine/`: AMM engine implementation
  - `models/`: Data models and schemas
  - `config/`: Configuration management
- `tests/`: Unit and integration tests

## Prerequisites

- Miniconda or Anaconda distribution
- Python 3.8 or higher

## Setup with Conda

1. **Create and activate the conda environment** (using the provided `environment.yml`):

```bash
# Create and activate the environment
conda env create -f environment.yml
conda activate amm-agno

# Install the package in development mode
pip install -e .
```

Alternatively, if you prefer to create the environment manually:

```bash
# Create a new conda environment
conda create -n amm-agno python=3.10
conda activate amm-agno

# Install dependencies
conda install --file requirements.txt

# Install development dependencies
conda install pytest pytest-cov pre-commit black isort mypy flake8

# Install the package in development mode
pip install -e .
```

## Running Tests

```bash
# Make sure you're in the activated conda environment
conda activate amm-agno

# Run all tests
pytest tests/

# Run tests with coverage report
pytest --cov=amm_project tests/
```

## Development

### Setting up pre-commit hooks (optional but recommended)

```bash
conda install -c conda-forge pre-commit
pre-commit install
```

### Updating Dependencies

1. Add new dependencies to `requirements.txt`
2. Update the conda environment:

```bash
conda env update --file environment.yml --prune
```

## License

This project is licensed under the terms of the MIT license. See the [LICENSE](LICENSE) file for details.
