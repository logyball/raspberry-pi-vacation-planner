from yaml import load, FullLoader
from functools import lru_cache

CONFIG_FILE_PATH = 'config.yaml'


def get_maps_key():
    return _get_config().get("keys", {}).get("google_maps")


def get_amadeus_keys():
    key = _get_config().get("keys", {}).get("amadeus_key")
    secret = _get_config().get("keys", {}).get("amadeus_secret")
    return key, secret


def get_weather_url():
    return _get_config().get('base_weather_url', '')


def get_origin_coordinates():
    origin = _get_config().get('origin', {})
    return origin.get('latitude', ''), origin.get('longitude', '')


def get_resort_driving(resort_name):
    resort = _get_individual_resort(resort_name)
    return bool(resort.get('driving', False))


def get_resort_airport_prefs(resort_name):
    resort = _get_individual_resort(resort_name)
    return resort.get('airport'), bool(resort.get('nonstop', ''))


def get_resort_coordinates(resort_name):
    """ returns (latitude, longitude) of the named resort"""
    resort = _get_individual_resort(resort_name)
    return resort.get('latitude'), resort.get('longitude')


def get_hotel_min():
    return _get_config().get('preferences', {}).get('hotel_star_min', 3)


def get_hotels_pref():
    return _get_config().get('preferences', {}).get('hotels', '')


def get_airlines_pref():
    prefs = _get_config().get('preferences', {})
    return prefs.get('airlines', '')


def get_origin_zipcode():
    return _get_config().get('origin', {}).get('zip', '10001')


def get_origin_airport():
    return _get_config().get('origin', {}).get('airport', 'NYC')


def get_width():
    return _get_config().get('screen_size', {}).get('width', 480)


def get_height():
    return _get_config().get('screen_size', {}).get('height', 800)


def _get_individual_resort(resort_name):
    resorts = _get_resorts()
    return resorts.get(resort_name, {})


@lru_cache(maxsize=4)
def _get_resorts():
    return _get_config().get('resorts', {})


@lru_cache(maxsize=4)
def _get_config():
    with open(CONFIG_FILE_PATH) as c_file:
        config_dict = load(c_file.read(), Loader=FullLoader)
    return config_dict
