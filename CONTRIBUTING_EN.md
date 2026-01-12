# Contributing Guide

English | [中文](CONTRIBUTING.md)

Thank you for your interest in contributing to BiliVagent-tool! We welcome contributions of all kinds.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How to Contribute](#how-to-contribute)
- [Development Setup](#development-setup)
- [Commit Guidelines](#commit-guidelines)
- [Code Style](#code-style)
- [Testing](#testing)
- [Documentation](#documentation)

## Code of Conduct

This project follows the Contributor Covenant. By participating, you agree to uphold its terms. Please be friendly, respectful, and inclusive.

## How to Contribute

### Reporting Bugs

If you find a bug, please report it via GitHub Issues:

1. Use a clear title to describe the issue
2. Provide detailed reproduction steps
3. Explain expected vs. actual behavior
4. Include environment information (OS, Python version, etc.)
5. Attach error logs and screenshots if possible

### Suggesting Features

We welcome feature suggestions:

1. Check if similar suggestions exist in Issues
2. Create a new Issue with `enhancement` label
3. Clearly describe the feature and use cases
4. Explain why this feature adds value to the project

### Submitting Code

1. **Fork the Project**
   ```bash
   # Fork on GitHub
   git clone https://github.com/your-username/BiliVagent-tool.git
   cd BiliVagent-tool
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Make Changes**
   - Follow code style guidelines
   - Add necessary tests
   - Update relevant documentation

4. **Commit Changes**
   ```bash
   git add .
   git commit -m "Describe your changes"
   ```

5. **Push to Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create Pull Request**
   - Create PR on GitHub
   - Fill out PR template
   - Link related Issues

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/HeDaas-Code/BiliVagent-tool.git
cd BiliVagent-tool
```

### 2. Create Virtual Environment

```bash
# Using venv
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate  # Windows

# Or using conda
conda create -n bilivagent python=3.8
conda activate bilivagent
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
# Edit .env file with your configuration
```

### 5. Run Tests

```bash
python -m pytest tests/
```

## Commit Guidelines

We follow Conventional Commits specification:

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation updates
- `style`: Code formatting (no functional changes)
- `refactor`: Code refactoring
- `perf`: Performance improvements
- `test`: Test-related changes
- `chore`: Build process or tooling changes

### Examples

```
feat(video): add video quality selection

Added functionality for users to choose download quality, supporting 1080p, 720p, 480p

Closes #123
```

```
fix(gui): fix progress bar not updating

Progress bar would freeze in some cases, fixed with thread synchronization

Fixes #456
```

## Code Style

### Python Code Standards

We follow PEP 8:

- Use 4 spaces for indentation
- Max 88 characters per line (Black default)
- Use meaningful variable names
- Add docstrings to functions and classes
- Import order: standard library → third-party → local

### Naming Conventions

- Classes: `PascalCase`
- Functions and variables: `snake_case`
- Constants: `UPPER_SNAKE_CASE`
- Private members: `_leading_underscore`

### Docstrings

```python
def analyze_video(video_url: str) -> dict:
    """
    Analyze Bilibili video and generate report
    
    Args:
        video_url: Bilibili video URL or BV number
    
    Returns:
        Dictionary containing analysis results
    
    Raises:
        ValueError: When video URL is invalid
        APIError: When API call fails
    """
    pass
```

## Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_video.py

# Check coverage
python -m pytest --cov=bilivagent
```

### Writing Tests

- Add tests for new features
- Ensure tests cover edge cases
- Use descriptive test names
- Tests should be independent

```python
def test_parse_bv_number_from_url():
    """Test parsing BV number from URL"""
    url = "https://www.bilibili.com/video/BV1xx411c7mD"
    result = parse_bv_number(url)
    assert result == "BV1xx411c7mD"
```

## Documentation

### Updating Documentation

If your changes affect user usage, update relevant documentation:

- `README.md` / `README_EN.md`: Main documentation
- `CONTRIBUTING.md` / `CONTRIBUTING_EN.md`: Contributing guide
- `CHANGELOG.md`: Changelog
- Code comments and docstrings

### Documentation Style

- Use clear and concise language
- Provide code examples
- Include screenshots (if applicable)
- Keep Chinese and English docs in sync

## Pull Request Process

1. Ensure code passes all tests
2. Update relevant documentation
3. Describe changes in PR description
4. Link related Issues
5. Wait for code review
6. Make changes based on feedback
7. Delete branch after PR is merged

## Code Review

All submissions require code review:

- Be friendly and constructive
- Explain "why" not just "what"
- Respect different perspectives and experience levels
- Respond to feedback promptly

## Getting Help

If you have questions:

- Check existing Issues and Discussions
- Create a new Issue to ask
- Ask questions in PRs

## License

By submitting code, you agree to license your contribution under the MIT License.

---

Thank you for your contribution! 🎉
