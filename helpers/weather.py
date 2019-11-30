from helpers.config import get_weather_key, get_resort_coordinates
from math import floor
from os import path
import requests

API_KEY = get_weather_key()
ICON_PATH = '.' + path.sep + 'resources' + path.sep + 'weather_icons'


def get_weather(resort_name):
    latitude, longitude = get_resort_coordinates(resort_name)
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={latitude}&lon={longitude}&appid={API_KEY}&units=imperial")
    weather = res.json()
    return weather


def get_current_temp_resort(resort_name):
    """returns the current temp (f) of the named resort"""
    weather = get_weather(resort_name)
    return floor(weather.get('main', {}).get('temp'))


def get_current_weather_icon_resort(resort_name):
    """returns the weather icon corresponding to the named resort"""
    weather = get_weather(resort_name)
    icon_filename = ICON_PATH + path.sep + weather.get('weather', [{}])[0].get('icon') + '.png'
    return icon_filename
