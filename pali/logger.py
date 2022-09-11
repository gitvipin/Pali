#!/usr/bin/env python
"""
Logger module provides common utilities useful for
setting up logging for Python projects.
"""

import logging
import os

import pali.constants as constants

LOG_LEVEL_NAMES = ['CRITICAL', 'DEBUG', 'ERROR', 'FATAL',
                   'WARN', 'WARNING', 'INFO']
LOG_SETUP_DONE = False


def create_log_dir(log_dir):
    """
    Creates log directory. If not successful raises
    exception after printing message on stdout.
    """
    try:
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
    except Exception as err:
        print("Failed to create log directory, %s :  %s" %
              (log_dir, str(err)))
        raise err


def set_module_log_level(module_name, log_level):
    """
    Sets the log level for a module. It is particulary
    helpful when third party module's debugging level
    needs to be changed.
    """
    assert log_level in LOG_LEVEL_NAMES, (
        "Invalid log level, %s, requestd for module %s" %
        (log_level, module_name))

    mod_logger = logging.getLogger(module_name)
    mod_logger.setLevel(getattr(logging, log_level))


def setup_logging(log_dir=None, log_file=None, log_level=logging.INFO):
    """
    Sets up logging for the project. Repeated calls are ignored after
    the first call.
    """
    global LOG_SETUP_DONE
    if LOG_SETUP_DONE:
        return  # makes repeated calls idempotent

    log_dir = log_dir or constants.LOG_DIR
    log_file = log_file or constants.LOG_FILE
    log_level = log_level or getattr(logging, constants.LOG_LEVEL)

    create_log_dir(log_dir)  # Create log directory

    log_file_name = os.path.join(log_dir, log_file)

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    file_handler = logging.FileHandler(log_file_name, mode='w')
    file_handler.setFormatter(logging.Formatter(constants.LOG_FORMAT))
    root_logger.addHandler(file_handler)
    LOG_SETUP_DONE = True


def getLogger(module_name):
    """
    Wrapper around logging.getLogger. It helps in making calls route
    through this method so that any common changes can be done here.
    """
    return logging.getLogger(module_name)
