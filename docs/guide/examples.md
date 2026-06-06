# Application Examples

Pali can be applied to various real-world scenarios. Below are practical examples demonstrating how to use Pali for different types of applications.

## Example 1: Process Numbers in Parallel

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

## Example 2: Fetch Multiple URLs Concurrently

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

## Example 3: ETL Pipeline

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

## Example 4: Stress Testing

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

---

See the [examples/](../../examples/) directory for more complete, runnable examples.
