# Quick Start

Get up and running with Pali in 5 minutes!

## Basic Example: Your First Thread Pool

Let's start with the simplest example - creating a task and processing it with a thread pool.

### Step 1: Import Required Modules

```python
from pali import task, worker
```

### Step 2: Define a Task

Create a custom task by extending `pali.task.Task`. The `_run()` method is where your work happens:

```python
class GreetingTask(task.Task):
    def __init__(self, name):
        super(GreetingTask, self).__init__()
        self.name = name
        self.greeting = None
    
    def _run(self):
        # This method is called by the thread pool
        self.greeting = f"Hello, {self.name}!"
        print(self.greeting)
```

### Step 3: Create Tasks and Process with Thread Pool

```python
# Create a list of tasks
names = ["Alice", "Bob", "Charlie"]
tasks = [GreetingTask(name) for name in names]

# Process them with a thread pool (3 concurrent threads)
with worker.ThreadPool(3) as tpool:
    for t in tasks:
        tpool.append_task(t)

# Results are available after the pool completes
for t in tasks:
    print(t.greeting)
```

### Output

```
Hello, Alice!
Hello, Bob!
Hello, Charlie!
```

## Complete Working Example

Save this as `hello_pali.py`:

```python
from pali import task, worker

class NumberTask(task.Task):
    def __init__(self, number):
        super(NumberTask, self).__init__()
        self.number = number
        self.square = None
    
    def _run(self):
        self.square = self.number ** 2

def main():
    # Create 10 tasks to square numbers 0-9
    tasks = [NumberTask(i) for i in range(10)]
    
    # Use 4 threads to process them
    with worker.ThreadPool(4) as tpool:
        for t in tasks:
            tpool.append_task(t)
    
    # Print results
    for t in tasks:
        print(f"{t.number}² = {t.square}")

if __name__ == "__main__":
    main()
```

Run it:

```bash
python hello_pali.py
```

Expected output:

```
0² = 0
1² = 1
2² = 4
3² = 9
4² = 16
5² = 25
6² = 36
7² = 49
8² = 64
9² = 81
```

## Key Concepts

- **Task**: A unit of work. Extend `pali.task.Task` and implement `_run()`
- **ThreadPool**: Manages a pool of worker threads. Use as a context manager with `with` statement
- **Worker Thread**: Executes tasks from the pool. Number of threads is specified when creating ThreadPool

## What's Next?

- [Thread Pool](../guide/thread-pool.md) - Learn more about configuring and using thread pools
- [Tasks](../guide/tasks.md) - Understand task lifecycle and advanced task features
- [Examples](../../examples/) - Browse more example scripts

## Common Questions

**Q: Do I need to manage threads manually?**
No! The ThreadPool handles all thread creation and management for you.

**Q: What if I don't use a context manager (`with` statement)?**
You can, but you'll need to manually stop the pool:

```python
tpool = worker.ThreadPool(3)
for t in tasks:
    tpool.append_task(t)
# ... do work ...
tpool.stop()  # Cleanup
```

Using `with` is recommended as it handles cleanup automatically.

**Q: Can I use Pali with Python 2?**
Yes! Pali is compatible with Python 2.7+ and Python 3.4+. Just use `print()` function syntax (with `from __future__ import print_function` in Python 2) or the older `print` statement.

## Troubleshooting

**ImportError: No module named pali**
Make sure you've installed Pali: `pip install pali`

**AttributeError: 'Task' object has no attribute '_run'**
Every task must implement the `_run()` method. This is where the work happens.

**My tasks aren't running in parallel**
- Make sure you're using multiple threads: `ThreadPool(num_threads)` where num_threads > 1
- Tasks run in parallel only when the thread pool is processing them
- Each thread picks up the next available task from the queue

For more help, check [Thread Pool Guide](../guide/thread-pool.md) or open an issue on [GitHub](https://github.com/gitvipin/pali/issues).
