# Changelog

All notable changes to Pali are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- [To be determined based on ongoing development]

### Changed
- [To be determined based on ongoing development]

### Fixed
- [To be determined based on ongoing development]

### Deprecated
- [To be determined based on ongoing development]

### Removed
- [To be determined based on ongoing development]

### Security
- [To be determined based on ongoing development]

---

## [0.0.6] - Initial Release

### Added

#### Core ThreadPool System
- ThreadPool implementation with configurable worker threads
- WorkerThread class for handling task execution
- Task-based parallel processing model
- Context manager support for automatic resource cleanup
- Task queueing with configurable queue size
- Worker thread management (enable/disable/stop)

#### Task System
- Abstract Task base class with `_run()` implementation pattern
- Task lifecycle management (NEW, READY, RUNNING, FINISHED states)
- Task priority support for custom ordering
- Self-contained task pattern with attribute-based result storage

#### Pipeline System
- Pipeline and Stage abstractions for sequential workflows
- Assembly pattern for running multiple pipelines in parallel
- Shared data dictionary for inter-stage communication
- Pipeline error handling and logging
- Stage execution ordering and state management

#### Configuration Management
- ConfigManager for INI-based configuration files
- Section-based configuration organization
- Type-safe parameter handling (string, int, float, bool)
- Configuration file parsing with defaults
- Parameter override support

#### Parameter System
- Parameter management with type checking
- A/B testing support with parameter values
- A/B value cycling (round-robin distribution)
- Enable/disable A/B testing per parameter
- Global parameter collection (PARAMS)

#### Logging System
- Integrated logging setup function
- Log level configuration
- File-based logging with auto-directory creation
- Per-module log level control
- Thread-aware log formatting

#### Utilities
- BBuffer (Balanced Buffer) utility module
- Common queue abstractions
- Logger wrapper utilities
- Constants module for default configurations

#### Examples
- ThreadPool usage examples (stock.py, party.py, bbuffer.py, ovftool.py)
- Task creation and execution patterns
- Pipeline and stage implementations

#### Testing
- Comprehensive test suite
- Worker pool tests
- ThreadPool functionality tests
- Task execution tests
- Configuration tests
- Parameter and A/B testing tests
- BBuffer utility tests

### Documentation
- MIT License
- README with basic usage examples
- Release notes documenting features

---

## Version History

### 0.0.6 (Current)
- Initial release with core ThreadPool, Task, Pipeline, Configuration, and A/B Testing capabilities

---

## How to Contribute

When adding changes to Pali, please update this CHANGELOG with:

1. **Added** - New features
2. **Changed** - Changes in existing functionality
3. **Fixed** - Bug fixes
4. **Deprecated** - Soon-to-be removed features
5. **Removed** - Now removed features
6. **Security** - Security fixes or improvements

Each release should have its own section with date in [YYYY-MM-DD] format.

---

## Support

For issues, feature requests, or questions, please visit:
- GitHub Issues: https://github.com/gitvipin/pali/issues
- GitHub Discussions: https://github.com/gitvipin/pali/discussions

---

## Links

- [GitHub Repository](https://github.com/gitvipin/pali)
- [PyPI Package](https://pypi.org/project/pali/)
- [Documentation](../README.md)
