#!/usr/bin/env python
'''
This module provides core implementation of ThreadPool.
'''

import threading as threading

from pali.common import queue
import pali.logger as logger

log = logger.getLogger(__name__)

class WorkerThread(threading.Thread):

    def __init__(self, in_queue, out_queue, name=None, verbose=False):

        threading.Thread.__init__(self)

        self._input_queue = in_queue
        self._output_queue = out_queue
        self._verbose = verbose

        # Thread control mechanism
        self._stop_event = threading.Event()
        self._stop_event.clear()

        # Set daemon thread, since run method does
        # blocking wait on items from queue
        self.daemon = True

    def run(self):
        while not self._stop_event.is_set():
            try:
                if self._verbose:
                    t = threading.current_thread()
                    log.debug(" Thread %s : popping element", t.name)

                # This is a blocking call.
                task = self._input_queue.get()

                if self._verbose:
                    log.debug(" Thread %s : popped element", t.name)

                # We handle only task.Task based requests.
                # assert(isinstance(task, task.Task))

                self.run_task(task)

                self._input_queue.task_done()

            except Exception as err:
                log.exception(err)
                pass

        log.info("Finished execution.")


    def run_task(self, task):
        try:
            task.run()
        except Exception as err:
            log.exception("Exception in rrunning task %s , %r", task, err)
            pass

    def stop(self):
        self._stop_event.set()

    disable = stop

    def enable(self):
        self._stop_event.clear()

    def is_disabled(self):
        """
        Returns True if worker thread is disabled.
        """
        return self._stop_event.isSet()

    def close(self):
        # Stop the thread.
        self.stop()
        # TODO : What else do we want to do.


class WorkerPool(object):
    MAXSIZE = 3000
    MAX_PARALLEL_TASK = 10

    def __init__(self, max_parallel=None, max_queue_size=None):
        '''
        A worker pool that simply takes job from pending tasks and
        assigns to one of the worker threads.
        '''
        maxsize = max_queue_size if max_queue_size else WorkerPool.MAXSIZE
        self._max_parallel_tasks = max_parallel if max_parallel else self.MAX_PARALLEL_TASK

        self._pending_tasks = queue.Queue(maxsize=maxsize)
        self._finished_tasks = queue.Queue(maxsize=maxsize)

        self._handlers = []

    def append_task(self, task):
        try:
            self._pending_tasks.put(task)
        except Exception as err:
            log.exception("Exception in adding task to queue %r", err)

    def close(self):
        self._pending_tasks.join()
        for handler in self._handlers:
            handler.stop()

    def remaining(self):
        """Returns (approx.) number of pending tasks."""
        return self._pending_tasks.qsize()

    def finished(self):
        return self._finished_tasks.qsize()

    def get_workers(self):
        '''
        Returns the list of worker threads.
        '''
        return self._handlers


class ThreadPool(WorkerPool):

    def __init__(self, max_threads=None, max_queue_size=None, verbose=False):
        self._verbose = verbose
        super(ThreadPool, self).__init__(max_parallel=max_threads,
                                         max_queue_size=max_queue_size)
        self.initialize()

    def initialize(self):
        # Initialize the handlers.
        self._handlers = [ WorkerThread(in_queue=self._pending_tasks,
                                        out_queue=self._finished_tasks,
                                        verbose=self._verbose)
                                    for i in range(self._max_parallel_tasks) ]

    def start(self):
        for handler in self._handlers:
            handler.start()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, _type, value, traceback):
        self.close()
