#!/usr/bin/env python
'''
This module represents the Basic Task in Pavo system.
'''

class Task(object):
    (NEW, READY, RUNNING, WAITING, FINISHED) = range(5)

    def __init__(self):
        self._state = self.NEW

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
        # TODO : make it non overridable
        try:
            self._run()
        except Exception as err:
            # TODO: Do Task Failure to run exception handling
            pass

    def _run(self):
        pass



if __name__ == '__main__':
    t = Task()
    t.run()
