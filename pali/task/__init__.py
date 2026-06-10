"""
Task package — task execution, pipelines, and assembly.
"""

from pali.task.task import Task
from pali.task.pipeline import Pipeline, Assembly, Stage

__all__ = [
    'Task', 'Pipeline', 'Assembly', 'Stage'
]
