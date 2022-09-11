#!/usr/bin/env python
'''
This module holds package level constants for Pali.
'''


# Config module constants
CONFIG_FILE_PATH = '/etc/pali/pali.cfg'
CONFIG_DEFAULT_SECTION = 'DEFAULT'
CONFIG_COMMON_SECTION = 'COMMON'
CONFIG_USE_PARAMS = True

# Logger constants
LOG_DIR = './'
LOG_FILE = 'pali.log'
LOG_FORMAT = (
    '%(asctime)s::%(levelname)s::%(threadName)s::'
    '%(module)s[%(lineno)04s]::%(message)s')
LOG_LEVEL = 'INFO'
