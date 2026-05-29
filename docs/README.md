# Pali Documentation

Welcome to the Pali documentation. This guide will help you get started with Pali and explore all its features.

## Table of Contents

### Getting Started
- [Installation](getting-started/installation.md) - How to install Pali
- [Quick Start](getting-started/quick-start.md) - Get up and running in 5 minutes

### Core Concepts & Guides
- [Thread Pool](guide/thread-pool.md) - Understanding and using ThreadPool
- [Tasks](guide/tasks.md) - Creating and managing custom tasks
- [Pipelines](guide/pipeline.md) - Building data pipelines with stages

### Advanced Features
- [Configuration](guide/configuration.md) - Configuring Pali with config files
- [Logging](guide/logging.md) - Setting up and using Pali's logging system
- [A/B Testing](guide/ab-testing.md) - Built-in A/B testing capabilities

### API Reference
- [API Reference](api/reference.md) - Complete API documentation

---

## What is Pali?

Pali is a lightweight initiator for Python applications that supports both Python 2.7+ and Python 3.4+.

Pali excels at:
- Creating flexible data pipelines
- Handling concurrent requests in messaging brokers
- Simulating stress testing scenarios
- Building API testing frameworks

## Quick Example

```python
from pali import worker, task

class MyTask(task.Task):
    def __init__(self, ident):
        self.task_id = ident
        self.result = None
    
    def _run(self):
        # Your processing logic here
        self.result = self.task_id * 2

# Create tasks
tasks = [MyTask(i) for i in range(10)]

# Process with thread pool
with worker.ThreadPool(3) as tpool:
    for t in tasks:
        tpool.append_task(t)

# Check results
results = [t.result for t in tasks]
print(results)  # [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

For more examples, see the [examples/](../examples/) directory.

## Next Steps

- New to Pali? Start with [Installation](getting-started/installation.md) and [Quick Start](getting-started/quick-start.md)
- Want to understand how it works? Read [Thread Pool](guide/thread-pool.md)
- Building a pipeline? Check out [Pipelines](guide/pipeline.md)
- Need to configure Pali? See [Configuration](guide/configuration.md)

## Contributing

Found a bug or want to add a feature? Check out the main [README](../README.md) for contribution guidelines.

## License

Pali is licensed under the MIT License. See [LICENSE](../LICENSE) for details.
