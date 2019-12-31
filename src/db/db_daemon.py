from src.db.database_logic_objects import TravelDbBackgroundProcess, WeatherDbBackgroundProcess
from time import sleep


def db_travel_daemon(db_path):
    print('starting travel db daemon')
    database = TravelDbBackgroundProcess(db_path)
    while True:
        database.update_resorts_check()
        sleep(2)


def db_weather_daemon(db_path):
    print('starting weather db daemon')
    database = WeatherDbBackgroundProcess(db_path)
    while True:
        database.update_resorts_check()
        sleep(2)
