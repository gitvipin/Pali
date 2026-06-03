"""
Tests for examples from Logging Guide.

These tests verify that all code snippets in docs/guide/logging.md
actually work as described.
"""

import logging
import os
import shutil
import tempfile
import time
import unittest

from pali import logger as pali_logger
from pali.logger import getLogger, set_module_log_level, setup_logging
from pali.task import Task
from pali.worker import ThreadPool


class TestLoggingGuideExamples(unittest.TestCase):
    """Test examples from docs/guide/logging.md."""

    def tearDown(self):
        root_logger = logging.getLogger()
        for handler in list(root_logger.handlers):
            root_logger.removeHandler(handler)
            handler.close()
        root_logger.setLevel(logging.WARNING)
        pali_logger.LOG_SETUP_DONE = False

    def _create_temp_log_dir(self):
        return tempfile.mkdtemp(prefix='pali-logging-test-')

    def _read_log_file(self, log_dir, log_file):
        log_path = os.path.join(log_dir, log_file)
        with open(log_path, 'r') as handle:
            return handle.read()

    def test_setup_logging_creates_log_file(self):
        """Test that setup_logging creates the target log file and writes entries."""
        log_dir = self._create_temp_log_dir()
        try:
            setup_logging(log_dir=log_dir, log_file='pali.log', log_level=logging.DEBUG)
            log = getLogger(__name__)
            log.info("Application started")
            log.debug("Debug message")

            for handler in logging.getLogger().handlers:
                handler.flush()

            contents = self._read_log_file(log_dir, 'pali.log')
            self.assertIn('Application started', contents)
            self.assertIn('Debug message', contents)
        finally:
            shutil.rmtree(log_dir, ignore_errors=True)

    def test_set_module_log_level_affects_logger(self):
        """Test that set_module_log_level changes a module logger's level."""
        log_dir = self._create_temp_log_dir()
        try:
            setup_logging(log_dir=log_dir, log_file='pali.log', log_level=logging.INFO)
            set_module_log_level(__name__, 'DEBUG')

            module_logger = getLogger(__name__)
            self.assertEqual(module_logger.level, logging.DEBUG)

            module_logger.debug('Debug message')
            for handler in logging.getLogger().handlers:
                handler.flush()

            contents = self._read_log_file(log_dir, 'pali.log')
            self.assertIn('Debug message', contents)
        finally:
            shutil.rmtree(log_dir, ignore_errors=True)

    def test_complete_logging_example_writes_task_messages(self):
        """Test that the complete logging example writes task lifecycle messages."""
        log_dir = self._create_temp_log_dir()
        try:
            setup_logging(log_dir=log_dir, log_file='application.log', log_level=logging.DEBUG)
            log = getLogger(__name__)

            class WorkTask(Task):
                def __init__(self, task_id, duration):
                    super(WorkTask, self).__init__()
                    self.task_id = task_id
                    self.duration = duration
                    self.completed = False
                    self.log = getLogger(__name__)

                def _run(self):
                    self.log.info(f"Task {self.task_id} started")
                    time.sleep(self.duration)
                    self.log.info(f"Task {self.task_id} completed in {self.duration}s")
                    self.completed = True

            tasks = [WorkTask(i, 0.01) for i in range(3)]
            log.info('=' * 50)
            log.info('Application started')
            log.info('=' * 50)

            with ThreadPool(3) as tpool:
                for task_obj in tasks:
                    log.debug(f"Appending task {task_obj.task_id}")
                    tpool.append_task(task_obj)

            log.info('All tasks completed')

            for handler in logging.getLogger().handlers:
                handler.flush()

            contents = self._read_log_file(log_dir, 'application.log')
            self.assertIn('Application started', contents)
            self.assertIn('Task 0 started', contents)
            self.assertIn('Task 0 completed in 0.01s', contents)
            self.assertIn('All tasks completed', contents)
            self.assertTrue(all(task_obj.completed for task_obj in tasks))
        finally:
            shutil.rmtree(log_dir, ignore_errors=True)


if __name__ == '__main__':
    unittest.main()
