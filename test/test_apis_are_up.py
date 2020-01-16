import unittest, requests
from src.backend.config import ConfigFunctions
from os import environ, remove
import yaml
from googlemaps import Client as gmaps_Client
import amadeus
from datetime import datetime, timedelta


class TestApisAreUp(unittest.TestCase):
    config_fn: ConfigFunctions = None
    wrote_new_file: bool = False

    @classmethod
    def setUpClass(cls) -> None:
        cls.config_fn = ConfigFunctions()
        try:
            cls.config_fn._get_secrets()
        except FileNotFoundError as e:
            print('file not found')
            print(e)
            secrets_yaml = yaml.load(f"""
            keys:
              amadeus_key: {environ.get('TEST_AMADEUS_KEY')}
              amadeus_secret: {environ.get('TEST_AMADEUS_SECRET')}
              google_maps: {environ.get('TEST_GMAPS_KEY')}
            """)
            with open('secrets.yaml', 'w') as f:
                f.write(yaml.dump(secrets_yaml))
                cls.wrote_new_file = True


    @classmethod
    def tearDownClass(cls) -> None:
        if cls.wrote_new_file:
            remove('secrets.yaml')

    def test_weather_api(self):
        weather_url = self.config_fn.get_weather_url()
        latitude, longitude = '45.505', '-122.675'
        resort_gps_url = "".join([weather_url, latitude, ",", longitude])
        res = requests.get(resort_gps_url)
        self.assertEqual(res.status_code, 200)
        self.assertGreater(len(res.json()), 0)

    def test_maps_api(self):
        client = gmaps_Client(key=self.config_fn.get_maps_key())
        origin_lat, origin_lon = '45.505', '-122.675'
        resort_lat, resort_lon = '43.505', '-73.675'
        res = client.directions(
            origin=''.join([origin_lat, ',', origin_lon]),
            destination=''.join([resort_lat, ',', resort_lon]),
            units='imperial'
        )
        self.assertIsInstance(res, list)
        self.assertGreater(len(res), 0)

    def test_flight_api(self):
        two_wks = datetime.now() + timedelta(14)
        two_wks_str = two_wks.strftime("%Y-%m-%d")
        if self.wrote_new_file:
            amadeus_cli = amadeus.Client(
                client_id=self.config_fn.get_amadeus_keys()[0],
                client_secret=self.config_fn.get_amadeus_keys()[1],
            )
        else:
            print('dont test locally!')
            return
        res = amadeus_cli.shopping.flight_offers.get(
            origin='MAD',
            destination='NYC',
            departureDate=two_wks_str
        )
        self.assertIsNotNone(res)
        self.assertIsInstance(res, amadeus.Response)
        self.assertFalse(isinstance(res, amadeus.ResponseError))
