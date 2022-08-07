'''
Config module allows to use Python's in-built configparser
for consuming standard configurations for projects. 

Configurations are defined in an .ini file based format.
'''

import configparser
import os
import threading

from pali.constants import CFG_FILE_PATH

CFG_MGR = None
CFG_MGR_LOCK = threading.Lock()

class ConfigManager(configparser.ConfigParser):

    def __init__(self, config_file_path, creat_config=False):
        self.config_file_path = config_file_path or CFG_FILE_PATH
        assert os.path.exists(self.config_file_path)

    def get_param(self, param, default_value):
        pass

    def set_param(self, param, value):
        pass

    def set_param_type(self, param, param_type):
        pass


def get_config_manager():
    """
    Returns Singleton instance of Configuration Manager. 

    Ensures that there are no other instance of configurations
    in the system.
    """
    global CFG_MGR
    if CFG_MGR is None:
        with CFG_MGR_LOCK:
            CFG_MGR = CFG_MGR or ConfigManager()
    return CFG_MGR


def get_param(param , default_value=None):
    """
    Returns provided or stored value for the param or None if it is not
    set yet.
    """
    return get_config_manager().get_param(param, default_value)


def set_param(param, value=None):
    """
    Sets param and it's value for later use.
    """
    get_config_manager().set_param(param, value)
