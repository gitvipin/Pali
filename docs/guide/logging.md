# Logging Guide

Pali provides a simple logging setup utility that integrates with Python's standard logging module.

## Overview

Pali's logging system:

- Built on Python's standard `logging` module
- Configurable log level and format
- File-based logging with automatic directory creation
- Per-module log level control
- Thread-aware logging (includes thread name in logs)

## Basic Setup

### Simple Setup

```python
from pali.logger import setup_logging, getLogger

# Initialize logging (call once at startup)
setup_logging()

# Get a logger for your module
log = getLogger(__name__)

# Use the logger
log.info("Application started")
log.debug("Debug message")
log.warning("Warning message")
log.error("Error message")
log.critical("Critical message")
```

### Custom Configuration

```python
from pali.logger import setup_logging, getLogger
import logging

# Setup with custom parameters
setup_logging(
    log_dir='./logs',              # Where to write log files
    log_file='myapp.log',          # Log file name
    log_level=logging.DEBUG        # Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
)

log = getLogger(__name__)
log.debug("This debug message will now be logged")
```

## Logging Levels

From least to most severe:

```python
import logging

logging.DEBUG       # Detailed information for diagnostics
logging.INFO        # Confirmation that things are working as expected
logging.WARNING     # Something unexpected or indicative of a problem (default)
logging.ERROR       # A serious problem
logging.CRITICAL    # A very serious problem
```

### Level Examples

```python
from pali.logger import getLogger

log = getLogger(__name__)

# DEBUG - detailed tracing
log.debug(f"Processing item: {item_id}")
log.debug(f"Request parameters: {params}")

# INFO - normal operation
log.info("Server started on port 8000")
log.info(f"Processed {count} items")

# WARNING - something unexpected
log.warning(f"Connection timeout after {timeout}s")
log.warning("Deprecated method used")

# ERROR - a problem occurred
log.error(f"Failed to save data: {error}")
log.error("Database connection failed")

# CRITICAL - serious problem
log.critical("Out of memory!")
log.critical("Configuration is invalid")
```

## Setup Parameters

### `log_dir`

Directory where log files are written. Created automatically if it doesn't exist.

```python
from pali.logger import setup_logging

setup_logging(log_dir='./logs')           # Relative path
setup_logging(log_dir='/var/log/pali')    # Absolute path
```

Default: `./` (current directory)

### `log_file`

Name of the log file.

```python
from pali.logger import setup_logging

setup_logging(log_file='myapp.log')
setup_logging(log_file='pali.log')
```

Default: `pali.log`

### `log_level`

Minimum log level to record.

```python
from pali.logger import setup_logging
import logging

setup_logging(log_level=logging.DEBUG)       # Verbose
setup_logging(log_level=logging.INFO)        # Normal
setup_logging(log_level=logging.WARNING)     # Warnings and errors only
setup_logging(log_level=logging.ERROR)       # Errors and critical only
```

Default: `logging.INFO`

## Log Format

Default log format:

```
2024-01-15 10:30:45,123::INFO::MainThread::module[0042]::Application started
timestamp::level::thread::module[line]::message
```

Fields:
- `%(asctime)s` - Timestamp
- `%(levelname)s` - Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `%(threadName)s` - Name of the thread
- `%(module)s` - Module name
- `%(lineno)s` - Line number
- `%(message)s` - Log message

## Using Loggers in Your Code

### Module-Level Logger

```python
# mymodule.py
from pali.logger import getLogger

log = getLogger(__name__)

def process_data(data):
    log.info(f"Processing data with {len(data)} items")
    try:
        result = do_work(data)
        log.info("Processing complete")
        return result
    except Exception as e:
        log.error(f"Processing failed: {e}")
        raise
```

### Class-Based Logger

```python
from pali.logger import getLogger

class DataProcessor:
    def __init__(self):
        self.log = getLogger(__name__)
    
    def process(self, data):
        self.log.info("Starting processing")
        try:
            result = self._do_work(data)
            self.log.info("Processing finished")
            return result
        except Exception as e:
            self.log.error(f"Error: {e}")
            raise
    
    def _do_work(self, data):
        self.log.debug(f"Work with {len(data)} items")
        return [x * 2 for x in data]
```

## Controlling Module Log Levels

Set specific log levels for different modules:

```python
from pali.logger import setup_logging, set_module_log_level
import logging

# Setup general logging
setup_logging(log_level=logging.INFO)

# Reduce verbosity of third-party libraries
set_module_log_level('requests', 'WARNING')  # Don't log requests debug info
set_module_log_level('urllib3', 'WARNING')   # Don't log urllib3 debug info

# Increase verbosity for your own modules
set_module_log_level('myapp.database', 'DEBUG')
```

## Complete Example

**File: `main.py`**

```python
from pali.logger import setup_logging, getLogger
from pali.worker import ThreadPool
from pali.task import Task
import logging
import time

# Setup logging at application startup
setup_logging(
    log_dir='./logs',
    log_file='application.log',
    log_level=logging.INFO
)

log = getLogger(__name__)

class WorkTask(Task):
    def __init__(self, task_id, duration):
        super(WorkTask, self).__init__()
        self.task_id = task_id
        self.duration = duration
        self.log = getLogger(__name__)
    
    def _run(self):
        self.log.info(f"Task {self.task_id} started")
        try:
            time.sleep(self.duration)
            self.log.info(f"Task {self.task_id} completed in {self.duration}s")
        except Exception as e:
            self.log.error(f"Task {self.task_id} failed: {e}")

def main():
    log.info("=" * 50)
    log.info("Application started")
    log.info("=" * 50)
    
    try:
        tasks = [WorkTask(i, i*0.1) for i in range(5)]
        
        log.info(f"Creating thread pool with 3 threads")
        with ThreadPool(3) as tpool:
            for t in tasks:
                log.debug(f"Appending task {t.task_id}")
                tpool.append_task(t)
        
        log.info("All tasks completed")
        
    except Exception as e:
        log.error(f"Application error: {e}", exc_info=True)
        raise

if __name__ == "__main__":
    main()
    log.info("Application finished")
```

**Output in `logs/application.log`:**

```
2024-01-15 10:30:45,000::INFO::MainThread::main[44]::==================================================
2024-01-15 10:30:45,001::INFO::MainThread::main[45]::Application started
2024-01-15 10:30:45,002::INFO::MainThread::main[46]::==================================================
2024-01-15 10:30:45,003::INFO::MainThread::main[51]::Creating thread pool with 3 threads
2024-01-15 10:30:45,004::DEBUG::MainThread::main[52]::Appending task 0
2024-01-15 10:30:45,005::DEBUG::MainThread::main[52]::Appending task 1
2024-01-15 10:30:45,006::DEBUG::MainThread::main[52]::Appending task 2
2024-01-15 10:30:45,007::DEBUG::MainThread::main[52]::Appending task 3
2024-01-15 10:30:45,008::DEBUG::MainThread::main[52]::Appending task 4
2024-01-15 10:30:45,009::INFO::Thread-1::main[15]::Task 0 started
2024-01-15 10:30:45,010::INFO::Thread-2::main[15]::Task 1 started
2024-01-15 10:30:45,011::INFO::Thread-3::main[15]::Task 2 started
2024-01-15 10:30:45,019::INFO::Thread-1::main[17]::Task 0 completed in 0.0s
2024-01-15 10:30:45,020::INFO::Thread-1::main[15]::Task 3 started
```

## Best Practices

### 1. Use Appropriate Log Levels

```python
log = getLogger(__name__)

# Bad - everything is INFO
log.info("Starting operation")
log.info(f"Value: {x}")
log.info(f"Another value: {y}")

# Good - use appropriate levels
log.info("Starting operation")
log.debug(f"Value: {x}")
log.debug(f"Another value: {y}")
```

### 2. Include Context in Error Logs

```python
log = getLogger(__name__)

# Bad
except Exception as e:
    log.error("Error occurred")

# Good
except Exception as e:
    log.error(f"Failed to save user {user_id}: {e}")
```

### 3. Use exc_info for Exceptions

```python
log = getLogger(__name__)

try:
    risky_operation()
except Exception as e:
    # This includes full stack trace
    log.error("Operation failed", exc_info=True)
```

### 4. Initialize Logging Once

```python
# main.py - Initialize once at startup
from pali.logger import setup_logging

setup_logging(log_dir='./logs', log_level='INFO')

# All other modules
from pali.logger import getLogger

log = getLogger(__name__)
```

### 5. Use Loggers, Not print()

```python
# Avoid
print("Processing item", item_id)

# Good
log = getLogger(__name__)
log.info(f"Processing item {item_id}")
```

## Troubleshooting

### Logs Not Being Written

1. Check that log directory exists or is writable:
   ```python
   import os
   log_dir = './logs'
   os.makedirs(log_dir, exist_ok=True)
   ```

2. Verify setup_logging() is called:
   ```python
   from pali.logger import setup_logging
   setup_logging()  # Call once at startup
   ```

3. Check log level:
   ```python
   import logging
   setup_logging(log_level=logging.DEBUG)  # DEBUG shows everything
   ```

### Only Seeing Some Log Levels

```python
from pali.logger import setup_logging
import logging

# Increase verbosity
setup_logging(log_level=logging.DEBUG)

# Or set specific module levels
from pali.logger import set_module_log_level
set_module_log_level('myapp', 'DEBUG')
```

## Next Steps

- [Configuration Guide](configuration.md) - Configure logging via config files
- [Thread Pool Guide](thread-pool.md) - Use logging with thread pools
- [A/B Testing Guide](ab-testing.md) - Log A/B testing events
