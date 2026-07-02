import sys

name = "pali"
__version__ = '1.1.0'

# Import directly from moved module files (avoid circular imports)
from pali.task.task import Task
from pali.threading.worker import ThreadPool, WorkerPool, WorkerThread
from pali.task.pipeline import Pipeline, Assembly, Stage
from pali.config.config import ConfigManager, get_param, get_config_manager
from pali.config.params import Parameter, DistType
from pali.utils.bbuffer import ProducerConsumer
from pali.utils.logger import getLogger, setup_logging, set_module_log_level
from pali.utils.console import Console
from pali.threading.thread import Thread, ThreadTaskLoop

# Expose subpackages for module-level imports
from pali import (
    threading, task, config, utils,
    common, constants
)

# Backward compatibility: register old module paths in sys.modules
# This allows: from pali.worker import ThreadPool (old path still works)
# Map old flat module paths to actual module locations
import pali.threading.worker
import pali.threading.thread
import pali.task.task
import pali.task.pipeline
import pali.config.config
import pali.config.params
import pali.utils.bbuffer
import pali.utils.logger
import pali.utils.console

sys.modules['pali.worker'] = sys.modules['pali.threading.worker']
sys.modules['pali.thread'] = sys.modules['pali.threading.thread']
sys.modules['pali.task'] = sys.modules['pali.task.task']
sys.modules['pali.pipeline'] = sys.modules['pali.task.pipeline']
sys.modules['pali.config'] = sys.modules['pali.config.config']
sys.modules['pali.params'] = sys.modules['pali.config.params']
sys.modules['pali.bbuffer'] = sys.modules['pali.utils.bbuffer']
sys.modules['pali.logger'] = sys.modules['pali.utils.logger']
sys.modules['pali.console'] = sys.modules['pali.utils.console']

__all__ = [
    # Core classes
    'Task',
    'ThreadPool', 'WorkerPool', 'WorkerThread',
    'Pipeline', 'Assembly', 'Stage',
    'ConfigManager', 'get_param', 'get_config_manager',
    'Parameter', 'DistType',
    'ProducerConsumer',
    # Logger functions
    'getLogger', 'setup_logging', 'set_module_log_level',
    # Utilities
    'Console',
    'Thread', 'ThreadTaskLoop',
    # Subpackages for backward compatibility
    'threading', 'task', 'config', 'utils',
    'common', 'constants'
]
