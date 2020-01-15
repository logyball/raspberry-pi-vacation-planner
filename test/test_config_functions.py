import unittest
from os import sep, getcwd
from src.backend.config import ConfigFunctions


class TestConfigReturnValues(unittest.TestCase):
    config_obj: ConfigFunctions = None
    cwd: str = None

    def setUp(self) -> None:
        self.config_obj = ConfigFunctions(test_environ=True)
        self.cwd = getcwd()

    def test_config_field_values(self):
        self.assertEqual(self.config_obj.conf_file_path, self.cwd + sep + 'test' + sep + 'conf' + sep + 'tst_config.yaml')
        self.assertEqual(self.config_obj.secrets_file_path, self.cwd + sep + 'test' + sep + 'conf' + sep + 'tst_secrets.yaml')

    def test_maps_key(self):
        self.assertEqual(self.config_obj.get_maps_key(), 'test_google_maps')

    def test_amadeus_keys(self):
        keys = self.config_obj.get_amadeus_keys()
        self.assertEqual(len(keys), 2)
        self.assertEqual(keys[0], 'test_amadeus_key')
        self.assertEqual(keys[1], 'test_amadeus_secret')

    def test_weather_url(self):
        self.assertEqual(self.config_obj.get_weather_url(), 'https://api.weather.gov/points/')

    def test_origin_coordinates(self):
        coordinates = self.config_obj.get_origin_coordinates()
        self.assertEqual(len(coordinates), 2)
        self.assertEqual(coordinates[0], '100.100')
        self.assertEqual(coordinates[1], '-200.200')

    def test_get_resort_driving(self):
        self.assertFalse(self.config_obj.get_resort_driving(resort_name='steamboat'))
        self.assertTrue(self.config_obj.get_resort_driving(resort_name='killington'))

    def test_resort_info_gets(self):
        res_coords = self.config_obj.get_resort_coordinates(resort_name='steamboat')
        prefs_steamboat = self.config_obj.get_resort_airport_prefs(resort_name='steamboat')
        resort_list = self.config_obj.get_list_of_resorts()
        self.assertEqual(len(prefs_steamboat), 2)
        self.assertEqual(prefs_steamboat[0], 'HDN')
        self.assertFalse(prefs_steamboat[1])
        self.assertEqual(len(res_coords), 2)
        self.assertEqual(res_coords[0], '667')
        self.assertEqual(res_coords[1], '-667')
        self.assertIn('steamboat', resort_list)
        self.assertIn('killington', resort_list)
        self.assertEqual(
            self.config_obj.get_resort_proper_name(resort_name='steamboat'),
            'Steamboat Springs'
        )

    def test_get_airline_prefs(self):
        self.assertEqual(self.config_obj.get_airlines_pref(), 'WN')
        self.assertEqual(self.config_obj.get_origin_airport(), 'NYC')

    def test_get_height_width(self):
        self.assertEqual(self.config_obj.get_width(), 1600)
        self.assertEqual(self.config_obj.get_height(), 960)

    def test_get_db(self):
        self.assertEqual(self.config_obj.get_db_path(), 'test_db.db')

    def test_get_stream_path(self):
        self.assertEqual(
            self.config_obj.get_stream_path(resort_name='killington'),
            'test_url2'
        )

    def test_hidden_config_functions(self):
        config = self.config_obj._get_config()
        secrets = self.config_obj._get_secrets()
        resorts = self.config_obj._get_resorts()
        resort = self.config_obj._get_individual_resort(resort_name='killington')
        self.assertEqual(type(config), dict)
        self.assertNotEqual(len(config), 0)
        self.assertEqual(type(secrets), dict)
        self.assertNotEqual(len(secrets), 0)
        self.assertEqual(type(resort), dict)
        self.assertNotEqual(len(resort), 0)
        self.assertEqual(type(resorts), dict)
        self.assertGreater(len(resorts), 1)