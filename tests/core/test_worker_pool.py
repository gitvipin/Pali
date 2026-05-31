#!/usr/bin/env python
'''
Worker Pool testcases.
'''

import unittest

import pali.task as task
import pali.worker as worker


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
        """
        Same as above test but test context manager
        """
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

    def test_task_order(self):
        """
        Tests that tasks are processed in same order. Uses ThreadPool
        in single Thread mode to enusre that tasks are processed in
        the order they are pushed.

        This test case MUST pass for ThreadPool to be usable in
        building data pipelines.
        """
        class LinkedTask(task.Task):
            def __init__(self, index):
                self._id = index
                self.done = False
                self.prev = None

            def _run(self):
                # Need not check all previous nodes to be marked
                # done here. "Done" is a Transitive property here
                # and that means if aRb and bRc then aRc.
                assert(not self.prev or self.prev.done)
                self.done = True

        # Forms a linked List of Tasks and puts them on worker pool.
        # When each task is run it checks , all of its previous are
        # marked as done.
        TASK_COUNT = 10
        prev_task, tasks = None, []
        for i in range(TASK_COUNT):
            t = LinkedTask(i)
            tasks.append(t)
            t.prev, prev_task = prev_task, t

        # Push tasks on pool
        thr_count = 1

        # Invoke WorkerPool as in context manager.
        # Note that .start() and .close() w.r.t. to
        # previous test have been moved to context.
        with worker.ThreadPool(thr_count) as tpool:
            _ = [tpool.append_task(t) for t in tasks]

        # Validate that all tasks are marked done.
        # A node will be marked done only if all its
        # previous nodes in the list were marked done.
        self.assertTrue(all(t.done for t in tasks))


if __name__ == '__main__':
    unittest.main()
