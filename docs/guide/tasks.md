# Tasks Guide

Tasks are units of work in Pali. Every task must implement a well-defined interface and extend `pali.task.Task`.

## Task Basics

A task represents a single unit of work that can be executed by a worker thread. Tasks are self-contained and execute independently.

### Task Lifecycle

Every task goes through these states:

```
NEW → READY → RUNNING → FINISHED
```

- **NEW**: Task object created, not yet queued
- **READY**: Task added to the thread pool queue
- **RUNNING**: Worker thread is executing `_run()`
- **FINISHED**: Execution completed (success or failure)

Access the state:

```python
from pali.task import Task

class MyTask(Task):
    def _run(self):
        pass

t = MyTask()
print(t.state)  # Task.NEW

# After appending to thread pool and executing:
print(t.state)  # Task.FINISHED
```

## Creating a Custom Task

Every custom task must extend `pali.task.Task` and implement the `_run()` method.

### Basic Template

```python
from pali.task import Task

class MyTask(Task):
    def __init__(self, data):
        super(MyTask, self).__init__()
        self.data = data
        self.result = None
    
    def _run(self):
        # Your work goes here
        self.result = process(self.data)
```

### Important Rules

1. **Extend Task**: Must inherit from `pali.task.Task`
2. **Call super().__init__()**: Initialize the base Task class
3. **Implement _run()**: Core logic goes here
4. **No arguments to _run()**: All data should be passed in `__init__`
5. **Store results as attributes**: Results are accessed after execution

## Task Examples

### Simple Data Processing

```python
from pali.task import Task

class SquareTask(Task):
    def __init__(self, number):
        super(SquareTask, self).__init__()
        self.number = number
        self.result = None
    
    def _run(self):
        self.result = self.number ** 2

# Usage
task = SquareTask(5)
print(task.result)  # None - not executed yet

with worker.ThreadPool(1) as tpool:
    tpool.append_task(task)

print(task.result)  # 25 - now it's executed
```

### HTTP Request Task

```python
import requests
from pali.task import Task

class FetchTask(Task):
    def __init__(self, url):
        super(FetchTask, self).__init__()
        self.url = url
        self.response = None
        self.error = None
    
    def _run(self):
        try:
            self.response = requests.get(self.url, timeout=5)
        except requests.RequestException as e:
            self.error = e

# Usage
urls = [
    "https://api.example.com/data1",
    "https://api.example.com/data2",
    "https://api.example.com/data3",
]

tasks = [FetchTask(url) for url in urls]

with worker.ThreadPool(5) as tpool:
    for t in tasks:
        tpool.append_task(t)

# Process results
for t in tasks:
    if t.error:
        print(f"Failed: {t.url} - {t.error}")
    else:
        print(f"Success: {t.url} - Status {t.response.status_code}")
```

### Database Operation Task

```python
import sqlite3
from pali.task import Task

class DatabaseTask(Task):
    def __init__(self, db_file, query, params=None):
        super(DatabaseTask, self).__init__()
        self.db_file = db_file
        self.query = query
        self.params = params or ()
        self.result = None
        self.error = None
    
    def _run(self):
        try:
            conn = sqlite3.connect(self.db_file)
            cursor = conn.cursor()
            cursor.execute(self.query, self.params)
            self.result = cursor.fetchall()
            conn.close()
        except sqlite3.Error as e:
            self.error = e

# Usage
tasks = [
    DatabaseTask("data.db", "SELECT * FROM users WHERE id=?", (1,)),
    DatabaseTask("data.db", "SELECT * FROM users WHERE id=?", (2,)),
    DatabaseTask("data.db", "SELECT * FROM users WHERE id=?", (3,)),
]

with worker.ThreadPool(3) as tpool:
    for t in tasks:
        tpool.append_task(t)

for t in tasks:
    if t.error:
        print(f"Error: {t.error}")
    else:
        print(f"Results: {t.result}")
```

### File Processing Task

```python
import hashlib
from pali.task import Task

class FileHashTask(Task):
    def __init__(self, filepath):
        super(FileHashTask, self).__init__()
        self.filepath = filepath
        self.hash = None
        self.error = None
    
    def _run(self):
        try:
            sha256 = hashlib.sha256()
            with open(self.filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b''):
                    sha256.update(chunk)
            self.hash = sha256.hexdigest()
        except IOError as e:
            self.error = e

# Usage - hash multiple files in parallel
files = ["file1.bin", "file2.bin", "file3.bin"]
tasks = [FileHashTask(f) for f in files]

with worker.ThreadPool(4) as tpool:
    for t in tasks:
        tpool.append_task(t)

for t in tasks:
    if t.error:
        print(f"Error reading {t.filepath}: {t.error}")
    else:
        print(f"{t.filepath}: {t.hash}")
```

## Task Priority

Tasks support priority-based ordering. Lower priority values run first.

```python
from pali.task import Task

class PriorityTask(Task):
    def __init__(self, name, priority):
        super(PriorityTask, self).__init__(priority=priority)
        self.name = name
    
    def _run(self):
        print(f"Running {self.name}")

# Default priority is 1
t1 = PriorityTask("Task A", priority=1)

# Higher priority number = runs later
t2 = PriorityTask("Task B", priority=10)
t3 = PriorityTask("Task C", priority=5)
```

**Note**: Pali's thread pool processes tasks in FIFO order, not by priority. Priority is available for custom ordering implementations.

## Error Handling in Tasks

### Try-Except Pattern

```python
from pali.task import Task

class SafeTask(Task):
    def __init__(self, data):
        super(SafeTask, self).__init__()
        self.data = data
        self.result = None
        self.error = None
    
    def _run(self):
        try:
            # Risky operation
            self.result = 1 / self.data
        except ZeroDivisionError as e:
            self.error = e
        except Exception as e:
            self.error = e

# Usage
t = SafeTask(0)
with worker.ThreadPool(1) as tpool:
    tpool.append_task(t)

if t.error:
    print(f"Task failed: {t.error}")
else:
    print(f"Result: {t.result}")
```

### Logging Errors

```python
from pali.task import Task
from pali.logger import getLogger

log = getLogger(__name__)

class LoggingTask(Task):
    def __init__(self, data):
        super(LoggingTask, self).__init__()
        self.data = data
    
    def _run(self):
        try:
            # Do work
            pass
        except Exception as e:
            log.error(f"Task failed with data {self.data}: {e}")
            raise  # Re-raise or handle as needed
```

## Best Practices

### 1. Keep Tasks Self-Contained

```python
# Good - task contains all needed data
class CalculationTask(Task):
    def __init__(self, numbers):
        super(CalculationTask, self).__init__()
        self.numbers = numbers
        self.result = None
    
    def _run(self):
        self.result = sum(self.numbers)

# Avoid - accessing external state
shared_list = []

class BadTask(Task):
    def _run(self):
        shared_list.append(1)  # Don't rely on external state
```

### 2. Store Results as Attributes

```python
# Good - results accessible after execution
class MyTask(Task):
    def __init__(self, value):
        super(MyTask, self).__init__()
        self.input = value
        self.output = None
    
    def _run(self):
        self.output = self.input * 2

# Avoid - returning values from _run()
class BadTask(Task):
    def _run(self):
        return 42  # This return value is lost
```

### 3. Handle Cleanup

```python
from pali.task import Task

class DatabaseTask(Task):
    def __init__(self, db_file):
        super(DatabaseTask, self).__init__()
        self.db_file = db_file
        self.connection = None
        self.result = None
    
    def _run(self):
        try:
            import sqlite3
            self.connection = sqlite3.connect(self.db_file)
            # Do work
            self.result = "success"
        finally:
            if self.connection:
                self.connection.close()
```

### 4. Use Meaningful Names

```python
# Good - clear what the task does
class ParseJSONTask(Task):
    pass

class CompressFileTask(Task):
    pass

# Avoid - unclear names
class Task1(Task):
    pass

class DoStuff(Task):
    pass
```

## Task Comparison

Tasks implement comparison operators for priority ordering:

```python
t1 = Task(priority=1)
t2 = Task(priority=2)

print(t1 < t2)  # True - t1 has higher priority
```

This is useful for custom queue implementations that need priority ordering.

## Next Steps

- [Thread Pool Guide](thread-pool.md) - Learn about running tasks
- [Pipelines Guide](pipeline.md) - Combine tasks into workflows
- [Examples](../../examples/) - See more task examples
