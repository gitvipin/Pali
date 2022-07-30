#!/usr/bin/env python
'''
Some general purpose utilities.
'''

import platform

PYTHON_VER = platform.python_version()

PYTHON_2 = PYTHON_VER.startswith('2')
PYTHON_3 = PYTHON_VER.startswith('3')

system = platform.system()
IS_WINDOWS = system == 'Windows'
IS_LINUX = system == 'Linux'
IS_MAC = system == 'Darwin'

if PYTHON_2:
    import Queue as queue
elif PYTHON_3:
    import queue as queue


queue = queue
