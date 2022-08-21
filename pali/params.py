#!/usr/bin/env python
'''
This module allows to provide common framework for defining Parameters.

There is a collection of these parameters which is globally accessible. To keep the implementation simple, 
addition of a paramater is not made "Thread Safe" and it is suggested / expected that
all such parameters are defined in the startup of a project in the main thread itself.

It is also advised to add parameters through the exposed interface "add_param" here.
However, these parameters should be consumed through "config" module. It is mainly
done for two reasons. 

- Config files can ovverride parameter values and hence should be used.
- Config files by itself don't define parameter data type. Through Params, type of config value
  can be determined. 
'''

import collections
from pali.logger import getLogger

log = getLogger(__name__)
PARAMS = collections.defaultdict()

class DistType:
    EVEN = 1

class Parameter(object):

    def __init__(self, name, val, val_type=str,
                ab_values = None, ab_enabled = False,
                ab_distribution=DistType.EVEN):
        self.name = name
        self.val_type = val_type
        self.val = val

        assert isinstance(val, val_type), "Invalid val type."

        # If A/B Values are enabled, param's value provided is ignored. 
        self.ab_values = list(ab_values) if ab_values else []
        self.ab_enabled = ab_enabled
        self.ab_distribution = ab_distribution

        self._ab_value_iter = self.get_ab_value()

    def get_ab_value(self):
        for value in self.ab_values:
            yield value
    
    def get_val(self):
        if not self.ab_enabled:
            return self.val
        try:
            return next(self._ab_value_iter)
        except StopIteration:
            self._ab_value_iter = self.get_ab_value()
            return next(self._ab_value_iter)


def add_param(param, val, val_type=str, ab_values = None, ab_enabled = False, ab_distribution='EVEN'):
    """
    Adds Constant in the global constants dictionary.
    """
    PARAMS[param] = Parameter(param, val, val_type, ab_values, ab_enabled, ab_distribution)
    log.debug("Added parameter : %s", param)


def get_param(param):   # DEPRECATED, use config module instead.
    """
    Returns param val.
    """
    return PARAMS[param].get_val()