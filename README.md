# Auto PR Tag Ruff

A simple Python project template with Poetry and Ruff.

## Features

- 📦 **Poetry** for dependency management
- 🧹 **Ruff** for fast Python linting and formatting
- 🧪 **Pytest** for testing with coverage
- 🚀 **GitHub Actions** for CI/CD

## Prerequisites

- Python 3.8 or higher
- [Poetry](https://python-poetry.org/docs/#installation) installed

## Getting Started

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd auto-pr-tag-ruff
   ```

2. **Install dependencies**
   ```bash
   poetry install
   ```

3. **Activate the virtual environment**
   ```bash
   poetry shell
   ```

## Development

### Running the application

```bash
poetry run python -m auto_pr_tag_ruff.main
```

### Running tests

```bash
poetry run pytest
```

With coverage:
```bash
poetry run pytest --cov
```

### Linting and formatting

Check code with Ruff:
```bash
poetry run ruff check .
```

Format code with Ruff:
```bash
poetry run ruff format .
```

## Project Structure

```
auto-pr-tag-ruff/
├── src/
│   └── auto_pr_tag_ruff/
│       ├── __init__.py
│       └── main.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── .gitignore
├── pyproject.toml
└── README.md
```

## License

This project is licensed under the MIT License.