# Architecture

Pali provides several architectural patterns for building concurrent and sequential applications. This guide explains the core models and how they work together.

## ThreadPool Model

The ThreadPool manages a fixed number of worker threads that process tasks from a queue:

```
ThreadPool (manages N worker threads)
├── Worker Thread 1 (processes tasks)
├── Worker Thread 2 (processes tasks)
├── Worker Thread 3 (processes tasks)
└── ...

Task Queue → Worker Threads → Task Execution
```

### How It Works
1. Tasks are added to a queue
2. Available worker threads pick up tasks from the queue
3. Each worker executes the task's `_run()` method
4. Results are stored as task attributes
5. Main thread can retrieve results after tasks complete

**Best for:** I/O-bound operations (network requests, file I/O, database queries), batch processing, and concurrent task execution.

## Pipeline Model

The Pipeline executes stages sequentially, with each stage processing shared data:

```
Pipeline
├── Stage 1 (validation)
├── Stage 2 (processing)
└── Stage 3 (output)
     ↓
   Shared Data Dictionary
```

### How It Works
1. Each stage receives the shared data dictionary
2. Stage processes and modifies the data
3. Next stage receives updated data
4. Final stage produces output

**Best for:** ETL workflows, data transformation, sequential processing with dependencies.

## Assembly Model

The Assembly manages multiple pipelines running in parallel:

```
Assembly (manages multiple pipelines in parallel)
├── Pipeline 1 (server A)
├── Pipeline 2 (server B)
└── Pipeline 3 (server C)
```

### How It Works
1. Multiple independent pipelines run concurrently
2. Each pipeline has its own data context
3. Pipelines can be monitored and controlled independently
4. Useful for processing multiple items through same workflow

**Best for:** Processing multiple independent workflows, multi-tenant processing, distributed data handling.

## Choosing the Right Model

| Use Case | Model | Why |
|----------|-------|-----|
| Parallel tasks, same operation | ThreadPool | Efficient for I/O-bound work |
| Sequential stages, shared data | Pipeline | Maintains execution order and state |
| Multiple parallel workflows | Assembly | Processes multiple items independently |
| Mixed: parallel execution of sequential workflows | ThreadPool + Pipeline | Combine models for complex scenarios |

## Performance Characteristics

### ThreadPool
- **Thread Overhead**: Fixed number of threads created once
- **Scalability**: Scales with number of available cores and I/O concurrency
- **Memory**: Minimal per-task overhead

### Pipeline
- **Execution**: Linear, predictable
- **Memory**: Single data dictionary shared across stages
- **Speed**: Limited by slowest stage

### Assembly
- **Concurrency**: Multiple pipelines process independently
- **Resource**: Scales with available CPU and memory
- **Complexity**: Higher management overhead

---

For examples of these patterns in action, see [Application Examples](examples.md).
