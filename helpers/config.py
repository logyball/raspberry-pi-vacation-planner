from yaml import load, FullLoader
from functools import lru_cache

CONFIG_FILE_PATH = 'config.yaml'


def get_weather_key():
    return  _get_config().get('keys', {}).get('open_weather')


def get_resort_coordinates(resort_name):
    """ returns (latitude, longitude) of the named resort"""
    resorts = get_resorts()
    resort = resorts.get(resort_name, {})
    return resort.get('latitude'), resort.get('longitude')


@lru_cache(maxsize=4)
def get_resorts():
    return _get_config().get('resorts', {})


def get_origin_zipcode():
    return _get_config().get('origin', {}).get('zip', '10001')


def get_origin_airport():
    return _get_config().get('origin', {}).get('airport', 'NYC')


def get_width():
    return _get_config().get('screen_size', {}).get('width', 480)


def get_height():
    return _get_config().get('screen_size', {}).get('height', 800)


@lru_cache(maxsize=4)
def _get_config():
    with open(CONFIG_FILE_PATH) as c_file:
        config_dict = load(c_file.read(), Loader=FullLoader)
    return config_dict
