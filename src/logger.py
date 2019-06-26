#!/usr/bin/env python
"""
Module for setting up logging for Pali project.
"""

import logging
import time

import src.constants as constants

logging_already_set = False

def setup_logging():
    """
    Configures a logger to pali.log
    """
    global logging_already_set
    if logging_already_set:
       return
    logging_already_set = True
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s[%(lineno)d]:"
        "%(funcName)s %(message)s")
    # formatter.converter = time.gmtime  # log UTC timestamps
    handler = logging.FileHandler(constants.LOG_FILE)
    handler.setFormatter(formatter)
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)

def getLogger(module_name):
    setup_logging()
    return logging.getLogger(module_name)
