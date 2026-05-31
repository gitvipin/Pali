# Documentation Examples Tests

This directory contains comprehensive test coverage for all code examples and snippets mentioned in the Pali documentation.

## Purpose

These tests serve as **verification tests** to ensure that every example shown in the documentation actually works as described. This prevents documentation drift and ensures users can rely on all examples being accurate and functional.

## Test Files

### 1. `test_quick_start_examples.py`
Tests all examples from `docs/getting-started/quick-start.md`
- Basic greeting task execution
- Number squaring task
- Thread pool basic usage
- Context manager proper cleanup

### 2. `test_tasks_examples.py`
Tests all examples from `docs/guide/tasks.md`
- Task lifecycle and states
- Simple data processing (square numbers)
- HTTP request tasks with mocking
- Database operations with SQLite
- Error handling in tasks

### 3. `test_thread_pool_examples.py`
Tests all examples from `docs/guide/thread-pool.md`
- Thread pool creation (single and multi-threaded)
- Context manager usage (recommended)
- ThreadPool parameters and configuration
- ThreadPool interface methods (append_task, remaining, finished, get_workers, close)
- Manual pool management
- Task lifecycle in pools

### 4. `test_logging_examples.py`
Tests all examples from `docs/guide/logging.md`
- Basic logging setup
- Custom logging configuration
- All logging levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- Formatted log messages
- Log directory and file configuration
- Multiple logger instances

### 5. `test_configuration_examples.py`
Tests all examples from `docs/guide/configuration.md`
- ConfigManager creation and loading
- Reading configuration values with type conversion
- Working with configuration sections
- Listing options and checking existence
- Edge cases and error handling
- Different value types (string, numeric, boolean)

### 6. `test_ab_testing_examples.py`
Tests all examples from `docs/guide/ab-testing.md`
- Basic A/B testing with enabled/disabled
- Integer, float, and string parameter types
- Multiple A/B parameters
- Distribution and cycling behavior
- Edge cases (single value, two values)
- Type preservation

### 7. `test_pipeline_examples.py`
Tests all examples from `docs/guide/pipeline.md`
- Stage creation and execution
- Validation, processing, and output stages
- Pipeline creation and execution
- Data sharing between stages
- Stage ordering
- Assembly creation and execution
- Multiple pipelines with ThreadPool
- Complex scenarios (data transformation, conditional processing)

## Running the Tests

### Run all documentation example tests:
```bash
python -m unittest discover -s tests/test_examples_from_docs -p "test_*.py" -v
```

### Run a specific test file:
```bash
python -m unittest tests.test_examples_from_docs.test_quick_start_examples -v
```

### Run a specific test class:
```bash
python -m unittest tests.test_examples_from_docs.test_quick_start_examples.TestQuickStartGreeting -v
```

### Run a specific test method:
```bash
python -m unittest tests.test_examples_from_docs.test_quick_start_examples.TestQuickStartGreeting.test_greeting_task_basic -v
```

## Test Design

- **No external dependencies**: All tests use `unittest` (Python standard library)
- **Isolation**: Each test is independent and can run in any order
- **Mocking**: External services (HTTP, database) are mocked for reliability
- **Fixtures**: Temporary directories are used for file-based tests
- **Comprehensive coverage**: Every code snippet in documentation is tested

## Adding New Examples

When you add new examples to the documentation:

1. Identify which guide section they belong to
2. Create or update the corresponding test file
3. Write test(s) that verify the example works exactly as shown in docs
4. Use appropriate assertions (assertEqual, assertIn, assertTrue, etc.)
5. Mock external services to keep tests isolated and fast
6. Run the tests to verify they pass

## Test Organization Structure

```
tests/test_examples_from_docs/
├── __init__.py                          # Package marker
├── README.md                            # This file
├── test_quick_start_examples.py         # Quick start guide tests
├── test_tasks_examples.py               # Tasks guide tests
├── test_thread_pool_examples.py         # Thread pool guide tests
├── test_logging_examples.py             # Logging guide tests
├── test_configuration_examples.py       # Configuration guide tests
├── test_ab_testing_examples.py          # A/B testing guide tests
└── test_pipeline_examples.py            # Pipeline guide tests
```

## Benefits

✅ **Documentation Accuracy**: Examples are guaranteed to work
✅ **Regression Detection**: Changes that break examples are caught immediately
✅ **User Confidence**: Users know all examples in docs are tested
✅ **Maintainability**: Easy to update examples and tests together
✅ **Learning Aid**: Tests serve as working references for features
✅ **Quality Assurance**: No example drift between documentation and reality
