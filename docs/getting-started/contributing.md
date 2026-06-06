# Contributing to Pali

We welcome contributions! Here's how you can help make Pali better.

## Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** to your local machine
3. **Create a feature branch** for your work:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Making Changes

1. **Write your code** following the existing style and patterns
2. **Add tests** for any new functionality
3. **Update documentation** if adding new features or changing behavior
4. **Run the test suite** to ensure nothing breaks:
   ```bash
   python -m pytest tests/
   # or
   bash tests.sh
   ```

## Committing Your Changes

Write clear, descriptive commit messages:

```bash
git commit -m "Add feature: description of what was added"
```

Avoid vague messages like "Fix bug" or "Updates" – be specific about what changed and why.

## Pushing and Creating a Pull Request

1. **Push to your fork**:
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Open a Pull Request** on the main repository with:
   - A clear title describing the change
   - A description of what was changed and why
   - Reference to any related issues
   - Test results showing tests pass

## Guidelines

### Code Quality
- Follow PEP 8 style guidelines
- Use meaningful variable and function names
- Add docstrings to public functions and classes
- Include inline comments for complex logic

### Testing
- Write unit tests for new functionality
- Ensure all existing tests pass
- Aim for good test coverage

### Documentation
- Update docstrings if changing function signatures
- Update relevant guide files if adding features
- Add examples if introducing new patterns

### Commit History
- Keep commits atomic and logical
- Write descriptive commit messages
- Avoid mixing unrelated changes

## Running Tests Locally

```bash
# Run all tests
bash tests.sh

# Run specific test file
python -m pytest tests/core/test_worker.py

# Run with verbose output
python -m pytest tests/ -v
```

## Getting Help

- Check existing [issues](https://github.com/gitvipin/pali/issues) to see if your idea is already discussed
- Start a [discussion](https://github.com/gitvipin/pali/discussions) for feature ideas or questions
- Review existing code for patterns and conventions

## Code of Conduct

Be respectful and constructive in all interactions. We're building this together!

---

Thank you for contributing to Pali!
