'''
This module :
1. defines wrapper over Python's threading.Thread class.
2. defines ThreadTaskLoop that runs a task in loop.
'''

import threading

from pali.common import PYTHON_2, PYTHON_3
import pali.logger as logger

log = logger.getLogger(__name__)


class Thread(threading.Thread):
    """
    Wrapper over Python's Thread class with daemon property set to
    True by default.

    NOTE: Python allows you to override only __init__ and run method
    for this class.
    """

    def __init__(self, daemon=True, *args, **kwargs):
        # 'daemon' attribute on Thread object is accepted in constructor
        # argument from Python 3 onwards only. In Python 2, it was not
        # accepted as argument but was rather set as attribute on object.
        if PYTHON_3:
            kwargs['daemon'] = daemon

        super(Thread, self).__init__(*args, **kwargs)

        if PYTHON_2:
            self.daemon = daemon


class ThreadTaskLoop(object):
    THREAD_JOIN_TIMEOUT = 3

    def __init__(self, init_switch=True, daemon=True, *args, **kwargs):
        """
        ThreadTask runs a task (defined by _task method) in a loop on a
        separate thread.

        Parameters
        ------------
        init_switch
        """
        self.daemon = daemon
        self._task_switch = threading.Event()
        self._task_thread = None
        if init_switch:
            self.switch_on()

    def _task(self):
        raise NotImplementedError("_task is not implemented.")

    def switch_on(self):
        """
        Turns on task switch.
        """
        self._task_switch.set()
    
    def switch_off(self):
        """
        Turns off task switch.
        """
        self._task_switch.clear()

    def is_switch_on(self):
        """
        Returns True if task switch is ON , False otherwise.
        """
        return self._task_switch.is_set()

    def task(self):
        """
        Runs task in a loop.
        """
        while self.is_switch_on():
            self._task()

    def start(self):
        """
        Start task on a separate thread.
        """
        if self._task_thread:
            log.error("Task thread already started.")
            return

        try:
            self._task_thread = Thread(target=self.task, daemon=self.daemon)
            self._task_thread.start()
        except Exception as err:
            log.error("Error in starting task : %r", err)

    def stop(self):
        """
        Stops the thread running the task and deletes object.
        """
        if not self._task_thread:
            log.error("Task is not running for %s ", self.__name__)
            return

        try:
            self.switch_off()
            self._task_thread.join(timeout=self.THREAD_JOIN_TIMEOUT)
        except Exception as err:
            log.error("Error in stopping task : %r", err)
        finally:
            del self._task_thread
            self._task_thread = None
