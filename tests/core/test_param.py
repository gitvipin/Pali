#!/usr/bin/env python
'''
A simple test for the task.
'''
import unittest

from pali import logger as logger
from pali import params as params


class ParamsTest(unittest.TestCase):

    def check_param_value(self, param, values):
        # TEST 2 : Test if values iterate for A/B enabled.
        params.add_param(param=param, val=False,
                         val_type=bool, ab_values =values,
                         ab_enabled=True)

        # Try to get value of param for 10 times and
        # it should simply iterate over values. 
        for _ in range(10):
            assert params.get_param(param) in values, \
                "A/B values not in values provided."

    def test_params(self):
        """
        Tests Params
        """
        # TEST 1 : Check if value is added properly.
        params.add_param('key', 'value')
        assert params.get_param('key') == 'value'

        # TEST 2 : Check for bool param values.
        self.check_param_value('enabled', [True, False])

        # TEST 3 : Check for int param values.
        self.check_param_value('int_vals', list(range(2, 5)))

        # TEST 4 : Check for int param values.
        self.check_param_value('int_vals', list(range(6)))

        # TEST 5 : Check for float param values.
        self.check_param_value('float_vals', [10.3, 4.5, 6.2, 3.56])


if __name__ == '__main__':
    unittest.main()
