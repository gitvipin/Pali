# Configuration Guide

Pali provides a configuration management system that reads configuration from `.ini` files and supports parameter overrides.

## Overview

The configuration system uses Python's `configparser` to load configuration from `.ini` files. It supports:

- Multiple configuration sections
- Parameter value type checking
- Configuration overrides
- Default values

## Basic Setup

### Step 1: Create a Configuration File

Create a `.ini` file with your configuration. Example: `config/pali.cfg`

```ini
[DEFAULT]
log_level = INFO
max_threads = 4

[DATABASE]
host = localhost
port = 5432
database = myapp

[API]
timeout = 30
retries = 3
```

### Step 2: Load Configuration

```python
from pali.config import ConfigManager

# Load configuration
cfg = ConfigManager(config_file_path='config/pali.cfg')

# Get values from sections
db_host = cfg.get('DATABASE', 'host')
api_timeout = cfg.get('API', 'timeout')
```

## ConfigManager API

### Creating a ConfigManager

```python
from pali.config import ConfigManager

# Load from default location
cfg = ConfigManager()

# Load from custom location
cfg = ConfigManager(config_file_path='/path/to/config.cfg')

# Load with parameter values
cfg = ConfigManager(
    config_file_path='config/pali.cfg',
    param_vals={'key': 'value'}
)
```

### Reading Configuration

```python
from pali.config import ConfigManager

cfg = ConfigManager('config/pali.cfg')

# Get a value from a section
value = cfg.get('SECTION_NAME', 'key')

# Get with type conversion
timeout = int(cfg.get('API', 'timeout'))
enabled = cfg.getboolean('FEATURE', 'enabled')
float_value = cfg.getfloat('CALCULATION', 'precision')

# List all options in a section
options = cfg.options('DATABASE')

# List all sections
sections = cfg.sections()

# Check if option exists
has_option = cfg.has_option('DATABASE', 'host')
```

### Working with Sections

```python
from pali.config import ConfigManager

cfg = ConfigManager('config/pali.cfg')

# Set the active section
cfg.set_section('DATABASE')

# Get value from active section
host = cfg.get('DATABASE', 'host')

# Get from active section (shorthand)
# cfg.get('host')  # This will use the active section
```

## Configuration File Format

Configuration files use the standard `.ini` format:

```ini
# Comments start with #

[SECTION_NAME]
key1 = value1
key2 = value2

[ANOTHER_SECTION]
key3 = value3
```

### Common Sections

**[DEFAULT]** - Default values available to all sections

```ini
[DEFAULT]
debug = false
timeout = 30
```

**[DATABASE]** - Database configuration

```ini
[DATABASE]
host = localhost
port = 5432
name = myapp
user = admin
```

**[LOGGING]** - Logging configuration

```ini
[LOGGING]
level = INFO
file = logs/app.log
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**[API]** - API configuration

```ini
[API]
base_url = https://api.example.com
timeout = 30
retries = 3
```

## Type Conversion

Configuration values are stored as strings. Use type conversion methods:

```python
from pali.config import ConfigManager

cfg = ConfigManager('config/pali.cfg')

# String (default)
name = cfg.get('SERVICE', 'name')

# Integer
port = cfg.getint('SERVICE', 'port')

# Float
precision = cfg.getfloat('CALCULATION', 'precision')

# Boolean
enabled = cfg.getboolean('FEATURE', 'enabled')
```

### Boolean Values

For `getboolean()`, these values are considered True:
- '1', 'yes', 'true', 'on' (case-insensitive)

These values are considered False:
- '0', 'no', 'false', 'off' (case-insensitive)

## Configuration with Parameters

Pali supports parameters that can override configuration values:

```python
from pali.config import ConfigManager
from pali import params

# Define parameters
params.add_param('db_host', 'localhost', str)
params.add_param('db_port', 5432, int)

# Create ConfigManager with parameters
param_vals = {
    'db_host': params.get_param('db_host'),
    'db_port': params.get_param('db_port'),
}

cfg = ConfigManager(
    config_file_path='config/pali.cfg',
    param_vals=param_vals
)
```

## Example: Complete Configuration

**File: `config/app.cfg`**

```ini
[DEFAULT]
debug = true
log_level = INFO

[DATABASE]
host = localhost
port = 5432
name = myapp_db
username = admin
password = secret123
pool_size = 10

[CACHE]
enabled = true
ttl = 3600
max_entries = 1000

[API]
base_url = https://api.example.com
timeout = 30
retries = 3
max_connections = 100

[LOGGING]
file = logs/app.log
format = %(asctime)s - %(name)s - %(levelname)s - %(message)s
```

**Code to use it:**

```python
from pali.config import ConfigManager

class AppConfig:
    def __init__(self, config_path='config/app.cfg'):
        self.cfg = ConfigManager(config_path)
    
    def get_db_config(self):
        return {
            'host': self.cfg.get('DATABASE', 'host'),
            'port': self.cfg.getint('DATABASE', 'port'),
            'name': self.cfg.get('DATABASE', 'name'),
            'user': self.cfg.get('DATABASE', 'username'),
            'password': self.cfg.get('DATABASE', 'password'),
            'pool_size': self.cfg.getint('DATABASE', 'pool_size'),
        }
    
    def get_api_config(self):
        return {
            'base_url': self.cfg.get('API', 'base_url'),
            'timeout': self.cfg.getint('API', 'timeout'),
            'retries': self.cfg.getint('API', 'retries'),
        }
    
    def is_debug(self):
        return self.cfg.getboolean('DEFAULT', 'debug')

# Usage
app_cfg = AppConfig()
print(app_cfg.get_db_config())
print(app_cfg.get_api_config())
print(f"Debug mode: {app_cfg.is_debug()}")
```

## Common Patterns

### Environment-Specific Configuration

Use different config files for different environments:

```python
import os
from pali.config import ConfigManager

env = os.getenv('APP_ENV', 'development')
config_file = f'config/{env}.cfg'

cfg = ConfigManager(config_file)
```

### Configuration with Defaults

```python
from pali.config import ConfigManager

cfg = ConfigManager('config/pali.cfg')

# Use get() with a default value fallback
timeout = cfg.get('API', 'timeout') if cfg.has_option('API', 'timeout') else '30'
```

### Reading Custom Sections

```python
from pali.config import ConfigManager

cfg = ConfigManager('config/pali.cfg')

# Dynamically read sections for multiple instances
for section in cfg.sections():
    if section.startswith('SERVER_'):
        server_config = dict(cfg.items(section))
        print(f"Server: {server_config}")
```

## Best Practices

### 1. Use Section Names Consistently

```ini
# Good - clear, organized
[DATABASE]
[CACHE]
[API]

# Avoid - inconsistent naming
[database]
[CACHE]
[apis]
```

### 2. Use Descriptive Keys

```ini
# Good
[API]
connection_timeout = 30
max_retries = 3

# Avoid
[API]
timeout = 30
retries = 3
```

### 3. Use [DEFAULT] for Shared Values

```ini
[DEFAULT]
timeout = 30
log_level = INFO

[API]
# Inherits timeout = 30

[DATABASE]
# Inherits log_level = INFO
```

### 4. Store Sensitive Data Carefully

```python
# Good - use environment variables
import os
db_password = os.getenv('DB_PASSWORD')

# Avoid - storing secrets in config files
# [DATABASE]
# password = secret123
```

### 5. Validate Configuration at Startup

```python
from pali.config import ConfigManager

def validate_config(config_path):
    cfg = ConfigManager(config_path)
    
    required_sections = ['DATABASE', 'API']
    for section in required_sections:
        if not cfg.has_section(section):
            raise ValueError(f"Missing required section: {section}")
    
    required_keys = {
        'DATABASE': ['host', 'port'],
        'API': ['base_url', 'timeout'],
    }
    
    for section, keys in required_keys.items():
        for key in keys:
            if not cfg.has_option(section, key):
                raise ValueError(f"Missing required key {key} in {section}")
    
    return cfg

cfg = validate_config('config/pali.cfg')
```

## Next Steps

- [Logging Guide](logging.md) - Learn how to set up logging
- [A/B Testing Guide](ab-testing.md) - Configure A/B testing with parameters
- [Thread Pool Guide](thread-pool.md) - Use configuration with thread pools
