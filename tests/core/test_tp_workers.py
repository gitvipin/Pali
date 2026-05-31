#!/usr/bin/env python
'''
A simple test to check pause on worker threads.

To run the test (from repo root directory) :
    python -m unittest discover -p test_tp_workers.py ./tests
'''
import collections
import threading
import time
import unittest

import pali.task as task
import pali.worker as worker
import pali.logger as logger

log = logger.getLogger(__name__)

class MyTask(task.Task):

    def __init__(self, index, exec_bk, sleep=1):
        """
        A simple task.
        """
        super(MyTask, self).__init__()

        self.index = index
        self.done = False
        self._sleep = sleep
        self.exec_bk = exec_bk
        self.executed_on = None

    def _run(self):
        log.info("Starting task %d", self.index)
        self.done = True    # mark it done
        self.executed_on = threading.current_thread().name
        self.exec_bk[self.index] = self.executed_on
        time.sleep(self._sleep)
        log.info("Finished executing task %d", self.index)


class TestWorkerPoolPause(unittest.TestCase):

    def test_thread_stop(self):
        """
        Check ability to stop and pause the threads. 
        """
        task_thr_map = {}   # thread on which task executed map

        # Generate 20 tasks
        tasks = [MyTask(i,task_thr_map,i) for i in range(7)]

        # list_iter = lambda x : yield n for n in x
        def list_iter(_list):
            for elem in _list:
                yield elem
        
        tasks_iter = list_iter(tasks)

        with worker.ThreadPool(3) as tp:
            # Push first 3 tasks on thre threads. Sleep of 3 secs.
            # ensures that each thread gets one task.
            tp.append_task(next(tasks_iter))
            tp.append_task(next(tasks_iter))
            tp.append_task(next(tasks_iter))

            # stop 2 threads
            thr_act = [False, True, True]
            for worker_thread, stop in zip(tp.get_workers(), thr_act):
                if stop:
                    # perform lazy stop
                    worker_thread.stop()

            # Pausing thread through stop on individual worker thread does
            # lazy-pause which means it will eventually pause and not take
            # more than one item from the queue.

            # Push next 4 tasks on Threadpool just to flush the queue.
            tp.append_task(next(tasks_iter))
            tp.append_task(next(tasks_iter))
            tp.append_task(next(tasks_iter))
            tp.append_task(next(tasks_iter))

            # Wait for all the tasks pushed so far to finish. 
            while not all(tasks[i].done for i in range(7)):
                time.sleep(3)

            log.info(" Task Thread map (before): %r", task_thr_map)

            # Now push all the tasks again on the queue
            task_thr_map = {}
            for t in tasks:
                t.done = False  # mark the tasks undone
                tp.append_task(t) # push on queue again

            # Wait for all the tasks pushed so far to finish. 
            while not all(tasks[i].done for i in range(7)):
                time.sleep(3)

            thr_name = tp.get_workers()[0].name # get first/active thread name
            assert all(t.executed_on == thr_name for t in tasks)
