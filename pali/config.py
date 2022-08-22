'''
Config module allows to use Python's in-built configparser
for consuming standard configurations for projects. 

Configurations are defined in an .ini file based format.
'''

import configparser
import os
import threading

from pali import constants as constants
from pali.logger import getLogger
from pali import params as params


CFG_MGR = None
CFG_MGR_LOCK = threading.Lock()

log = getLogger(__name__)


class ConfigManager(configparser.ConfigParser):

    def __init__(self, config_file_path=None, param_vals=None):
        super(ConfigManager, self).__init__()

        self.config_file_path = config_file_path or constants.CONFIG_FILE_PATH
        assert os.path.exists(self.config_file_path), "Invalid Config file path"

        self._section = constants.CONFIG_DEFAULT_SECTION

        self.params = param_vals or params.PARAMS if constants.CONFIG_USE_PARAMS else {}

        setattr(self, "optionxform", str)   # Read in case sensitive manner

        self.read(self.config_file_path)

    def read(self, config_path=None):
        """
        Reads config file.
        Also copies common config section in all other sections.
        """
        # determing file to read config from. param has precedence as it can
        # be used to override existing params.
        cfg_file = config_path or self.config_file_path
        super(ConfigManager, self).read(cfg_file)

    def set_section(self, section):
        """
        Changes the current section.
        """
        if self.section == section:
            return
        assert section in self.sections(), "Invalid section : %s" % section
        self._section = section

    @property
    def section(self):
        """
        Returns current default section.
        """
        return self._section

    def get_type_mapping(self, val_type):
        if val_type == int:
            return 'getint'
        elif val_type == float:
            return 'getfloat'
        elif val_type == bool:
            return 'getboolean'
        elif val_type == str:
            return 'get'    # default is str

    def get_param(self, param, val=None, section=None):
        _section = section or self.section

        if param not in self.params:
            return self[_section].get(param, val)

        param_obj = self.params[param]
        mapping = self.get_type_mapping(param_obj.val_type)
        return getattr(self[_section], mapping)(param, param_obj.get_val())

    def set_param(self, param, val, section=None):
        _section = section or self.section
        self[_section][param] = val


def get_config_manager(config_file_path=None):
    """
    Returns Singleton instance of Configuration Manager. 

    Ensures that there are no other instance of configurations
    in the system.
    """
    global CFG_MGR
    if CFG_MGR is None:
        with CFG_MGR_LOCK:
            CFG_MGR = CFG_MGR or ConfigManager(config_file_path)
    return CFG_MGR


def get_param(param , default_val=None, section=None):
    """
    Returns provided or stored value for the param or None if it is not
    set yet.
    """
    return get_config_manager().get_param(param, default_val, section)


def set_param(param, val=None, section=None):
    """
    Sets param and it's value for later use.
    """
    get_config_manager().set_param(param, val, section)
