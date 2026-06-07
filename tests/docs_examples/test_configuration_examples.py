"""
Tests for examples from Configuration Guide.

These tests verify that the code snippets in docs/guide/configuration.md
actually work as described.
"""

import os
import tempfile
import unittest

from pali import params
from pali.config import ConfigManager


class TestConfigurationGuideExamples(unittest.TestCase):

    def setUp(self):
        params.PARAMS.clear()

    def tearDown(self):
        params.PARAMS.clear()

    def _write_config(self, content):
        fd, path = tempfile.mkstemp(prefix='pali-config-test-', suffix='.ini')
        os.close(fd)
        with open(path, 'w') as handle:
            handle.write(content)
        return path

    def test_config_manager_reads_values_from_file(self):
        config_content = '''[DEFAULT]
log_level = INFO
max_threads = 4

[DATABASE]
host = localhost
port = 5432
database = myapp

[API]
timeout = 30
retries = 3
'''
        config_path = self._write_config(config_content)
        try:
            cfg = ConfigManager(config_file_path=config_path)
            self.assertEqual(cfg.get('DATABASE', 'host'), 'localhost')
            self.assertEqual(cfg.get('DATABASE', 'database'), 'myapp')
            self.assertEqual(cfg.get('API', 'timeout'), '30')
            self.assertEqual(cfg.get('DEFAULT', 'max_threads'), '4')
        finally:
            os.remove(config_path)

    def test_config_manager_type_conversion(self):
        config_content = '''[SERVICE]
threshold = 0.75
enabled = true
port = 8080
'''
        config_path = self._write_config(config_content)
        try:
            cfg = ConfigManager(config_file_path=config_path)
            self.assertEqual(cfg.getfloat('SERVICE', 'threshold'), 0.75)
            self.assertEqual(cfg.getboolean('SERVICE', 'enabled'), True)
            self.assertEqual(cfg.getint('SERVICE', 'port'), 8080)
        finally:
            os.remove(config_path)

    def test_set_section_changes_active_section(self):
        config_content = '''[DEFAULT]
app = pali

[DATABASE]
host = localhost
port = 5432
'''
        config_path = self._write_config(config_content)
        try:
            cfg = ConfigManager(config_file_path=config_path)
            cfg.set_section('DATABASE')
            self.assertEqual(cfg.section, 'DATABASE')
            self.assertEqual(cfg.get('DATABASE', 'host'), 'localhost')
        finally:
            os.remove(config_path)

    def test_set_param_updates_section_value(self):
        config_content = '''[DEFAULT]
value = 1

[SECTION]
value = 2
'''
        config_path = self._write_config(config_content)
        try:
            cfg = ConfigManager(config_file_path=config_path)
            cfg.set_section('SECTION')
            cfg.set_param('new_key', 'new_val')
            self.assertEqual(cfg.get('SECTION', 'new_key'), 'new_val')
        finally:
            os.remove(config_path)

    def test_config_manager_uses_param_values(self):
        config_content = '''[DEFAULT]
value = 1
'''
        config_path = self._write_config(config_content)
        try:
            params.add_param('db_port', 9999, int)
            cfg = ConfigManager(config_file_path=config_path)
            self.assertEqual(cfg.get_param('db_port'), 9999)
        finally:
            os.remove(config_path)


if __name__ == '__main__':
    unittest.main()
