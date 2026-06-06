# Best Practices for Pali

This guide covers recommended patterns and practices for building robust applications with Pali.

## Task Design

### Do's ✓

- **Create self-contained tasks** with all needed data in `__init__`
  ```python
  class MyTask(task.Task):
      def __init__(self, user_id, email):
          super(MyTask, self).__init__()
          self.user_id = user_id
          self.email = email
  ```

- **Store results as task attributes** rather than returning from `_run()`
  ```python
  def _run(self):
      self.result = expensive_operation()
      self.success = True
  ```

- **Use context manager** (`with` statement) for ThreadPool
  ```python
  with worker.ThreadPool(8) as tpool:
      # tasks are automatically cleaned up
  ```

- **Handle exceptions in `_run()` method**
  ```python
  def _run(self):
      try:
          self.result = risky_operation()
      except Exception as e:
          self.error = str(e)
  ```

- **Log important operations** for debugging and monitoring
  ```python
  from pali import logger
  logger.info(f"Processing user {self.user_id}")
  ```

- **Use type hints** for better IDE support and code clarity
  ```python
  def __init__(self, data: Dict[str, Any]) -> None:
      super(MyTask, self).__init__()
      self.data = data
  ```

### Don'ts ✗

- **Don't pass arguments to `_run()` method**
  ```python
  # Wrong
  task._run(some_argument)
  
  # Right - pass everything in __init__
  task._run()  # uses self.data from __init__
  ```

- **Don't share mutable state between tasks without synchronization**
  ```python
  # Wrong - race conditions
  shared_list = []
  tasks = [MyTask(shared_list) for _ in range(10)]
  
  # Right - use immutable or thread-safe patterns
  tasks = [MyTask(list_copy) for _ in range(10)]
  ```

- **Don't return values from `_run()`**
  ```python
  # Wrong
  def _run(self):
      return compute_result()
  
  # Right
  def _run(self):
      self.result = compute_result()
  ```

- **Don't create threads manually**
  ```python
  # Wrong
  import threading
  t = threading.Thread(target=self.work)
  
  # Right - use ThreadPool
  tpool.append_task(MyTask())
  ```

- **Don't forget to call `close()` if not using context manager**
  ```python
  # If not using 'with' statement, must cleanup
  tpool = worker.ThreadPool(8)
  # ... add tasks ...
  tpool.close()
  ```

## ThreadPool Configuration

### Thread Count Selection

- **I/O-bound tasks** (network, file, database): Use 10-100+ threads depending on I/O latency
- **CPU-bound tasks** (computation): Use number of available CPU cores
- **Mixed workload**: Start with CPU cores and adjust based on profiling

```python
import multiprocessing
cpu_count = multiprocessing.cpu_count()
tpool = worker.ThreadPool(cpu_count)  # CPU-bound
```

### Queue Size Management

- **Default**: 3000 tasks
- **For large batch processing**: Increase queue size
  ```python
  tpool = worker.ThreadPool(8, max_queue_size=10000)
  ```
- **Monitor queue depth** to detect bottlenecks

## Logging Configuration

### Production Deployments

```python
from pali import logger
logger.set_level('WARNING')  # or ERROR
```

Use `WARNING` or `ERROR` levels to reduce I/O overhead and storage.

### Development and Debugging

```python
logger.set_level('DEBUG')  # or INFO
```

Use `INFO` for normal development, `DEBUG` for detailed tracing.

## Error Handling

Always check task status after execution:

```python
with worker.ThreadPool(8) as tpool:
    for task in tasks:
        tpool.append_task(task)

# Check results
for task in tasks:
    if hasattr(task, 'error') and task.error:
        logger.error(f"Task {task.id} failed: {task.error}")
    else:
        logger.info(f"Task {task.id} succeeded")
```

## Performance Optimization

### Profiling

Profile your application to identify bottlenecks:

```python
import cProfile
import pstats

profiler = cProfile.Profile()
profiler.enable()

# ... run your task processing ...

profiler.disable()
stats = pstats.Stats(profiler)
stats.sort_stats('cumulative')
stats.print_stats(10)  # top 10 functions
```

### Batch Processing

For very large workloads, process in batches:

```python
all_items = range(100000)
batch_size = 1000

for i in range(0, len(all_items), batch_size):
    batch = all_items[i:i+batch_size]
    tasks = [MyTask(item) for item in batch]
    
    with worker.ThreadPool(8) as tpool:
        for task in tasks:
            tpool.append_task(task)
```

## Pipeline Design

### Stage Independence

Keep pipeline stages independent and focused:

```python
class ExtractStage(Stage):
    def run(self, data):
        data['raw'] = self.extract()

class TransformStage(Stage):
    def run(self, data):
        data['transformed'] = self.transform(data['raw'])
```

### Error Propagation

Handle and log errors appropriately:

```python
class MyStage(Stage):
    def run(self, data):
        try:
            data['result'] = self.process(data)
        except Exception as e:
            data['error'] = str(e)
            logger.error(f"Stage failed: {e}")
```

---

For more guidance, see [Architecture](architecture.md) and [Application Examples](examples.md).
