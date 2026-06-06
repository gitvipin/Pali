[![Downloads](https://pepy.tech/badge/pali)](https://pepy.tech/project/pali)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-2.7%2B%2C%203.4%2B-blue.svg)](#requirements)

# Pali

**Pali (Python Applications Lightweight Initiator)** is a dependency-free application foundation library for Python.

It provides a collection of reusable infrastructure components and software patterns that commonly appear across Python applications, whether they are simple automation scripts, cron jobs, backend services, integration solutions, or production microservices.

Instead of repeatedly implementing the same foundational capabilities in every project, developers can leverage Pali's lightweight building blocks for:

* Configuration management
* Logging standardization
* Persistence and state management
* Daemon and service lifecycle management
* Concurrent execution and thread pools
* Assembly and pipeline processing
* Sliding window protocols
* A/B testing and experimentation

Pali is implemented entirely in native Python and intentionally avoids third-party dependencies. The result is a lightweight, portable, and easy-to-understand library that can be adopted incrementally without introducing a bulky framework with runtime and dependencies footprint.

Originally developed as a ThreadPool implementation for Python 2.7, Pali has evolved into a broader collection of production-tested utilities that address recurring challenges in real-world Python applications.


## Quick Links

- **[Documentation](docs/README.md)** - Full guides and API reference
- **[Installation](docs/getting-started/installation.md)** - How to install Pali
- **[Quick Start](docs/getting-started/quick-start.md)** - Get running in 5 minutes
- **[GitHub](https://github.com/gitvipin/pali)** - Source code and issues

## Requirements

- Python 2.7+ or Python 3.4+
- No external dependencies

## Documentation

### Getting Started
- [Installation Guide](docs/getting-started/installation.md)
- [Quick Start (5 minutes)](docs/getting-started/quick-start.md)

### Core Concepts
- [ThreadPool Guide](docs/guide/thread-pool.md) - Parallel task execution
- [Tasks Guide](docs/guide/tasks.md) - Creating custom tasks
- [Pipelines Guide](docs/guide/pipeline.md) - Sequential workflows

### Advanced Features
- [Configuration Guide](docs/guide/configuration.md) - Config file management
- [Logging Guide](docs/guide/logging.md) - Logging setup and usage
- [A/B Testing Guide](docs/guide/ab-testing.md) - A/B testing with parameters

### Full Documentation
Visit the [Documentation Index](docs/README.md) for complete API reference.

## Additional Guides

- [Application Examples](docs/guide/examples.md) - Real-world usage patterns and code samples
- [Architecture](docs/guide/architecture.md) - System design and core concepts
- [Best Practices](docs/guide/best-practices.md) - Recommended patterns and optimization tips
- [Contributing Guide](docs/getting-started/contributing.md) - How to contribute to Pali

## Contributing
See the [Contributing Guide](docs/getting-started/contributing.md) for details.

## Support

- 📖 [Documentation](docs/README.md)
- 🐛 [Report Issues](https://github.com/gitvipin/pali/issues)
- 💬 [Discussions](https://github.com/gitvipin/pali/discussions)
- 📧 [Contact](mailto:sh.vipin@gmail.com)

## License

Pali is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for version history and release notes.

## Acknowledgments

Pali was built with simplicity and ease of use in mind. It draws inspiration from various threading and task queue libraries while maintaining a minimal footprint and zero external dependencies.

---

**Ready to get started?** Check out the [Quick Start Guide](docs/getting-started/quick-start.md)!
