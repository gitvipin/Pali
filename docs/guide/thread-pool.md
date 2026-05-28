# Thread Pool Guide

ThreadPool is the core component of Pali. It manages a pool of worker threads that execute tasks concurrently.

## Overview

A ThreadPool maintains a queue of tasks and assigns them to available worker threads. This allows you to process multiple tasks in parallel without manually managing individual threads.

### Key Components

- **ThreadPool**: Manages the pool of worker threads
- **WorkerThread**: Individual thread that executes tasks
- **Task Queue**: Queue that holds pending tasks
- **Finished Queue**: Queue that holds completed tasks

## Creating a Thread Pool

### Basic Usage

```python
from pali import worker

# Create a thread pool with 4 worker threads
tpool = worker.ThreadPool(4)

# Add tasks
tpool.append_task(task1)
tpool.append_task(task2)

# Don't forget to stop the pool!
tpool.close()
```

### Using Context Manager (Recommended)

The context manager automatically starts and stops the thread pool:

```python
from pali import worker

tasks = [MyTask(i) for i in range(10)]

with worker.ThreadPool(4) as tpool:
    for task in tasks:
        tpool.append_task(task)
# Pool is automatically closed here
```

## ThreadPool Parameters

### `max_threads` (required)

The number of worker threads to create.

```python
# Single-threaded processing
with worker.ThreadPool(1) as tpool:
    pass

# Multi-threaded processing
with worker.ThreadPool(10) as tpool:
    pass
```

**Note**: More threads don't always mean faster processing. Consider:
- Number of CPU cores on your system
- Whether tasks are CPU-bound or I/O-bound
- System memory available

**Guidelines:**
- **I/O-bound tasks** (network, database): Can use many threads (10-100+)
- **CPU-bound tasks**: Use number of CPU cores

### `max_queue_size` (optional)

Maximum number of tasks that can be queued at once (default: 3000).

```python
with worker.ThreadPool(4, max_queue_size=5000) as tpool:
    pass
```

### `verbose` (optional)

Enable debug logging for detailed thread activity (default: False).

```python
with worker.ThreadPool(4, verbose=True) as tpool:
    pass
```

This will log thread operations like popping/pushing tasks.

## ThreadPool Interface

### `append_task(task)`

Add a task to the thread pool for processing.

```python
tpool.append_task(my_task)
```

Tasks are processed in FIFO order (first in, first out).

### `close()`

Wait for all pending tasks to complete and stop all worker threads.

```python
tpool.close()
```

**Important**: This blocks until all tasks are finished. Don't call it while tasks are still being added.

### `remaining()`

Get the approximate number of pending (unfinished) tasks.

```python
pending = tpool.remaining()
print(f"Tasks waiting: {pending}")
```

### `finished()`

Get the number of completed tasks.

```python
done = tpool.finished()
```

### `get_workers()`

Get a list of all worker threads.

```python
workers = tpool.get_workers()
print(f"Number of workers: {len(workers)}")
```

## Task Lifecycle

When you append a task to the thread pool, it goes through this lifecycle:

1. **NEW** - Task created
2. **READY** - Task added to queue
3. **RUNNING** - Worker thread executing `_run()` method
4. **FINISHED** - Task execution completed (success or failure)

Access task state:

```python
class MyTask(task.Task):
    pass

t = MyTask()
print(t.state)  # Task.NEW

tpool.append_task(t)
# ... in worker thread ...
# t.state becomes Task.READY
# t.state becomes Task.RUNNING
# t.state becomes Task.FINISHED
```

## Common Patterns

### Processing a Large Batch

```python
from pali import worker, task

class ProcessFileTask(task.Task):
    def __init__(self, filename):
        super(ProcessFileTask, self).__init__()
        self.filename = filename
        self.result = None
    
    def _run(self):
        with open(self.filename, 'r') as f:
            self.result = f.read().upper()

# Process 100 files with 8 threads
files = [f"file_{i}.txt" for i in range(100)]
tasks = [ProcessFileTask(f) for f in files]

with worker.ThreadPool(8) as tpool:
    for t in tasks:
        tpool.append_task(t)

# Collect results
results = [t.result for t in tasks]
```

### Producer-Consumer Pattern

```python
import time
from pali import worker, task

class ConsumerTask(task.Task):
    def __init__(self, job_id):
        super(ConsumerTask, self).__init__()
        self.job_id = job_id
        self.status = "pending"
    
    def _run(self):
        time.sleep(1)  # Simulate work
        self.status = "complete"

with worker.ThreadPool(4) as tpool:
    # Add tasks as they become available
    for i in range(20):
        tpool.append_task(ConsumerTask(i))
        if i % 5 == 0:
            print(f"Pending tasks: {tpool.remaining()}")
        time.sleep(0.1)  # Simulate work being produced

print(f"All done! Final pending: {tpool.remaining()}")
```

### Waiting for Specific Tasks

```python
with worker.ThreadPool(4) as tpool:
    tasks = [MyTask(i) for i in range(10)]
    
    for t in tasks:
        tpool.append_task(t)
    
    # Wait for all to complete
    while tpool.remaining() > 0:
        print(f"Waiting... {tpool.remaining()} tasks left")
        time.sleep(1)
```

## Error Handling

Exceptions in tasks are caught by the worker thread and logged. The pool continues processing other tasks.

```python
class FailingTask(task.Task):
    def _run(self):
        raise ValueError("Oops!")

tasks = [FailingTask(), MyTask()]

with worker.ThreadPool(2) as tpool:
    for t in tasks:
        tpool.append_task(t)
    # Pool catches the ValueError and logs it
    # Other tasks continue processing
```

To handle task-specific errors, use try-except in your `_run()` method:

```python
class SafeTask(task.Task):
    def __init__(self, data):
        super(SafeTask, self).__init__()
        self.data = data
        self.error = None
    
    def _run(self):
        try:
            # Do risky work
            result = 1 / self.data
        except Exception as e:
            self.error = e
```

## Performance Tuning

### Thread Count

```python
import multiprocessing

# Use all CPU cores
num_cores = multiprocessing.cpu_count()
with worker.ThreadPool(num_cores) as tpool:
    pass
```

### Queue Size

For very large batches, increase queue size:

```python
with worker.ThreadPool(8, max_queue_size=10000) as tpool:
    # Can queue 10,000 tasks
    pass
```

### Monitoring

```python
import time

with worker.ThreadPool(4) as tpool:
    # Add tasks...
    for t in tasks:
        tpool.append_task(t)
    
    # Monitor progress
    start = time.time()
    while tpool.remaining() > 0:
        elapsed = time.time() - start
        rate = (len(tasks) - tpool.remaining()) / elapsed
        print(f"Rate: {rate:.1f} tasks/sec, Remaining: {tpool.remaining()}")
        time.sleep(1)
```

## Advanced Topics

### Manual Thread Control

```python
tpool = worker.ThreadPool(4)
tpool.start()

# Add tasks...

# Get worker threads
workers = tpool.get_workers()
for w in workers:
    print(f"Worker: {w.name}, Disabled: {w.is_disabled()}")

tpool.close()
```

### Custom Worker Threads

You can access individual worker threads for advanced use cases, but this is rarely needed. Most users should use the standard ThreadPool interface.

## Next Steps

- [Tasks Guide](tasks.md) - Learn how to create custom tasks
- [Pipelines Guide](pipeline.md) - Use pipelines for complex workflows
- [Examples](../../examples/) - See real-world examples
