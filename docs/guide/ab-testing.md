# A/B Testing Guide

Pali provides built-in A/B testing capabilities through the parameters system, allowing you to easily configure and distribute different parameter values across your application.

## Overview

A/B testing in Pali allows you to:

- Define parameters with multiple values
- Automatically distribute values across test runs
- Control distribution strategy (currently even distribution)
- Enable/disable A/B testing per parameter
- Integrate seamlessly with Pali's configuration system

## Basic A/B Testing

### Simple Example

```python
from pali import params

# Define a parameter with A/B values
params.add_param(
    name='algorithm',
    val='algorithm_v1',                    # Default value
    val_type=str,
    ab_values=['algorithm_v1', 'algorithm_v2'],  # A/B values
    ab_enabled=True                        # Enable A/B testing
)

# Each call to get_param returns the next value in sequence
print(params.get_param('algorithm'))  # 'algorithm_v1'
print(params.get_param('algorithm'))  # 'algorithm_v2'
print(params.get_param('algorithm'))  # 'algorithm_v1' (cycles back)
```

### Disabling A/B Testing

When `ab_enabled=False`, the default value is always returned:

```python
from pali import params

params.add_param(
    name='feature_flag',
    val='disabled',
    val_type=str,
    ab_values=['enabled', 'disabled'],
    ab_enabled=False  # A/B testing disabled
)

# Always returns 'disabled' (the default value)
print(params.get_param('feature_flag'))  # 'disabled'
print(params.get_param('feature_flag'))  # 'disabled'
```

## A/B Testing with Different Types

### Integer Parameters

```python
from pali import params

params.add_param(
    name='batch_size',
    val=32,
    val_type=int,
    ab_values=[16, 32, 64],
    ab_enabled=True
)

# Cycles through: 16, 32, 64, 16, 32, 64, ...
for i in range(6):
    print(f"Iteration {i}: batch_size={params.get_param('batch_size')}")

# Output:
# Iteration 0: batch_size=16
# Iteration 1: batch_size=32
# Iteration 2: batch_size=64
# Iteration 3: batch_size=16
# Iteration 4: batch_size=32
# Iteration 5: batch_size=64
```

### Float Parameters

```python
from pali import params

params.add_param(
    name='learning_rate',
    val=0.001,
    val_type=float,
    ab_values=[0.0001, 0.001, 0.01],
    ab_enabled=True
)

learning_rates = [params.get_param('learning_rate') for _ in range(3)]
print(learning_rates)  # [0.0001, 0.001, 0.01]
```

### Boolean Parameters

```python
from pali import params

params.add_param(
    name='use_cache',
    val=False,
    val_type=bool,
    ab_values=[True, False],
    ab_enabled=True
)

cache_settings = [params.get_param('use_cache') for _ in range(4)]
print(cache_settings)  # [True, False, True, False]
```

## Real-World Examples

### A/B Testing Algorithm Versions

```python
from pali import params
from pali.task import Task
from pali.worker import ThreadPool

params.add_param(
    name='sorting_algorithm',
    val='quicksort',
    val_type=str,
    ab_values=['quicksort', 'mergesort', 'heapsort'],
    ab_enabled=True
)

class SortTask(Task):
    def __init__(self, data, task_id):
        super(SortTask, self).__init__()
        self.data = data
        self.task_id = task_id
        self.algorithm = None
        self.sorted_data = None
        self.execution_time = 0
    
    def _run(self):
        import time
        
        self.algorithm = params.get_param('sorting_algorithm')
        
        start = time.time()
        if self.algorithm == 'quicksort':
            self.sorted_data = self._quicksort(self.data[:])
        elif self.algorithm == 'mergesort':
            self.sorted_data = self._mergesort(self.data[:])
        else:
            self.sorted_data = self._heapsort(self.data[:])
        self.execution_time = time.time() - start
        
        print(f"Task {self.task_id}: {self.algorithm} took {self.execution_time:.4f}s")
    
    def _quicksort(self, arr):
        if len(arr) <= 1:
            return arr
        pivot = arr[len(arr) // 2]
        left = [x for x in arr if x < pivot]
        middle = [x for x in arr if x == pivot]
        right = [x for x in arr if x > pivot]
        return self._quicksort(left) + middle + self._quicksort(right)
    
    def _mergesort(self, arr):
        if len(arr) <= 1:
            return arr
        mid = len(arr) // 2
        return self._merge(self._mergesort(arr[:mid]), self._mergesort(arr[mid:]))
    
    def _merge(self, left, right):
        result = []
        i = j = 0
        while i < len(left) and j < len(right):
            if left[i] <= right[j]:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
        return result + left[i:] + right[j:]
    
    def _heapsort(self, arr):
        import heapq
        return sorted(arr)

# Run A/B tests with 12 tasks (cycles through 3 algorithms, 4 times)
tasks = [SortTask(list(range(100, 0, -1)), i) for i in range(12)]

with ThreadPool(4) as tpool:
    for task in tasks:
        tpool.append_task(task)

# Analyze results
results_by_algo = {}
for task in tasks:
    if task.algorithm not in results_by_algo:
        results_by_algo[task.algorithm] = []
    results_by_algo[task.algorithm].append(task.execution_time)

print("\nA/B Test Results:")
for algo, times in sorted(results_by_algo.items()):
    avg_time = sum(times) / len(times)
    print(f"{algo}: avg={avg_time:.4f}s, count={len(times)}")
```

### A/B Testing Features

```python
from pali import params
from pali.logger import getLogger

log = getLogger(__name__)

# Define feature flags
params.add_param(
    name='new_ui',
    val='old_ui',
    val_type=str,
    ab_values=['old_ui', 'new_ui'],
    ab_enabled=True
)

params.add_param(
    name='enable_analytics',
    val=True,
    val_type=bool,
    ab_values=[True, False],
    ab_enabled=True
)

class RequestHandler:
    def __init__(self, request_id):
        self.request_id = request_id
    
    def handle(self):
        ui_version = params.get_param('new_ui')
        analytics_enabled = params.get_param('enable_analytics')
        
        log.info(f"Request {self.request_id}: UI={ui_version}, Analytics={analytics_enabled}")
        
        if ui_version == 'new_ui':
            return self._handle_new_ui()
        else:
            return self._handle_old_ui()
    
    def _handle_new_ui(self):
        return {'status': 'ok', 'ui_version': 'new'}
    
    def _handle_old_ui(self):
        return {'status': 'ok', 'ui_version': 'old'}

# Simulate requests
for i in range(10):
    handler = RequestHandler(i)
    result = handler.handle()
    print(f"  → {result}")
```

### A/B Testing Configuration Tuning

```python
from pali import params

# Test different timeout values
params.add_param(
    name='api_timeout',
    val=30,
    val_type=int,
    ab_values=[10, 30, 60],
    ab_enabled=True
)

# Test different cache sizes
params.add_param(
    name='cache_size',
    val=1000,
    val_type=int,
    ab_values=[100, 1000, 10000],
    ab_enabled=True
)

# Test different thread counts
params.add_param(
    name='num_threads',
    val=4,
    val_type=int,
    ab_values=[2, 4, 8],
    ab_enabled=True
)

class PerformanceTest:
    def __init__(self, test_id):
        self.test_id = test_id
        self.config = {
            'timeout': params.get_param('api_timeout'),
            'cache_size': params.get_param('cache_size'),
            'num_threads': params.get_param('num_threads'),
        }
    
    def run(self):
        print(f"Test {self.test_id}: {self.config}")
        # Run test with this configuration
        return {'test_id': self.test_id, 'config': self.config, 'result': 'pass'}

# Run performance tests
for i in range(9):
    test = PerformanceTest(i)
    result = test.run()
```

## Distribution Strategies

Currently, Pali supports even distribution (round-robin):

```python
from pali import params

# Even distribution cycles through values sequentially
params.add_param(
    name='server',
    val='server_a',
    val_type=str,
    ab_values=['server_a', 'server_b', 'server_c'],
    ab_enabled=True,
    ab_distribution='EVEN'  # Round-robin distribution
)

# Calls cycle: server_a, server_b, server_c, server_a, server_b, server_c, ...
```

## Integration with Configuration System

You can use A/B testing parameters with the configuration system:

```python
from pali import params
from pali.config import ConfigManager

# Define parameters (usually at startup)
params.add_param(
    name='db_host',
    val='localhost',
    val_type=str,
    ab_values=['localhost', 'db-backup'],
    ab_enabled=True
)

params.add_param(
    name='db_port',
    val=5432,
    val_type=int,
    ab_values=[5432, 5433],
    ab_enabled=True
)

# Create config manager with parameters
param_vals = {
    'db_host': params.get_param('db_host'),
    'db_port': params.get_param('db_port'),
}

cfg = ConfigManager(param_vals=param_vals)
```

## Best Practices

### 1. Define Parameters at Startup

```python
# main.py - Define all A/B parameters here
from pali import params

def init_ab_parameters():
    params.add_param('feature_x', 'old', str, 
                     ab_values=['old', 'new'], ab_enabled=True)
    params.add_param('feature_y', 'disabled', str,
                     ab_values=['disabled', 'enabled'], ab_enabled=False)
    params.add_param('batch_size', 32, int,
                     ab_values=[16, 32, 64], ab_enabled=True)

init_ab_parameters()
```

### 2. Log A/B Test Assignments

```python
from pali import params
from pali.logger import getLogger

log = getLogger(__name__)

def get_test_config():
    config = {
        'feature': params.get_param('feature_x'),
        'batch_size': params.get_param('batch_size'),
    }
    log.info(f"A/B test config: {config}")
    return config
```

### 3. Track A/B Test Results

```python
from pali import params

class ExperimentResult:
    def __init__(self):
        self.algorithm = params.get_param('algorithm')
        self.metric_a = 0
        self.metric_b = 0
    
    def analyze(self):
        return {
            'algorithm': self.algorithm,
            'metric_a': self.metric_a,
            'metric_b': self.metric_b,
        }
```

### 4. Keep A/B Variants Minimal

```python
from pali import params

# Good - 2-3 variants
params.add_param('color', 'blue', str,
                 ab_values=['blue', 'red'], ab_enabled=True)

# Avoid - too many variants
params.add_param('size', 's', str,
                 ab_values=['xs', 's', 'm', 'l', 'xl', 'xxl'],
                 ab_enabled=True)
```

## Troubleshooting

### Getting Same Value Repeatedly

Make sure A/B testing is enabled:

```python
from pali import params

# Problem: returns same value
params.add_param('test', 'a', str, ab_values=['a', 'b'])
# ab_enabled=False by default!

# Solution: enable A/B testing
params.add_param('test', 'a', str, ab_values=['a', 'b'], ab_enabled=True)
```

### Values Not Cycling

Ensure you're using `get_param()`:

```python
from pali import params

# Problem: not cycling
param_obj = params.PARAMS['test']

# Solution: use get_param()
value = params.get_param('test')
```

## Next Steps

- [Configuration Guide](configuration.md) - Use A/B parameters with config
- [Logging Guide](logging.md) - Log A/B test assignments
- [Thread Pool Guide](thread-pool.md) - Run A/B tests in parallel
