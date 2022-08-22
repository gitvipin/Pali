#!/usr/bin/env python
'''
A simple test for config module.
'''
import tempfile
import unittest

from pali import logger as logger
from pali import params as params
from pali import config as config

SAMPLE_CONFIG="""
[DEFAULT]
Compression = yes
ForwardX11 = yes
User = First.Last

[SECTION1]
Port = 50022
ForwardX11 = no
BitRate = 0.9

[SECTION2]
ServerAliveInterval = 45
CompressionLevel = 9
"""

class ConfigTest(unittest.TestCase):

    def test_config(self):
        """
        Tests Params
        """
        params.add_param('ServerAliveInterval', 40, int)
        params.add_param('Compression', False, bool)
        params.add_param('ForwardX11', True, bool)
        params.add_param('BitRate', 1.2, float)

        # Create Config file. 
        with tempfile.NamedTemporaryFile(prefix='test_config') as fp:
            fp.write(bytes(SAMPLE_CONFIG, 'utf-8'))
            fp.flush()

            _ = config.get_config_manager(fp.name)

            # For following tests, default section would be automatically
            # set to "DEFAULT"
            # Test 1 : "Compression"
            # Compression is set to be False in params but in config file
            # it has been enabled by word "yes". Config Manager would read
            # value from config and automatically convert "yes" to True
            assert config.get_param('Compression'), "Compression test failed."

            # Test 2 : "ForwardX11"
            # ForwardX11 is set to be "yes" in DEFAULT section. Though it
            # has been disabled by "no" in section. Config Manager would read
            # value from config and automatically convert "no" to False.
            assert not config.get_param('ForwardX11', section='SECTION1'), \
                "ForwardX11 test failed."

            # Test 3 : Default section values should be available in other
            # sections as well. 
            assert config.get_param('User', section='SECTION1') == "First.Last", \
                "DEFAULT::user not found in DEFAULT SECTION"
            assert config.get_param('User', section='SECTION2') == "First.Last", \
                "DEFAULT::user not found in SECTION1 SECTION"



if __name__ == '__main__':
    unittest.main()
