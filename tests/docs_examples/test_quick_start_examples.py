"""
Tests for examples from Quick Start guide.

These tests verify that all code snippets in docs/getting-started/quick-start.md
actually work as described.
"""

import unittest
from pali import task, worker


class GreetingTask(task.Task):
    """Example from Quick Start: Basic greeting task."""
    
    def __init__(self, name):
        super(GreetingTask, self).__init__()
        self.name = name
        self.greeting = None
    
    def _run(self):
        # This method is called by the thread pool
        self.greeting = f"Hello, {self.name}!"


class NumberTask(task.Task):
    """Example from Quick Start: Square numbers."""
    
    def __init__(self, number):
        super(NumberTask, self).__init__()
        self.number = number
        self.square = None
    
    def _run(self):
        self.square = self.number ** 2


class TestQuickStartGreeting(unittest.TestCase):
    """Test: Basic greeting task example from Quick Start."""
    
    def test_greeting_task_basic(self):
        """Test single greeting task execution."""
        task_obj = GreetingTask("Alice")
        self.assertIsNone(task_obj.greeting)  # Not executed yet
        
        with worker.ThreadPool(1) as tpool:
            tpool.append_task(task_obj)
        
        self.assertEqual(task_obj.greeting, "Hello, Alice!")
    
    def test_multiple_greetings(self):
        """Test multiple greeting tasks from Quick Start example."""
        names = ["Alice", "Bob", "Charlie"]
        tasks = [GreetingTask(name) for name in names]
        
        with worker.ThreadPool(3) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        # Verify all tasks completed
        greetings = [t.greeting for t in tasks]
        self.assertIn("Hello, Alice!", greetings)
        self.assertIn("Hello, Bob!", greetings)
        self.assertIn("Hello, Charlie!", greetings)


class TestQuickStartNumberSquaring(unittest.TestCase):
    """Test: Number squaring example from Quick Start."""
    
    def test_square_numbers_0_to_9(self):
        """Test squaring numbers 0-9 as in Quick Start example."""
        tasks = [NumberTask(i) for i in range(10)]
        
        with worker.ThreadPool(4) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        # Verify all squares are correct
        expected_results = [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]
        actual_results = [t.square for t in tasks]
        self.assertEqual(actual_results, expected_results)
    
    def test_individual_number_square(self):
        """Test squaring an individual number."""
        task_obj = NumberTask(5)
        
        with worker.ThreadPool(1) as tpool:
            tpool.append_task(task_obj)
        
        self.assertEqual(task_obj.square, 25)
    
    def test_large_number_square(self):
        """Test squaring larger numbers."""
        task_obj = NumberTask(100)
        
        with worker.ThreadPool(1) as tpool:
            tpool.append_task(task_obj)
        
        self.assertEqual(task_obj.square, 10000)


class TestContextManagerUsage(unittest.TestCase):
    """Test: Proper use of context manager from Quick Start."""
    
    def test_context_manager_cleanup(self):
        """Test that context manager properly cleans up resources."""
        tasks = [GreetingTask(f"Person{i}") for i in range(5)]
        
        # Using context manager should not raise any errors
        with worker.ThreadPool(2) as tpool:
            for t in tasks:
                tpool.append_task(t)
        
        # All tasks should be completed
        for t in tasks:
            self.assertIsNotNone(t.greeting)
            self.assertTrue(t.greeting.startswith("Hello"))


if __name__ == '__main__':
    unittest.main()
