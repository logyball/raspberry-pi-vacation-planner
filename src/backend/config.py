from yaml import load, FullLoader
from functools import lru_cache
from os import environ


class ConfigFunctions(object):
    conf_file_path: str = 'config.yaml'
    secrets_file_path: str = 'secrets.yaml'

    def __init__(self):
        pass

    def get_maps_key(self):
        return self._get_secrets().get("keys", {}).get("google_maps")

    def get_amadeus_keys(self):
        key = self._get_secrets().get("keys", {}).get("amadeus_key")
        secret = self._get_secrets().get("keys", {}).get("amadeus_secret")
        return key, secret

    def get_weather_url(self):
        return self._get_config().get('base_weather_url', '')

    def get_origin_coordinates(self):
        origin = self._get_secrets().get('origin', {})
        return origin.get('latitude', ''), origin.get('longitude', '')

    def get_resort_driving(self, resort_name: str):
        resort = self._get_individual_resort(resort_name)
        return bool(resort.get('driving', False))

    def get_resort_airport_prefs(self, resort_name: str):
        resort = self._get_individual_resort(resort_name)
        return resort.get('airport'), bool(resort.get('nonstop', ''))

    def get_resort_coordinates(self, resort_name: str):
        """ returns (latitude, longitude) of the named resort"""
        resort = self._get_individual_resort(resort_name)
        return resort.get('latitude'), resort.get('longitude')

    def get_airlines_pref(self):
        prefs = self._get_secrets().get('preferences', {})
        return prefs.get('airlines', '')

    def get_origin_airport(self):
        return self._get_secrets().get('origin', {}).get('airport', 'NYC')

    def get_width(self):
        return self._get_config().get('screen_size', {}).get('width', 480)

    def get_height(self):
        return self._get_config().get('screen_size', {}).get('height', 800)

    def _get_individual_resort(self, resort_name: str):
        resorts = self._get_resorts()
        return resorts.get(resort_name, {})

    def get_list_of_resorts(self):
        return list(self._get_resorts().keys())

    def get_db_path(self):
        return self._get_config().get('db_path')

    def get_stream_path(self, resort_name: str):
        resort = self._get_individual_resort(resort_name)
        return resort.get('stream')

    def get_resort_proper_name(self, resort_name: str):
        resort = self._get_individual_resort(resort_name)
        return resort.get('name')

    @lru_cache(maxsize=4)
    def _get_resorts(self):
        return self._get_config().get('resorts', {})

    @lru_cache(maxsize=4)
    def _get_config(self):
        with open(self.conf_file_path) as c_file:
            config_dict = load(c_file.read(), Loader=FullLoader)
        return config_dict

    @lru_cache(maxsize=4)
    def _get_secrets(self):
        with open(self.secrets_file_path) as c_file:
            secrets = load(c_file.read(), Loader=FullLoader)
        return secrets

