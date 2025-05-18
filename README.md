# AMM Agno Memory Modules

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Advanced Memory Management (AMM) for the Agno platform, providing efficient storage, retrieval, and management of AI interaction data and knowledge bases.

## ✨ Features

- **Adaptive Memory Engine**: Efficient storage and retrieval of interaction data
- **Vector Database Integration**: Seamless integration with LanceDB for semantic search
- **Multi-Model Support**: Compatible with various LLM providers (OpenAI, Anthropic, Google AI)
- **Production-Ready**: Built with FastAPI for high-performance API serving
- **Scalable**: Designed for both small-scale applications and enterprise deployments

## 🚀 Quick Start

### Prerequisites

- [Miniconda](https://docs.conda.io/en/latest/miniconda.html) or [Anaconda](https://www.anaconda.com/products/distribution)
- Python 3.12
- CUDA 12.1+ (for GPU acceleration)
- NVIDIA GPU with compute capability 7.0+ (recommended)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/AMM_Agno_Memory_Modules.git
   cd AMM_Agno_Memory_Modules
   ```

2. **Set up the conda environment**
   ```bash
   # Create and activate the environment
   conda env create -f environment.yml
   conda activate amm-agno
   
   # Install in development mode
   pip install -e .
   ```

3. **Verify the installation**
   ```bash
   python -c "import torch; print(f'PyTorch version: {torch.__version__}')"
   python -c "import lancedb; print(f'LanceDB version: {lancedb.__version__}')"
   ```

## 🏗 Project Structure

```
AMM_Agno_Memory_Modules/
├── amm_project/           # Core package
│   ├── config/           # Configuration management
│   ├── engine/           # Core AMM engine implementation
│   └── models/           # Data models and schemas
├── tests/                # Test suite
│   └── unit/             # Unit tests
├── environment.yml       # Conda environment specification
├── requirements.txt      # Python dependencies
└── setup.py             # Package configuration
```

## 🧪 Running Tests

```bash
# Run all tests
pytest tests/

# Run tests with coverage report
pytest --cov=amm_project tests/

# Generate HTML coverage report
pytest --cov=amm_project --cov-report=html tests/
```

## 🛠 Development

### Code Style

We use `black` for code formatting and `isort` for import sorting. Pre-commit hooks are available to automate this:

```bash
# Install pre-commit hooks
pre-commit install

# Run against all files
pre-commit run --all-files
```

### Dependency Management

1. **Adding a new dependency**:
   - Add to `environment.yml` for conda packages
   - Add to `requirements.txt` for pip packages
   - Update the environment:
     ```bash
     conda env update --file environment.yml --prune
     ```

2. **Updating dependencies**:
   ```bash
   conda env export --from-history > environment.yml
   pip freeze > requirements.txt
   ```

## 📚 Documentation

For detailed documentation, please refer to:
- [API Reference](docs/api.md)
- [Configuration Guide](docs/configuration.md)
- [Deployment Guide](docs/deployment.md)

## 🤝 Contributing

Contributions are welcome! Please read our [Contributing Guide](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 📬 Contact

For questions or support, please open an issue on GitHub or contact the maintainers.
