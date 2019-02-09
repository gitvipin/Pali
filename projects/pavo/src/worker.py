#!/usr/bin/env python


import common.queue as queue
import threading as threading


class WorkerThread(threading.Thread):

    def __init__(self, in_queue, out_queue, name=None):
        self._stop_event = threading.Event()
        self._input_queue = in_queue
        self._output_queue = out_queue

    def start(self):
        while True and not self._stop_event.is_set():
            try:
                # This is a blocking call.
                task = self._input_queue.get()

                # We handle only task.Task based requests.
                assert(isinstance(task, task.Task))

                self.run_task(task)

                self._input_queue.task_done()

            except Exception as err:
                pass


    def run_task(self, task):
        try:
            task.run()
        except Exception as err:
            # TODO : Handle errors coming out of running the task.
            # This must be different from error to be handled out of
            # Queue handling

    def stop(self):
        self._stop_event.set()

    def close(self):
        pass


class WorkerPool(object):
    MAXSIZE = 3000
    MAX_PARALLEL_TASK = 10

    def __init__(self):
        '''
        A worker pool that simply takes job from pending tasks and
        assigns to one of the worker threads.
        '''
        self._pending_tasks = queue.PriorityQueue(maxsize=WorkerPool.MAXSIZE)
        self._finished_tasks = queue.PriorityQueue(maxsize=WorkerPool.MAXSIZE)

        self._handlers = []
        pass


class ThreadedPool(WorkerPool):

    def __init__(self):
        for i in range(self.MAX_PARALLEL_TASK):
            self._handlers = threading.Thread()
        super(ThreadedPool, self).__init__()
        pass


class MultiprocessingPool(WorkerPool):

    def __init__(self):
        super(MultiprocessingPool, self).__init__()
        pass


