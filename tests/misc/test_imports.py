#!/usr/bin/env python
'''
Unit tests to validate import compatibility and public API surface.

This test module ensures that:
1. New short import paths work (from pali import ThreadPool, Task, etc.)
2. Old import paths remain functional (from pali.worker import ThreadPool, etc.)
3. Both import styles reference the same classes (backward compatibility)
4. Public API is properly exposed via __all__
'''

import unittest
import sys


class TestImportCompatibility(unittest.TestCase):
    '''Test new and old import styles work and reference same classes.'''

    def test_new_import_threadpool(self):
        '''Test new import style: from pali import ThreadPool'''
        from pali import ThreadPool
        self.assertIsNotNone(ThreadPool)
        self.assertEqual(ThreadPool.__name__, 'ThreadPool')

    def test_new_import_task(self):
        '''Test new import style: from pali import Task'''
        from pali import Task
        self.assertIsNotNone(Task)
        self.assertEqual(Task.__name__, 'Task')

    def test_new_import_pipeline(self):
        '''Test new import style: from pali import Pipeline'''
        from pali import Pipeline
        self.assertIsNotNone(Pipeline)
        self.assertEqual(Pipeline.__name__, 'Pipeline')

    def test_new_import_assembly(self):
        '''Test new import style: from pali import Assembly'''
        from pali import Assembly
        self.assertIsNotNone(Assembly)
        self.assertEqual(Assembly.__name__, 'Assembly')

    def test_new_import_stage(self):
        '''Test new import style: from pali import Stage'''
        from pali import Stage
        self.assertIsNotNone(Stage)
        self.assertEqual(Stage.__name__, 'Stage')

    def test_new_import_configmanager(self):
        '''Test new import style: from pali import ConfigManager'''
        from pali import ConfigManager
        self.assertIsNotNone(ConfigManager)
        self.assertEqual(ConfigManager.__name__, 'ConfigManager')

    def test_new_import_parameter(self):
        '''Test new import style: from pali import Parameter'''
        from pali import Parameter
        self.assertIsNotNone(Parameter)
        self.assertEqual(Parameter.__name__, 'Parameter')

    def test_new_import_producer_consumer(self):
        '''Test new import style: from pali import ProducerConsumer'''
        from pali import ProducerConsumer
        self.assertIsNotNone(ProducerConsumer)
        self.assertEqual(ProducerConsumer.__name__, 'ProducerConsumer')

    def test_new_import_logger_functions(self):
        '''Test new import style: logger functions from pali'''
        from pali import getLogger, setup_logging, set_module_log_level
        self.assertIsNotNone(getLogger)
        self.assertIsNotNone(setup_logging)
        self.assertIsNotNone(set_module_log_level)

    def test_old_import_threadpool(self):
        '''Test old import style: from pali.worker import ThreadPool'''
        from pali.worker import ThreadPool
        self.assertIsNotNone(ThreadPool)
        self.assertEqual(ThreadPool.__name__, 'ThreadPool')

    def test_old_import_task(self):
        '''Test old import style: from pali.task import Task'''
        from pali.task import Task
        self.assertIsNotNone(Task)
        self.assertEqual(Task.__name__, 'Task')

    def test_old_import_pipeline(self):
        '''Test old import style: from pali.pipeline import Pipeline'''
        from pali.pipeline import Pipeline
        self.assertIsNotNone(Pipeline)
        self.assertEqual(Pipeline.__name__, 'Pipeline')

    def test_old_import_config(self):
        '''Test old import style: from pali.config import ConfigManager'''
        from pali.config import ConfigManager
        self.assertIsNotNone(ConfigManager)
        self.assertEqual(ConfigManager.__name__, 'ConfigManager')

    def test_backward_compatibility_threadpool(self):
        '''Verify old and new imports reference the same ThreadPool class'''
        from pali import ThreadPool as new_style
        from pali.worker import ThreadPool as old_style
        self.assertIs(new_style, old_style)

    def test_backward_compatibility_task(self):
        '''Verify old and new imports reference the same Task class'''
        from pali import Task as new_style
        from pali.task import Task as old_style
        self.assertIs(new_style, old_style)

    def test_backward_compatibility_pipeline(self):
        '''Verify old and new imports reference the same Pipeline class'''
        from pali import Pipeline as new_style
        from pali.pipeline import Pipeline as old_style
        self.assertIs(new_style, old_style)

    def test_backward_compatibility_assembly(self):
        '''Verify old and new imports reference the same Assembly class'''
        from pali import Assembly as new_style
        from pali.pipeline import Assembly as old_style
        self.assertIs(new_style, old_style)

    def test_backward_compatibility_configmanager(self):
        '''Verify old and new imports reference the same ConfigManager class'''
        from pali import ConfigManager as new_style
        from pali.config import ConfigManager as old_style
        self.assertIs(new_style, old_style)

    def test_submodule_access(self):
        '''Test that submodules are accessible via pali package'''
        from pali import task, worker, pipeline, config, params
        self.assertIsNotNone(task)
        self.assertIsNotNone(worker)
        self.assertIsNotNone(pipeline)
        self.assertIsNotNone(config)
        self.assertIsNotNone(params)

    def test_multiple_imports_in_one_statement(self):
        '''Test multiple imports in a single statement (new style)'''
        from pali import (
            ThreadPool, Task, Pipeline, Assembly, Stage,
            ConfigManager, Parameter, ProducerConsumer
        )
        self.assertIsNotNone(ThreadPool)
        self.assertIsNotNone(Task)
        self.assertIsNotNone(Pipeline)
        self.assertIsNotNone(Assembly)
        self.assertIsNotNone(Stage)
        self.assertIsNotNone(ConfigManager)
        self.assertIsNotNone(Parameter)
        self.assertIsNotNone(ProducerConsumer)

    def test_all_export_list(self):
        '''Verify __all__ export list is properly defined'''
        import pali
        self.assertTrue(hasattr(pali, '__all__'))
        self.assertIsInstance(pali.__all__, list)
        self.assertGreater(len(pali.__all__), 0)

        # Verify key exports are in __all__
        expected_exports = [
            'Task', 'ThreadPool', 'Pipeline', 'Assembly', 'Stage',
            'ConfigManager', 'Parameter', 'ProducerConsumer',
            'getLogger', 'setup_logging', 'set_module_log_level'
        ]
        for export in expected_exports:
            self.assertIn(export, pali.__all__,
                         f"'{export}' not found in pali.__all__")

    def test_version_info(self):
        '''Verify version information is present'''
        import pali
        self.assertTrue(hasattr(pali, '__version__'))
        self.assertTrue(hasattr(pali, 'name'))
        self.assertEqual(pali.name, 'pali')
        # Version should be a non-empty string
        self.assertIsInstance(pali.__version__, str)
        self.assertGreater(len(pali.__version__), 0)


class TestWorkerPoolVariants(unittest.TestCase):
    '''Test that WorkerPool variants are accessible'''

    def test_worker_pool_import(self):
        '''Test WorkerPool import (base class)'''
        from pali import WorkerPool
        self.assertIsNotNone(WorkerPool)
        self.assertEqual(WorkerPool.__name__, 'WorkerPool')

    def test_worker_thread_import(self):
        '''Test WorkerThread import'''
        from pali import WorkerThread
        self.assertIsNotNone(WorkerThread)
        self.assertEqual(WorkerThread.__name__, 'WorkerThread')

    def test_thread_classes(self):
        '''Test Thread and ThreadTaskLoop imports'''
        from pali import Thread, ThreadTaskLoop
        self.assertIsNotNone(Thread)
        self.assertIsNotNone(ThreadTaskLoop)

    def test_console_import(self):
        '''Test Console utility import'''
        from pali import Console
        self.assertIsNotNone(Console)
        self.assertEqual(Console.__name__, 'Console')


class TestParameterVariants(unittest.TestCase):
    '''Test parameter-related imports'''

    def test_dist_type_import(self):
        '''Test DistType import (parameter distribution type)'''
        from pali import DistType
        self.assertIsNotNone(DistType)
        self.assertEqual(DistType.__name__, 'DistType')

    def test_parameter_old_style(self):
        '''Test old import style for Parameter'''
        from pali.params import Parameter
        self.assertIsNotNone(Parameter)

    def test_parameter_backward_compat(self):
        '''Verify Parameter old and new import style compatibility'''
        from pali import Parameter as new_style
        from pali.params import Parameter as old_style
        self.assertIs(new_style, old_style)


if __name__ == '__main__':
    unittest.main()
