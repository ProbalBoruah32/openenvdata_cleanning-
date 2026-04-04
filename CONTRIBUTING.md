# Contributing to Data Cleaning OpenEnv Environment

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

Please be respectful and inclusive in all interactions. We are committed to providing a welcoming and inspiring community for all.

## How to Contribute

### 1. Reporting Bugs

Before creating bug reports, check the issue list as you might find that you don't need to create one. When you create a bug report, include as many details as possible:

- Use a clear, descriptive title
- Describe the exact steps to reproduce the problem
- Provide specific examples to demonstrate the steps
- Describe the behavior you observed after following the steps
- Explain which behavior you expected to see instead
- Include screenshots if applicable
- Run `python validator.py` and include the output

### 2. Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion:

- Use a clear, descriptive title
- Provide a step-by-step description of the suggested enhancement
- Provide specific examples to demonstrate the steps
- Describe the current behavior and expected behavior
- Explain why this enhancement would be useful

### 3. Pull Requests

- Fork the repository and create your branch from `main`
- If you've added code that should be tested, add tests
- Ensure your code passes the validator: `python validator.py`
- Test inference: `python inference.py`
- Follow the existing code style
- Write clear, descriptive commit messages
- Include references to any related issues

### 4. Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/data-cleaning-env.git
cd data-cleaning-env

# Create virtual environment
python -m venv .venv

# Activate (Windows)
.venv\Scripts\Activate.ps1

# Activate (Linux/Mac)
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run validator
python validator.py

# Run tests
python inference.py
```

### 5. Code Guidelines

- Follow PEP 8 style guide
- Use type hints where applicable
- Write descriptive docstrings
- Keep functions focused and single-purpose
- Add comments for complex logic

### 6. OpenEnv Compliance

Any changes must maintain OpenEnv specification compliance:

- `openenv.yaml` must remain valid
- API endpoints must follow specification
- Models must have proper type hints
- Graders must return scores in [0.0, 1.0] range
- Tasks must be reproducible and deterministic

### 7. Testing

```bash
# Run validator (must pass)
python validator.py

# Test inference
python inference.py

# Test API endpoints
curl http://localhost:8000/reset
curl http://localhost:8000/tasks

# Build Docker
docker build -t data-cleaning-env:test .
```

## Commit Message Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

Types: feat, fix, docs, style, refactor, test, chore

Example:
```
feat(grader): add semantic similarity scoring

This adds advanced semantic similarity checking for text normalization.

Closes #123
```

## Pull Request Process

1. Update README.md with any new features
2. Update openenv.yaml if API changes
3. Increase version number following SemVer
4. Ensure validator passes all checks
5. Request review from maintainers
6. Address any review feedback

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- MAJOR: Breaking API changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

## Questions?

- Join our discussions on GitHub
- Open an issue with the `question` label
- Contact maintainers

---

**Thank you for contributing!**
