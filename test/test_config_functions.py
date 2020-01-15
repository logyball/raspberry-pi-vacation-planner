import unittest
from os import sep
from src.backend.config import ConfigFunctions


class TestConfigReturnValues(unittest.TestCase):
    config_obj: ConfigFunctions = None

    def setUp(self) -> None:
        self.config_obj = ConfigFunctions(test_environ=True)

    def test_config_field_values(self):
        self.assertEqual(self.config_obj.conf_file_path, 'test' + sep + 'conf' + sep + 'tst_config.yaml')
        self.assertEqual(self.config_obj.secrets_file_path, 'test' + sep + 'conf' + sep + 'tst_secrets.yaml')

