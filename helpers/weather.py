from helpers.config import get_resort_coordinates, get_weather_url
from datetime import datetime, timezone
from requests import get
from shutil import copyfileobj
from pathlib import Path
from os.path import sep
from os import getcwd
from re import sub
import dateutil.parser
BASE_WEATHER_URL = get_weather_url()


def get_weather_info(resort_name, num_days=5):
    latitude, longitude = get_resort_coordinates(resort_name)
    resort_gps_url = "".join([BASE_WEATHER_URL, latitude, ",", longitude])
    res_dict = get(resort_gps_url).json()  # TODO - error handling
    forecast_url = res_dict.get('properties', {}).get('forecast', None)
    if forecast_url:
        forecast = get(forecast_url).json()
        return _format_weather(forecast.get('properties', {}), num_days)
    return "error"  # TODO raise exception


def _format_weather(weather_info, num_days):
    if not weather_info:
        return "error"  # TODO raise exception
    weather_details = {
        "timestamp": weather_info.get("generatedAt", datetime.utcnow().replace(tzinfo=timezone.utc, microsecond=0).isoformat()),
        'today': _get_current_weather(weather_info.get('periods', [])[0]),
        'forecast': _get_forecast(weather_info.get('periods', [])[1:], num_days)
    }
    return weather_details


def _get_current_weather(todays_weather):
    if not todays_weather:
        return "error"  # TODO raise exception
    today_details = todays_weather
    return {
        "temp": _get_temp(today_details),
        "wind": _get_wind(today_details),
        "details": today_details.get("detailedForecast"),
        "icon": _get_icon_path(today_details.get("icon"))
    }


def _get_forecast(weather_periods, num_days):
    if not weather_periods:
        return "error"  # TODO raise exception
    forecasts = []
    for forecast in weather_periods:
        if bool(forecast.get("isDaytime")):
            forecasts.append({
                "date": _get_date(forecast),
                "temp": _get_temp(forecast),
                "forecast": forecast.get("shortForecast"),
                "day": forecast.get("name"),
                "icon": _get_icon_path(forecast.get("icon"))
            })
        if len(forecasts) >= num_days:
            break
    return forecasts


def _get_temp(details):
    return ''.join([str(details.get("temperature")), details.get("temperatureUnit")])


def _get_wind(details):
    return ''.join([details.get('windSpeed'), " ", details.get('windDirection')])


def _get_date(details):
    return dateutil.parser.parse(details.get("startTime")).date().strftime("%m/%d")


def _get_icon_path(icon_url):
    icon_str = sub(r"[/\?=+\.,!@#$%^&*()]", "", icon_url.split('icons')[1])
    icon_str = icon_str + ".png"
    icon_path = ''.join([getcwd(), sep, "resources", sep, "weather_icons", sep, icon_str])
    if not Path(icon_path).is_file():
        response = get(icon_url, stream=True)
        with open(icon_path, 'wb') as icon_output:
            copyfileobj(response.raw, icon_output)
        del response
    return icon_path
