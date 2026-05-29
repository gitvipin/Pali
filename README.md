[![Downloads](https://pepy.tech/badge/pali)](https://pepy.tech/project/pali)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-2.7%2B%2C%203.4%2B-blue.svg)](#requirements)

# Pali - Python Applications Lightweight Initiator

Pali is a lightweight initiator for Python applications. It provides essential utilities for task execution, workflow orchestration, configuration, logging, and runtime support.

Pali is compatible with Python 2.7+ and Python 3.4+, and is designed to help you bootstrap small to medium Python applications with minimal dependencies.

## Quick Links

- **[Documentation](docs/README.md)** - Full guides and API reference
- **[Installation](docs/getting-started/installation.md)** - How to install Pali
- **[Quick Start](docs/getting-started/quick-start.md)** - Get running in 5 minutes
- **[GitHub](https://github.com/gitvipin/pali)** - Source code and issues

## What is Pali?

Pali provides a compact suite of application utilities for Python, including task execution, workflow pipelines, configuration management, logging, and parameter-driven runtime behavior.

It is built to help developers compose reusable application building blocks without imposing a heavy framework.

### 1. **Task Execution** - Parallel and Asynchronous Workloads

One of Pali's core execution models is ThreadPool, which lets you process multiple independent tasks in parallel using a pool of worker threads:

```python
from pali import worker, task

class MyTask(task.Task):
    def __init__(self, number):
        super(MyTask, self).__init__()
        self.number = number
        self.result = None
    
    def _run(self):
        self.result = self.number ** 2

# Create 10 tasks
tasks = [MyTask(i) for i in range(10)]

# Process with 4 threads
with worker.ThreadPool(4) as tpool:
    for t in tasks:
        tpool.append_task(t)

# Get results
print([t.result for t in tasks])  # [0, 1, 4, 9, 16, ...]
```

### 2. **Pipelines** - Workflow Coordination and Sequential Processing

Pipelines let you build ordered workflows with stages that execute sequentially, so you can model real application processes and multi-step business logic:

```python
from pali.pipeline import Pipeline, Stage

class ValidationStage(Stage):
    def run(self, data):
        if not data:
            raise ValueError("Invalid data")

class ProcessingStage(Stage):
    def run(self, data):
        data['result'] = sum(data['values'])

class OutputStage(Stage):
    def run(self, data):
        print(f"Result: {data['result']}")

pipeline = Pipeline(
    "MyPipeline",
    stages=[ValidationStage(), ProcessingStage(), OutputStage()],
    data={'values': [1, 2, 3, 4, 5]}
)

pipeline._run()  # Output: Result: 15
```

## Application Utility Use Cases

Pali excels at providing lightweight utility support for application-style workflows and infrastructure:

| Use Case | Solution | Details |
|----------|----------|---------|
| **Application Bootstrapping** | Task Execution + Configuration | Core utilities for starting app workflows, managing config, and running tasks |
| **Data Workflows** | Pipeline + Assembly | Multi-stage ETL workflows, processing pipelines, and workflow coordination |
| **Concurrent Request Handling** | ThreadPool | Handle parallel request or job processing in broker-style applications |
| **Stress and Load Simulation** | ThreadPool | Simulate load, stress testing, and background work |
| **Configuration Management** | ConfigManager | INI-based config loading, default values, and environment variants |
| **Logging and Diagnostics** | Logger | Thread-aware logging, file logging, and module-level control |
| **Feature Experimentation** | Parameters | Parameter-driven A/B testing and runtime variant switching |

## Core Features

### 🚀 **ThreadPool** - Simple Parallel Processing for Application Workloads
- Easy-to-use context manager API
- Configurable thread count
- Thread-safe task queueing
- Automatic task distribution
- Graceful shutdown handling

### 📊 **Pipelines** - Sequential Workflows
- Ordered stage execution
- Shared data dictionary between stages
- Assembly pattern for parallel pipelines
- Error handling and logging
- Reusable pipeline definitions

### ⚙️ **Configuration Management**
- INI-based configuration files
- Type-safe parameter handling
- Section-based organization
- Environment-specific configs

### 📝 **Logging**
- Integrated logging setup
- Thread-aware log formatting
- Per-module log level control
- File-based logging with auto-directory creation

### 🔬 **A/B Testing**
- Parameter-based A/B testing
- Multiple value distributions
- Enable/disable per parameter
- Automatic cycling through variants

## Installation

### From PyPI (Recommended)

```bash
pip install pali
```

### From Source

```bash
git clone https://github.com/gitvipin/pali.git
cd pali
python setup.py install
```

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
Visit the [Documentation Index](docs/README.md) for complete API reference and examples.

## Application Examples

### Example 1: Process Numbers in Parallel

```python
from pali import worker, task

class SquareTask(task.Task):
    def __init__(self, number):
        super(SquareTask, self).__init__()
        self.number = number
        self.result = None
    
    def _run(self):
        self.result = self.number ** 2

numbers = list(range(100))
tasks = [SquareTask(n) for n in numbers]

with worker.ThreadPool(8) as tpool:
    for t in tasks:
        tpool.append_task(t)

results = [t.result for t in tasks]
```

### Example 2: Fetch Multiple URLs Concurrently

```python
from pali import worker, task
import requests

class FetchTask(task.Task):
    def __init__(self, url):
        super(FetchTask, self).__init__()
        self.url = url
        self.response = None
        self.error = None
    
    def _run(self):
        try:
            self.response = requests.get(self.url, timeout=5)
        except Exception as e:
            self.error = e

urls = ['https://api.example.com/data1', 'https://api.example.com/data2']
tasks = [FetchTask(url) for url in urls]

with worker.ThreadPool(10) as tpool:
    for t in tasks:
        tpool.append_task(t)

for t in tasks:
    if t.error:
        print(f"Failed: {t.url}")
    else:
        print(f"Success: {t.url} - {len(t.response.content)} bytes")
```

### Example 3: ETL Pipeline

```python
from pali.pipeline import Pipeline, Stage
import csv
import json

class ExtractStage(Stage):
    def run(self, data):
        rows = []
        with open(data['input_file']) as f:
            for row in csv.DictReader(f):
                rows.append(row)
        data['raw'] = rows

class TransformStage(Stage):
    def run(self, data):
        transformed = [{'name': row['Name'].upper()} for row in data['raw']]
        data['transformed'] = transformed

class LoadStage(Stage):
    def run(self, data):
        with open(data['output_file'], 'w') as f:
            json.dump(data['transformed'], f)

pipeline = Pipeline(
    "ETL",
    stages=[ExtractStage(), TransformStage(), LoadStage()],
    data={'input_file': 'input.csv', 'output_file': 'output.json'}
)
pipeline._run()
```

### Example 4: Stress Testing

```python
from pali import worker, task
import time
import random

class StressTask(task.Task):
    def __init__(self, task_id):
        super(StressTask, self).__init__()
        self.task_id = task_id
        self.duration = None
    
    def _run(self):
        # Simulate variable load
        self.duration = random.uniform(0.1, 2.0)
        time.sleep(self.duration)

# Create 1000 stress tasks
tasks = [StressTask(i) for i in range(1000)]

# Process with 50 concurrent threads
with worker.ThreadPool(50) as tpool:
    for t in tasks:
        tpool.append_task(t)

print(f"Total tasks: {len(tasks)}")
print(f"Avg duration: {sum(t.duration for t in tasks) / len(tasks):.2f}s")
```

More examples can be found in the [examples/](examples/) directory.

## Architecture

### ThreadPool Model

```
ThreadPool (manages N worker threads)
├── Worker Thread 1 (processes tasks)
├── Worker Thread 2 (processes tasks)
├── Worker Thread 3 (processes tasks)
└── ...

Task Queue → Worker Threads → Task Execution
```

### Pipeline Model

```
Pipeline
├── Stage 1 (validation)
├── Stage 2 (processing)
└── Stage 3 (output)
     ↓
   Shared Data Dictionary
```

### Assembly Model

```
Assembly (manages multiple pipelines in parallel)
├── Pipeline 1 (server A)
├── Pipeline 2 (server B)
└── Pipeline 3 (server C)
```

## Performance Tuning

### Thread Count
- **I/O-bound tasks**: Use 10-100+ threads
- **CPU-bound tasks**: Use number of CPU cores
- **Mixed workload**: Start with CPU cores and adjust

### Queue Size
- Default: 3000 tasks
- Increase for large batches: `ThreadPool(8, max_queue_size=10000)`

### Logging Level
- **Production**: `logging.WARNING` or `logging.ERROR`
- **Development**: `logging.INFO` or `logging.DEBUG`

## Best Practices

✅ **Do's**
- Create self-contained tasks with all needed data in `__init__`
- Store results as task attributes
- Use context manager (`with` statement) for ThreadPool
- Handle exceptions in `_run()` method
- Log important operations
- Use type hints for better IDE support

❌ **Don'ts**
- Don't pass arguments to `_run()` method
- Don't share mutable state between tasks without synchronization
- Don't return values from `_run()` (use attributes instead)
- Don't create threads manually (use ThreadPool instead)
- Don't forget to call `close()` if not using context manager



## Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

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
