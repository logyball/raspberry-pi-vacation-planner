from helpers.config import get_weather_key, get_resort_coordinates
from math import floor
import requests

API_KEY = get_weather_key()


def get_weather(lat, lon):
    res = requests.get(f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=imperial")
    weather = res.json()
    return weather


def get_current_temp_resort(resort_name):
    """returns the current temp (f) of the named resort"""
    latitude, longitude = get_resort_coordinates(resort_name)
    weather = get_weather(latitude, longitude)
    return floor(weather.get('main', {}).get('temp'))
