from yaml import load, FullLoader
from functools import lru_cache

CONFIG_FILE_PATH = 'config.yaml'
SECRETS_FILE_PATH = 'secrets.yaml'


def get_maps_key():
    return _get_secrets().get("keys", {}).get("google_maps")


def get_amadeus_keys():
    key = _get_secrets().get("keys", {}).get("amadeus_key")
    secret = _get_secrets().get("keys", {}).get("amadeus_secret")
    return key, secret


def get_weather_url():
    return _get_config().get('base_weather_url', '')


def get_origin_coordinates():
    origin = _get_secrets().get('origin', {})
    return origin.get('latitude', ''), origin.get('longitude', '')


def get_resort_driving(resort_name: str):
    resort = _get_individual_resort(resort_name)
    return bool(resort.get('driving', False))


def get_resort_airport_prefs(resort_name):
    resort = _get_individual_resort(resort_name)
    return resort.get('airport'), bool(resort.get('nonstop', ''))


def get_resort_coordinates(resort_name):
    """ returns (latitude, longitude) of the named resort"""
    resort = _get_individual_resort(resort_name)
    return resort.get('latitude'), resort.get('longitude')


def get_airlines_pref():
    prefs = _get_secrets().get('preferences', {})
    return prefs.get('airlines', '')


def get_origin_airport():
    return _get_secrets().get('origin', {}).get('airport', 'NYC')


def get_width():
    return _get_config().get('screen_size', {}).get('width', 480)


def get_height():
    return _get_config().get('screen_size', {}).get('height', 800)


def _get_individual_resort(resort_name):
    resorts = _get_resorts()
    return resorts.get(resort_name, {})


def get_list_of_resorts():
    return list(_get_resorts().keys())


def get_db_path():
    return _get_config().get('db_path')


def get_stream_path(resort_name: str):
    resort = _get_individual_resort(resort_name)
    return resort.get('stream')


def get_resort_proper_name(resort_name: str):
    resort = _get_individual_resort(resort_name)
    return resort.get('name')


@lru_cache(maxsize=4)
def _get_resorts():
    return _get_config().get('resorts', {})


@lru_cache(maxsize=4)
def _get_config():
    with open(CONFIG_FILE_PATH) as c_file:
        config_dict = load(c_file.read(), Loader=FullLoader)
    return config_dict


@lru_cache(maxsize=4)
def _get_secrets():
    with open(SECRETS_FILE_PATH) as c_file:
        secrets = load(c_file.read(), Loader=FullLoader)
    return secrets
