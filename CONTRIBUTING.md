# Contributing Guidelines

Thank you for considering contributing to this project. This document outlines the process and standards for contributions.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Testing Requirements](#testing-requirements)
- [Pull Request Process](#pull-request-process)
- [Commit Message Format](#commit-message-format)

---

## Code of Conduct

This project adheres to a Code of Conduct that all contributors are expected to follow. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

---

## Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key (for testing)

### Development Setup

```bash
# Fork and clone the repository
git clone https://github.com/YOUR_USERNAME/arg-surveillance-framework.git
cd arg-surveillance-framework

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Configure environment
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Verify setup
pytest
```

---

## Development Process

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch for features
- `feature/*` - New features
- `fix/*` - Bug fixes
- `docs/*` - Documentation updates

### Workflow

1. Create a feature branch from `develop`
2. Implement your changes
3. Write/update tests
4. Update documentation
5. Submit pull request to `develop`

Example:
```bash
git checkout develop
git pull origin develop
git checkout -b feature/your-feature-name

# Make changes
git add .
git commit -m "feat: add new feature"
git push origin feature/your-feature-name
```

---

## Coding Standards

### Python Style

This project follows [PEP 8](https://peps.python.org/pep-0008/) with enforcement via Black and Ruff.

**Formatting:**
```bash
# Format code
black app/

# Check linting
ruff check app/

# Type checking
mypy app/
```

**Code Structure:**
```python
# Standard library imports
import os
import json
from typing import Dict, Any, Optional

# Third-party imports
from fastapi import FastAPI
from pydantic import BaseModel

# Local imports
from app.llm import call_llm
from app.guards import check_guardrails


def function_name(
    param1: str,
    param2: int,
    optional_param: Optional[str] = None
) -> Dict[str, Any]:
    """
    Brief description of function.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        optional_param: Description of optional parameter
        
    Returns:
        Dictionary containing function results
        
    Raises:
        ValueError: If params are invalid
    """
    # Implementation
    pass
```

### Documentation

**Docstrings:**
- Required for all public functions and classes
- Use Google-style format
- Include type hints in function signatures

**Comments:**
- Explain why, not what
- Keep comments up-to-date with code
- Use inline comments sparingly

---

## Testing Requirements

### Test Coverage

- Minimum 80% code coverage
- All new features must include tests
- Bug fixes should include regression tests

### Writing Tests

```python
# tests/test_agents/test_a1_sampling.py
import pytest
from app.agents.a1_sampling import run_sampling_agent


def test_valid_query_returns_success():
    """Test agent handles valid query correctly."""
    query = "Design ARG surveillance study"
    output = run_sampling_agent(query)
    
    assert output["status"] == "success"
    assert "structured_output" in output


@pytest.mark.parametrize("query,expected_type", [
    ("hospital wastewater", "hospital"),
    ("agricultural soil", "farm"),
])
def test_system_classification(query, expected_type):
    """Test agent classifies study systems correctly."""
    output = run_sampling_agent(f"Design study in {query}")
    assert expected_type in output["raw_output"].lower()
```

### Running Tests

```bash
# Full test suite
pytest

# Specific test file
pytest tests/test_agents.py

# With coverage report
pytest --cov=app --cov-report=html

# Verbose output
pytest -v
```

---

## Pull Request Process

### Before Submitting

1. Update documentation for any changed functionality
2. Add tests for new features
3. Ensure all tests pass
4. Run code formatters and linters
5. Update CHANGELOG.md

### PR Title Format

Use conventional commit format:
- `feat: add new feature`
- `fix: resolve bug`
- `docs: update documentation`
- `refactor: restructure code`
- `test: add tests`

### PR Description Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Related Issues
Closes #123

## Changes Made
- Change 1
- Change 2

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] Tests added/updated
```

### Review Process

- All PRs require at least one approval
- CI/CD checks must pass
- Conflicts must be resolved
- Address reviewer feedback promptly

---

## Commit Message Format

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test updates
- `chore`: Build/tool changes

**Examples:**
```bash
feat(agents): add literature review agent

Implement new agent for automated literature search and
citation extraction from PubMed database.

Closes #42

---

fix(api): resolve timeout in async workflow

Add timeout configuration and improved error handling
for long-running workflows.

Fixes #38
```

---

## Issue Guidelines

### Bug Reports

Include:
- Clear description
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Error logs

### Feature Requests

Include:
- Use case description
- Proposed solution
- Alternative solutions considered
- Impact assessment

---

## Development Best Practices

### Code Quality

- Write self-documenting code
- Keep functions focused and small
- Avoid deep nesting
- Handle errors appropriately
- Use type hints

### Performance

- Profile before optimizing
- Document performance-critical sections
- Consider algorithmic complexity
- Test with realistic data sizes

### Security

- Never commit API keys or secrets
- Validate all user inputs
- Use parameterized queries
- Follow security best practices

---

## Getting Help

- Review existing documentation
- Check closed issues for similar problems
- Ask questions in GitHub Discussions
- Contact maintainers via email

---

## Recognition

Contributors will be:
- Listed in project documentation
- Mentioned in release notes
- Credited in academic citations

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
