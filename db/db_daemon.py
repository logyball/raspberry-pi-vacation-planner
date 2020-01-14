from db.db_logic import TravelDbBackgroundProcess, WeatherDbBackgroundProcess
from time import sleep
from datetime import datetime


def cur_hour_is_daytime():
    cur_hour = datetime.now().hour
    return True if (5 <= cur_hour <= 13) else False


def db_travel_daemon(db_path):
    print('starting travel db daemon')
    database = TravelDbBackgroundProcess(db_path)
    while True:
        if cur_hour_is_daytime():
            print('daytime!')
            database.update_resorts_check()
        sleep(2)


def db_weather_daemon(db_path):
    print('starting weather db daemon')
    database = WeatherDbBackgroundProcess(db_path)
    while True:
        if cur_hour_is_daytime():
            print('daytime!')
            database.update_resorts_check()
        sleep(2)
