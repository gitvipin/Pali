# Pipelines Guide

Pipelines are a powerful way to organize complex, sequential workflows. A pipeline is a series of stages that execute in order on shared data.

## Pipeline Concepts

### Terminology

- **Stage**: A single step in a pipeline. Executes a specific task on the data.
- **Pipeline**: An ordered collection of stages. Stages execute sequentially.
- **Assembly**: A collection of pipelines that can run in parallel.

### When to Use Pipelines

Use pipelines when you have:

- **Sequential steps**: Processing must happen in a specific order
- **Shared state**: Stages need to share and modify common data
- **Complex workflows**: Multi-step processes with interdependencies

**Example Use Cases:**
- Data ETL pipelines (Extract → Transform → Load)
- Configuration management (Validate → Apply → Verify)
- Build pipelines (Compile → Test → Package → Deploy)

## Pipeline Architecture

```
Pipeline
├── Stage 1 (validates data)
├── Stage 2 (processes data)
├── Stage 3 (saves results)
└── [shared data dictionary]

Assembly
├── Pipeline 1 (process host A)
├── Pipeline 2 (process host B)
└── Pipeline 3 (process host C)
```

Key difference from ThreadPool:
- **ThreadPool**: Tasks run in parallel, independent
- **Pipeline**: Stages run sequentially, share data
- **Assembly**: Multiple pipelines run in parallel

## Creating Stages

Stages are the building blocks of pipelines. Create a custom stage by extending `pali.pipeline.Stage`.

### Basic Stage Template

```python
from pali.pipeline import Stage

class MyStage(Stage):
    def __init__(self, name):
        super(MyStage, self).__init__(name)
    
    def run(self, data):
        """
        data: dictionary shared with other stages
        """
        # Modify or read from data dictionary
        if 'key' in data:
            data['result'] = process(data['key'])
```

### Stage States

Each stage has a state:

```python
Stage.WAITING = 0x1      # Waiting to execute
Stage.RUNNING = 0x1 << 1 # Currently executing
Stage.PASSED = 0x1 << 2  # Completed successfully
Stage.FAILED = 0x1 << 3  # Failed with error
```

### Stage Examples

#### Validation Stage

```python
from pali.pipeline import Stage

class ValidateDataStage(Stage):
    def __init__(self):
        super(ValidateDataStage, self).__init__("Validate")
    
    def run(self, data):
        print(f"Validating data...")
        
        if not isinstance(data, dict):
            raise ValueError("Data must be a dictionary")
        
        required_keys = ['input', 'config']
        for key in required_keys:
            if key not in data:
                raise KeyError(f"Missing required key: {key}")
        
        print("✓ Validation passed")
```

#### Processing Stage

```python
class ProcessingStage(Stage):
    def __init__(self, multiplier=2):
        super(ProcessingStage, self).__init__("Processing")
        self.multiplier = multiplier
    
    def run(self, data):
        print("Processing data...")
        
        if 'numbers' in data:
            data['processed'] = [x * self.multiplier for x in data['numbers']]
        
        print(f"✓ Processing complete")
```

#### Output Stage

```python
import json

class OutputStage(Stage):
    def __init__(self, output_file):
        super(OutputStage, self).__init__("Output")
        self.output_file = output_file
    
    def run(self, data):
        print(f"Writing output to {self.output_file}...")
        
        with open(self.output_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        print("✓ Output written")
```

## Creating Pipelines

A pipeline combines multiple stages and manages shared data.

### Basic Pipeline Template

```python
from pali.pipeline import Pipeline, Stage

class MyPipeline(Pipeline):
    def __init__(self, data=None):
        stages = [
            ValidationStage(),
            ProcessingStage(),
            OutputStage("output.json")
        ]
        super(MyPipeline, self).__init__("MyPipeline", stages, data)
```

### Pipeline Example

```python
from pali.pipeline import Pipeline
from pali.worker import ThreadPool

# Define stages
validate_stage = ValidateDataStage()
process_stage = ProcessingStage(multiplier=3)
output_stage = OutputStage("result.json")

# Create pipeline
pipeline = Pipeline(
    name="DataProcessingPipeline",
    stages=[validate_stage, process_stage, output_stage],
    data={'numbers': [1, 2, 3, 4, 5]}
)

# Run pipeline
pipeline._run()

# Access results
print(pipeline.data)  # {'numbers': [...], 'processed': [...]}
```

### Pipeline with ThreadPool

Pipelines can be executed by a ThreadPool (since Pipeline extends Task):

```python
pipelines = [
    Pipeline(
        name=f"Pipeline_{i}",
        stages=[validate_stage, process_stage, output_stage],
        data={'numbers': list(range(i*10, (i+1)*10))}
    )
    for i in range(3)
]

with worker.ThreadPool(3) as tpool:
    for pipeline in pipelines:
        tpool.append_task(pipeline)

# Each pipeline runs on a separate thread
# Stages within each pipeline run sequentially
```

## Creating Assemblies

An assembly is a collection of related pipelines that run in parallel.

### Assembly Template

```python
from pali.pipeline import Assembly

class MyAssembly(Assembly):
    def __init__(self):
        pipelines = [
            self.create_pipeline("server1", "192.168.1.1"),
            self.create_pipeline("server2", "192.168.1.2"),
            self.create_pipeline("server3", "192.168.1.3"),
        ]
        super(MyAssembly, self).__init__(
            name="MyAssembly",
            pipelines=pipelines,
            max_concurrent_pipelines=2
        )
    
    def create_pipeline(self, name, ip):
        stages = [
            ValidateServerStage(),
            ConfigureServerStage(ip),
            VerifyServerStage(),
        ]
        return Pipeline(name, stages, data={'ip': ip})
```

### Assembly Example

```python
from pali.pipeline import Assembly, Pipeline, Stage

# Define stages for server configuration
class ValidateServerStage(Stage):
    def run(self, data):
        print(f"Validating server {data['ip']}...")

class ConfigureServerStage(Stage):
    def __init__(self, ip):
        super(ConfigureServerStage, self).__init__("Configure")
        self.ip = ip
    
    def run(self, data):
        print(f"Configuring {self.ip}...")
        data['config_status'] = 'applied'

class VerifyServerStage(Stage):
    def run(self, data):
        print(f"Verifying server {data['ip']}...")
        data['verified'] = True

# Create assembly
servers = ['server1', 'server2', 'server3']
ips = ['192.168.1.10', '192.168.1.11', '192.168.1.12']

pipelines = []
for name, ip in zip(servers, ips):
    stages = [
        ValidateServerStage(),
        ConfigureServerStage(ip),
        VerifyServerStage(),
    ]
    pipeline = Pipeline(name, stages, data={'ip': ip})
    pipelines.append(pipeline)

assembly = Assembly(
    name="ServerConfigAssembly",
    pipelines=pipelines,
    max_concurrent_pipelines=2  # Run 2 servers at a time
)

# Run assembly (automatically runs pipelines in parallel)
assembly._run()
```

## Stage Ordering

Stages in a pipeline are executed in the order they were added:

```python
stages = [
    Stage1(),  # Runs first
    Stage2(),  # Runs second
    Stage3(),  # Runs third
]

pipeline = Pipeline("MyPipeline", stages)
pipeline._run()
```

## Data Sharing

Pipelines use a data dictionary to share state between stages:

```python
from pali.pipeline import Pipeline, Stage

class ReadStage(Stage):
    def run(self, data):
        print(f"Reading: {data.get('value')}")

class WriteStage(Stage):
    def run(self, data):
        data['value'] = 42  # Write for next stage
        print(f"Wrote: {data['value']}")

class ModifyStage(Stage):
    def run(self, data):
        data['value'] *= 2  # Read and modify
        print(f"Modified to: {data['value']}")

pipeline = Pipeline(
    "DataPipeline",
    stages=[ReadStage(), WriteStage(), ModifyStage()],
    data={'value': None}
)

pipeline._run()
# Output:
# Reading: None
# Wrote: 42
# Modified to: 84
```

## Error Handling in Pipelines

If a stage raises an exception, the pipeline stops and logs the error:

```python
from pali.pipeline import Stage, Pipeline

class FailingStage(Stage):
    def run(self, data):
        raise ValueError("Intentional failure")

class NextStage(Stage):
    def run(self, data):
        print("This won't execute if FailingStage raises")

pipeline = Pipeline(
    "ErrorPipeline",
    stages=[FailingStage(), NextStage()]
)

try:
    pipeline._run()
except Exception as e:
    print(f"Pipeline error: {e}")
```

To handle errors gracefully:

```python
class SafeStage(Stage):
    def run(self, data):
        try:
            # Risky operation
            pass
        except Exception as e:
            # Log and continue
            data['error'] = str(e)
            print(f"Error handled: {e}")
```

## Real-World Example: ETL Pipeline

```python
from pali.pipeline import Pipeline, Stage
import csv
import json

class ExtractStage(Stage):
    def __init__(self, csv_file):
        super(ExtractStage, self).__init__("Extract")
        self.csv_file = csv_file
    
    def run(self, data):
        print("Extracting data...")
        rows = []
        with open(self.csv_file) as f:
            for row in csv.DictReader(f):
                rows.append(row)
        data['raw'] = rows

class TransformStage(Stage):
    def run(self, data):
        print("Transforming data...")
        transformed = []
        for row in data['raw']:
            transformed.append({
                'name': row['Name'].upper(),
                'age': int(row['Age']),
            })
        data['transformed'] = transformed

class LoadStage(Stage):
    def __init__(self, output_file):
        super(LoadStage, self).__init__("Load")
        self.output_file = output_file
    
    def run(self, data):
        print("Loading data...")
        with open(self.output_file, 'w') as f:
            json.dump(data['transformed'], f)

# Create and run ETL pipeline
pipeline = Pipeline(
    "ETLPipeline",
    stages=[
        ExtractStage("input.csv"),
        TransformStage(),
        LoadStage("output.json")
    ]
)

pipeline._run()
```

## Performance Considerations

- **Sequential Stages**: Pipeline stages always run one at a time
- **Parallel Pipelines**: Use Assembly for multiple pipelines in parallel
- **Data Dictionary**: Sharing large amounts of data between stages can be memory-intensive
- **Thread Count**: For Assembly, consider the number of pipelines and available CPU cores

## Next Steps

- [Thread Pool Guide](thread-pool.md) - Run multiple pipelines in parallel
- [Tasks Guide](tasks.md) - Learn about individual task units
- [Examples](../../examples/) - See real pipeline examples
