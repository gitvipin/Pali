name = "pali"
__version__ = '1.0.1'

# Core task execution
from pali.task import Task
from pali.worker import ThreadPool, WorkerPool, WorkerThread

# Pipeline and assembly
from pali.pipeline import Pipeline, Assembly, Stage

# Configuration and parameters
from pali.config import ConfigManager
from pali.params import Parameter, DistType

# Utilities
from pali.bbuffer import ProducerConsumer
from pali.logger import getLogger, setup_logging, set_module_log_level
from pali.console import Console
from pali.thread import Thread, ThreadTaskLoop

# Expose submodules for explicit imports (backward compatibility)
# Note: parallel module is lazy-loaded due to config initialization side-effects
from pali import (
    task, worker, pipeline, config, params,
    bbuffer, logger, console, thread, common,
    constants
)

__all__ = [
    # Core classes
    'Task',
    'ThreadPool', 'WorkerPool', 'WorkerThread',
    'Pipeline', 'Assembly', 'Stage',
    'ConfigManager',
    'Parameter', 'DistType',
    'ProducerConsumer',
    # Logger functions
    'getLogger', 'setup_logging', 'set_module_log_level',
    # Utilities
    'Console',
    'Thread', 'ThreadTaskLoop',
    # Submodules for backward compatibility
    'task', 'worker', 'pipeline', 'config', 'params',
    'bbuffer', 'logger', 'console', 'thread', 'common',
    'constants'
]
