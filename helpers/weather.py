from helpers.config import get_resort_coordinates
from datetime import datetime, timezone
from requests import get
BASE_WEATHER_URL = "https://api.weather.gov/points/"


def get_weather_info(resort_name, num_days=5):
    latitude, longitude = get_resort_coordinates(resort_name)
    resort_gps_url = "".join([BASE_WEATHER_URL, latitude, ",", longitude])
    res_dict = get(resort_gps_url).json()  # TODO - error handling
    forecast_url = res_dict.get('properties', {}).get('forecast', None)
    if forecast_url:
        forecast = get(forecast_url).json()
        return format_weather(forecast.get('properties', {}), num_days)
    return "error"  # TODO raise exception


def format_weather(weather_info, num_days):
    if not weather_info:
        return "error"  # TODO raise exception
    weather_details = {
        "timestamp": weather_info.get("generatedAt", datetime.utcnow().replace(tzinfo=timezone.utc, microsecond=0).isoformat()),
        'today': get_current_weather(weather_info.get('periods', [])[0]),
        'forecast': get_forecast(weather_info.get('periods', [])[1:], num_days)
    }
    return weather_details


def get_current_weather(todays_weather):
    if not todays_weather:
        return "error"  # TODO raise exception
    today_details = todays_weather
    return {
        "temp": get_temp(today_details),
        "wind": get_wind(today_details),
        "details": today_details.get("detailedForecast"),
        "icon": today_details.get("icon")
    }


def get_forecast(weather_periods, num_days):
    if not weather_periods:
        return "error"  # TODO raise exception
    forecasts = []
    for forecast in weather_periods:
        if bool(forecast.get("isDaytime")):
            forecasts.append({
                "temp": get_temp(forecast),
                "forecast": forecast.get("shortForecast"),
                "day": forecast.get("name"),
                "icon": forecast.get("icon")
            })
        if len(forecasts) >= num_days:
            break
    return forecasts


def get_temp(details):
    return ''.join([str(details.get("temperature")), details.get("temperatureUnit")])


def get_wind(details):
    return ''.join([details.get('windSpeed'), " ", details.get('windDirection')])
