#!/usr/bin/env python
'''
This module represents the Basic Task in Pavo system.
'''
import abc

class Task(object):
    (NEW, READY, RUNNING, WAITING, FINISHED) = range(5)
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        """
        This class defines the abstract representation of Task in Pavo system.

        A Task has a well defined life cycle and is treated accordingly. All
        the Tasks in the Pavo system MUST be derived from it. This class in
        itself is non-instantiable with the help of abstract method 'run' and
        '_run'.

        A Task object should be self contained and it's run method shouldn't
        accept any arguments. Any attribute, metadata, configuration or
        properties needed for the task must be passed in the contrsuctor at the
        time of initialization.
        """
        self._state = self.NEW
        super(Task, self).__init__()

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, val):
        # TODO : do validation
        self._state = val

    @state.deleter
    def state(self):
        del self._state

    def run(self):
        """
        This method exposes the interface for running the task. This is a
        non overridable method in class so as derived class types do not
        override the default behavior of execution of tasks in the system.
        """
        try:
            self._run()
        except Exception as err:
            # TODO: Do Task Failure to run exception handling
            pass

    @abc.abstractmethod
    def _run(self):
        """
        A helper 'run' routine for running Tasks in pavo system. The core
        functionality of task will be run through this helper routine.
        """
        pass

if __name__ == '__main__':
    class MyTask(Task):
        def _run(self):
            pass

    t = MyTask()
    t.run()
