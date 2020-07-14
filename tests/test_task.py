#!/usr/bin/env python
'''
A simple test for the task.
'''

import pali.task as task
import unittest


class MyTask(task.Task):
    def _run(self):
        pass


class FirstTest(unittest.TestCase):

    def setUp(self):
        self._task = MyTask()

    def test_first(self):
        """
        A simple test to check Task can be extended and
        executed.
        """
        self._task.run()


if __name__ == '__main__':
    unittest.main()
