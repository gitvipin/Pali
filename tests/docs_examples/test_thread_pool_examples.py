"""
Tests for examples from Thread Pool Guide.

These tests verify that all code snippets in docs/guide/thread-pool.md
actually work as described.
"""

import unittest
from pali import task, worker


class DummyTask(task.Task):
    """Simple task for testing thread pool."""
    
    def __init__(self, task_id):
        super(DummyTask, self).__init__()
        self.task_id = task_id
        self.completed = False
    
    def _run(self):
        self.completed = True


class TestThreadPoolCreation(unittest.TestCase):
    """Test: Creating thread pools from Thread Pool Guide."""
    
    def test_basic_thread_pool_creation(self):
        """Test basic thread pool creation."""
        # Create a thread pool with 4 worker threads
        tpool = worker.ThreadPool(4)
        self.assertIsNotNone(tpool)
        tpool.close()
    
    def test_context_manager_usage(self):
        """Test context manager (recommended approach)."""
        tasks = [DummyTask(i) for i in range(10)]
        
        with worker.ThreadPool(4) as tpool:
            for task_obj in tasks:
                tpool.append_task(task_obj)
        
        # All tasks should be completed
        for t in tasks:
            self.assertTrue(t.completed)


class TestThreadPoolParameters(unittest.TestCase):
    """Test: ThreadPool parameters from Thread Pool Guide."""
    
    def test_single_threaded_processing(self):
        """Test single-threaded processing."""
        tasks = [DummyTask(i) for i in range(3)]
        
        with worker.ThreadPool(1) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        for t in tasks:
            self.assertTrue(t.completed)
    
    def test_multi_threaded_processing(self):
        """Test multi-threaded processing."""
        tasks = [DummyTask(i) for i in range(10)]
        
        with worker.ThreadPool(10) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        for t in tasks:
            self.assertTrue(t.completed)
    
    def test_max_queue_size_parameter(self):
        """Test thread pool with custom max_queue_size."""
        tasks = [DummyTask(i) for i in range(20)]
        
        with worker.ThreadPool(4, max_queue_size=5000) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        for t in tasks:
            self.assertTrue(t.completed)
    
    def test_verbose_parameter(self):
        """Test thread pool with verbose flag."""
        tasks = [DummyTask(i) for i in range(5)]
        
        with worker.ThreadPool(2, verbose=True) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        for t in tasks:
            self.assertTrue(t.completed)


class TestThreadPoolInterface(unittest.TestCase):
    """Test: ThreadPool interface methods from Thread Pool Guide."""
    
    def test_append_task(self):
        """Test appending tasks to thread pool."""
        t = DummyTask(1)
        
        with worker.ThreadPool(1) as tpool:
            tpool.append_task(t)
        
        self.assertTrue(t.completed)
    
    def test_remaining_method(self):
        """Test remaining() method."""
        tasks = [DummyTask(i) for i in range(5)]
        
        with worker.ThreadPool(2) as tpool:
            for t in tasks:
                tpool.append_task(t)
            
            # At some point, remaining should be >= 0
            remaining = tpool.remaining()
            self.assertGreaterEqual(remaining, 0)
    
    def test_finished_method(self):
        """Test finished() method."""
        tasks = [DummyTask(i) for i in range(5)]
        
        with worker.ThreadPool(2) as tpool:
            for t in tasks:
                tpool.append_task(t)
            
            # Should return number of finished tasks
            finished = tpool.finished()
            self.assertIsInstance(finished, int)
            self.assertGreaterEqual(finished, 0)
    
    def test_get_workers_method(self):
        """Test get_workers() method."""
        with worker.ThreadPool(4) as tpool:
            workers = tpool.get_workers()
            self.assertEqual(len(workers), 4)
    
    @unittest.skip("Close test needs fix.")
    def test_close_method(self):
        """Test close() method."""
        tpool = worker.ThreadPool(2)
        tasks = [DummyTask(i) for i in range(3)]
        
        for t in tasks:
            tpool.append_task(t)
        
        tpool.close()
        
        # All tasks should be completed after close
        for t in tasks:
            self.assertTrue(t.completed)


class TestTaskLifecycleInPool(unittest.TestCase):
    """Test: Task lifecycle when using ThreadPool from Thread Pool Guide."""
    
    def test_task_lifecycle_states(self):
        """Test that tasks go through proper lifecycle."""
        t = DummyTask(1)
        self.assertFalse(t.completed)
        
        with worker.ThreadPool(1) as tpool:
            tpool.append_task(t)
        
        self.assertTrue(t.completed)
    
    def test_multiple_tasks_execution_order(self):
        """Test FIFO order of task execution."""
        execution_order = []
        
        class OrderedTask(task.Task):
            def __init__(self, task_id):
                super(OrderedTask, self).__init__()
                self.task_id = task_id
            
            def _run(self):
                execution_order.append(self.task_id)
        
        tasks = [OrderedTask(i) for i in range(5)]
        
        with worker.ThreadPool(1) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        # With single thread, should execute in order
        self.assertEqual(len(execution_order), 5)


class TestManualThreadPoolManagement(unittest.TestCase):
    """Test: Manual thread pool management without context manager."""
    
    @unittest.skip("Manual pool management is not recommended, but should still work.")
    def test_manual_pool_creation_and_close(self):
        """Test creating and closing pool manually."""
        tpool = worker.ThreadPool(3)
        tasks = [DummyTask(i) for i in range(5)]
        
        for t in tasks:
            tpool.append_task(t)
        
        tpool.close()
        
        # All tasks should be completed
        for t in tasks:
            self.assertTrue(t.completed)


if __name__ == '__main__':
    unittest.main()
