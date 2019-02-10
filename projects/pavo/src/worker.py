#!/usr/bin/env python


from common import queue
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
            pass

    def stop(self):
        self._stop_event.set()

    def close(self):
        # Stop the thread.
        self.stop()
        # TODO : What else do we want to do.


class WorkerPool(object):
    MAXSIZE = 3000
    MAX_PARALLEL_TASK = 10

    def __init__(self, max_parallel=None):
        '''
        A worker pool that simply takes job from pending tasks and
        assigns to one of the worker threads.
        '''
        self._pending_tasks = queue.PriorityQueue(maxsize=WorkerPool.MAXSIZE)
        self._finished_tasks = queue.PriorityQueue(maxsize=WorkerPool.MAXSIZE)
        self._max_parallel_tasks = max_parallel if not None else self.MAX_PARALLEL_TASK

        self._handlers = []
        pass

    def append_task(self, task):
        try:
            self._pending_tasks.put(task)
        except Exception as err:
            # What happens when queue is full and we cann't put elements in it.
            pass

    def close(self):
        for handler in self._handlers:
            handler.stop()


class ThreadedPool(WorkerPool):

    def __init__(self):
        super(ThreadedPool, self).__init__()

        for i in range(self.MAX_PARALLEL_TASK):
            self._handlers = threading.Thread()

        self.initialize()

    def initialize(self):
        # Initialize the handlers.
        self._handlers = [ WorkerThread(in_queue=self._pending_tasks,
                                        out_queue=self._finished_tasks)
                                    for i in range(self.MAX_PARALLEL_TASK) ]


class MultiprocessingPool(WorkerPool):

    def __init__(self):
        # TODO :
        super(MultiprocessingPool, self).__init__()
        pass


