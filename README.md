[![Downloads](https://pepy.tech/badge/pali)](https://pepy.tech/project/pali)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-2.7%2B%2C%203.4%2B-blue.svg)](#requirements)

# Pali

**Pali** (Python Applications Lightweight Initiator) is a lightweight foundation library for Python Applications. Built entirely in native Python with zero dependencies.

Python applications repeatedly solve the same infrastructure problems—configuration, logging, concurrency, persistence, data pipelines, and service lifecycle management. Pali provides a lightweight, dependency-free collection of reusable building blocks for these common application patterns, allowing developers to focus on application logic instead of reinventing infrastructure. Adopt only the components you need, with no hidden framework overhead.

Start with [Quick Start](docs/getting-started/quick-start.md) to see how fast it is to build with Pali.

**Why Pali?**
- ✅ **Lightweight** — Minimal footprint, no external dependencies.
- ✅ **Native Python** — Pure Python implementation, works well in constrained and dependency-sensitive environments (e.g. ESX).
- ✅ **[12-factor](https://12factor.net/) friendly** — Designed for config, concurrency, logging, and disposability.
- ✅ **Production-tested** — Real-world utilities refined over years.
- ✅ **Modular** — Import only what you use.

### When should I consider Pali ?

**Pali** is a good fit when you are building:

- Infrastructure automation
- DevOps tooling
- Background workers
- Long-running daemons
- Backend services
- Microservices
- Batch processing applications
- Data pipelines
- Integration services
- CLI utilities

### Micro-Examples

**Structured logging** — Standardized application logging:
```python
from pali import setup_logging, getLogger

# Setup logging once when application starts. 
setup_logging(log_dir="./", log_file="my_app.log")

# Now every module can get logger and add logs.
log = getLogger(__name__)
log.info('Application started')
```

**Configuration management** — Load and validate settings:
```ini
# Define a .ini format based Config file for application.
# config/pali.cfg
[DEFAULT]
debug = true

[DATABASE]
host = localhost
port = 5432
```

```python
from pali import ConfigManager

# Initialize ConfigManager with app config file.
cfg = ConfigManager('config/pali.cfg')

# Read a value from the DATABASE section
db_host = cfg.get('DATABASE', 'host')

# Read a default value from the DEFAULT section
debug = cfg.get('DEFAULT', 'debug')
```

**Data pipelines** — Sequential processing stages:
```python
from pali import Pipeline, Stage

class HeatWaterStage(Stage):
    def __init__(self):
        super(HeatWaterStage, self).__init__('Heat Water')

    def run(self, data):
        data['temperature'] = 100
        data['state'] = 'water heated'

class AddTeaStage(Stage):
    def __init__(self):
        super(AddTeaStage, self).__init__('Add Tea')

    def run(self, data):
        data['tea'] = 'green'
        data['state'] = 'tea added'

class SteepTeaStage(Stage):
    def __init__(self):
        super(SteepTeaStage, self).__init__('Steep Tea')

    def run(self, data):
        data['steeped'] = True
        data['state'] = 'tea steeped'

class ServeTeaStage(Stage):
    def __init__(self):
        super(ServeTeaStage, self).__init__('Serve Tea')

    def run(self, data):
        data['served'] = True
        data['result'] = 'cup of tea ready'

pipeline = Pipeline(
    name='TeaPipeline',
    stages=[HeatWaterStage(), AddTeaStage(), SteepTeaStage(), ServeTeaStage()],
    data={'cup': 'empty'}
)
pipeline._run()
print(pipeline.data)
```

**Parallel task execution** — Process items concurrently:
```python
from pali import Task, ThreadPool

class ProcessItem(Task):
    def _run(self):
        self.result = expensive_operation(self.data)

items = [1, 2, 3]
tasks = [ProcessItem(item) for item in items]
with ThreadPool(4) as pool:
    for t in tasks:
        pool.append_task(t)
results = [t.result for t in tasks]
```


## Quick Links

- **[Getting Started](docs/getting-started/)** - Installation and quick start
- **[Full Documentation](docs/README.md)** - All guides and API docs
- **[GitHub](https://github.com/gitvipin/pali)** - Source code and issues

## Requirements

- Python 2.7+ or Python 3.4+
- No external dependencies

## Contributing
See the [Contributing Guide](docs/getting-started/contributing.md) for details.

## Support

- 📖 [Documentation](docs/README.md)
- 🐛 [Report Issues](https://github.com/gitvipin/pali/issues)
- 💬 [Discussions](https://github.com/gitvipin/pali/discussions)

## License

Pali is licensed under the MIT License. See [LICENSE](LICENSE) for details.

## Changelog

See [CHANGELOG.md](docs/CHANGELOG.md) for version history and release notes.

## Acknowledgments

Pali was built with simplicity and ease of use in mind. It draws inspiration from various threading and task queue libraries while maintaining a minimal footprint and zero external dependencies.

---

**Ready to get started?** Check out the [Quick Start Guide](docs/getting-started/quick-start.md)!
