#!/usr/bin/env python
'''
Worker Pool testcases.
'''

import unittest

import src.task as task
import src.worker as worker


class MyTask(task.Task):

    def __init__(self, index=None):
        """
        A simple task.
        """
        super(MyTask, self).__init__()

        self.index = index
        self.done = False

    def _run(self):
        self.done = True    # mark it done


class TestWorkerPool(unittest.TestCase):

    def test_worker_pool(self):
        tasks = [MyTask(i) for i in range(5)]

        # Push tasks on pool
        thr_count = 2
        tpool = worker.ThreadPool(thr_count)
        tpool.start()
        for t in tasks:
            tpool.append_task(t)
        tpool.close()

        # Validate that all tasks passed.
        self.assertTrue(all(t.done for t in tasks))

    def test_context_manager(self):
        "Same as above test but test context manager"
        tasks = [MyTask(i) for i in range(5)]

        # Push tasks on pool
        thr_count = 2

        # Invoke WorkerPool as in context manager.
        # Note that .start() and .close() w.r.t. to
        # previous test have been moved to context.
        with worker.ThreadPool(thr_count) as tpool:
            _ = [tpool.append_task(t) for t in tasks]

        # Validate that all tasks passed.
        self.assertTrue(all(t.done for t in tasks))


if __name__ == '__main__':
    unittest.main()
