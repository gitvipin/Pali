#!/usr/bin/env python
'''
Scale Tests for WorkerPool.

Various scales tested are:
    - Large number of Tasks (~30K) added and served.
    - Can Queue hold upto 30K tasks at a time (if enough memory)
    - Large number of worker threads
    - Tasks with large runtimes.
    - Can we run 1 Million tasks through a worker pool, assuming
      only 10K Tasks are there at a time in queue.
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

class TestWorkerPoolScale(unittest.TestCase):

    def test_large_pending_tasks(self):
        """
        Scale test for pushing 3000 tasks on worker pool.
        """
        PENDING_TASK_COUNT = 3000
        tasks = [MyTask(i) for i in range(PENDING_TASK_COUNT)]

        # Push tasks on pool
        thr_count = 20
        tpool = worker.ThreadPool(thr_count)

        # Push tasks on pool but don't start pool yet so as we can
        # test the number of pending tasks. This testcase also highlights
        # the importance of having both the abilities for WorkerPool:
        # a) As context manager as well as b) respective API based invocations.
        for t in tasks:
            tpool.append_task(t)

        # All the tasks must remain in pending queue until pool is
        # started.
        assert(tpool.remaining() == PENDING_TASK_COUNT)

        # Validate that no task is done until it is started..
        self.assertFalse(any(t.done for t in tasks))

        # Test pending tasks status once again.
        assert(tpool.remaining() == PENDING_TASK_COUNT)

        tpool.start()
        tpool.close()

        # Validate that all tasks passed.
        self.assertTrue(all(t.done for t in tasks))

    def test_wp_scale_large_running(self):
        """
        Scale test for pushing 3000 tasks on worker pool.
        """
        PENDING_TASK_COUNT = 3000
        tasks = [MyTask(i) for i in range(PENDING_TASK_COUNT)]

        # Push tasks on pool
        thr_count = 20
        tpool = worker.ThreadPool(thr_count)

        # Push tasks on pool but don't start pool yet so as we can
        # test the number of pending tasks. This testcase also highlights
        # the importance of having both the abilities for WorkerPool:
        # a) As context manager as well as b) respective API based invocations.
        for t in tasks:
            tpool.append_task(t)

        # All the tasks must remain in pending queue until pool is
        # started.
        assert(tpool.remaining() == PENDING_TASK_COUNT)

        # Validate that no task is done until it is started..
        self.assertFalse(any(t.done for t in tasks))

        # Test pending tasks status once again.
        assert(tpool.remaining() == PENDING_TASK_COUNT)

        tpool.start()

        # Once we start, pending tasks will keep getting cleaned up soon.
        # Then we append tasks again on the queue to check that WPool is
        # working fine. Since Task.run doesn't check if task is already
        # run it doesn't error.
        #
        # Add tasks 3 times
        cnt = 3
        while cnt > 0:
            cnt -= 1
            for t in tasks:
                tpool.append_task(t)

        tpool.close()

        # Validate that all tasks passed.
        self.assertTrue(all(t.done for t in tasks))


