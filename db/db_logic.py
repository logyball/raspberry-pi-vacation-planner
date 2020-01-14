import sqlite3
from datetime import datetime
from pprint import pprint

from helpers.config import get_resort_driving, get_list_of_resorts
from db.db_hardcoded_sql import *
from helpers.travel import get_driving_to_resort_data_from_api, get_flying_to_resort_data_from_api
from helpers.weather import get_weather_info_from_api

def _get_cur_date_hour():
    cur_dt = datetime.now()
    cur_dt_str = cur_dt.strftime("%Y-%m-%d")
    cur_hr = cur_dt.hour
    return cur_dt_str, cur_hr


def _check_currentness_query_params(resort: str):
    cur_dt = _get_cur_date_hour()
    return {
        'resort': resort,
        'date': cur_dt[0],
        'hour': cur_dt[1]
    }


def _build_flight_info_dict(segments: list):
    dep = []
    ret = []
    price = ''
    for seg in segments:
        price = seg[0]
        seg_d = {
            'departFrom': seg[1],
            'departAt': seg[2],
            'arriveIn': seg[3],
            'arriveAt': seg[4],
            'duration': seg[5],
            'code': seg[7]
        }
        if seg[6]:
            dep.append(seg_d)
        else:
            ret.append(seg_d)
    return {
        'depart': dep,
        'price': price,
        'return': ret
    }


class BaseDb(object):
    source: str = None
    connection: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __init__(self, source=None):
        self.source = source
        self.set_up_connection()

    def set_up_connection(self):
        self.connection = sqlite3.connect(self.source)
        self.cursor = self.connection.cursor()

    def _check_currentness_result(self, cur_time: int):
        results = self.cursor.fetchone()
        if results[0] > 0 or (5 > cur_time > 18):
            return True
        return False

    def _get_cursor(self):
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()


class BaseWeatherDb(BaseDb):
    def __init__(self, source=None):
        super(BaseWeatherDb, self).__init__(source=source)

    def _check_weather_is_current(self, resort: str):
        query_params = _check_currentness_query_params(resort)
        cur_hour = query_params.get('hour')
        self.cursor.execute(check_weather_resort_current, query_params)
        return self._check_currentness_result(cur_time=cur_hour)


class WeatherDbReader(BaseWeatherDb):
    def __init__(self, source: str = None):
        super(WeatherDbReader, self).__init__(source=source)

    def get_weather_info(self, resort: str):
        cur_dt = _get_cur_date_hour()
        if self._check_weather_is_current(resort=resort):
            return self._get_weather_from_db(resort, cur_dt)
        print('getting weather from slow ass api')
        return get_weather_info_from_api(resort)

    def _get_weather_from_db(self, resort: str, cur_dt: tuple):
        query_params = self._get_info_query_params(resort, cur_dt)
        self.cursor.execute(read_weather_info, query_params)
        forecast_segments = self.cursor.fetchall()
        return self._build_weather_dict(forecast_segments)

    def _build_weather_dict(self, forecast_segments: list):
        today = {
            'temp': forecast_segments[0][0],
            'icon': forecast_segments[0][1],
            'details': forecast_segments[0][2]
        }
        forecasts = []
        for segment in forecast_segments:
            forecasts.append({
                'date': segment[3],
                'day': segment[4],
                'temp': segment[5],
                'forecast': segment[6],
                'icon': segment[7]
            })
        return {
            'today': today,
            'forecast': forecasts
        }

    def _get_info_query_params(self, resort: str, cur_dt: tuple):
        self._get_cursor()
        return {
            'resort': resort,
            'date': cur_dt[0],
            'hour': cur_dt[1]
        }


class BaseTravelDb(BaseDb):

    def __init__(self, source=None):
        super(BaseTravelDb, self).__init__(source=source)

    def _check_driving_is_current(self, resort: str):
        query_params = _check_currentness_query_params(resort)
        cur_hour = query_params.get('hour')
        self.cursor.execute(check_driving_resort_current, query_params)
        return self._check_currentness_result(cur_time=cur_hour)

    def _check_flying_is_current(self, resort: str):
        query_params = _check_currentness_query_params(resort)
        cur_hour = query_params.get('hour')
        self.cursor.execute(check_flying_resort_current, query_params)
        return self._check_currentness_result(cur_time=cur_hour)


class TravelDbReader(BaseTravelDb):
    def __init__(self, source=None):
        super(TravelDbReader, self).__init__(source)

    def get_travel_info(self, resort: str):
        cur_dt = _get_cur_date_hour()
        if get_resort_driving(resort):
            return {
                'mode': 'driving',
                'info': self._get_cur_driving_info(resort, cur_dt)
            }
        return {
            'mode': 'flying',
            'info': self._get_cur_flying_info(resort, cur_dt)
        }

    def _get_cur_driving_info(self, resort: str, cur_dt: tuple):
        """{'resort': resort, 'date': date, 'hour': hour}"""
        if self._check_driving_is_current(resort):
            query_params = self._get_info_query_params(resort, cur_dt)
            self.cursor.execute(read_travel_info_driving, query_params)
            result = self.cursor.fetchone()
            return {
                'distance': result[0],
                'time': result[1]
            }
        print('driving info: not current, fetching from slow ass api')
        return get_driving_to_resort_data_from_api(resort)

    def _get_cur_flying_info(self, resort: str, cur_dt: tuple):
        """{'resort': resort, 'date': date, 'hour': hour}"""
        if self._check_flying_is_current(resort):
            query_params = self._get_info_query_params(resort, cur_dt)
            if self._check_flying_err(query_params):
                return {
                    'depart': "could not find flight info for departure",
                    'return': "could not find flight info for return",
                    'price': "could not find flight price"
                }
            self.cursor.execute(read_travel_info_flying, query_params)
            segment_list = self.cursor.fetchall()
            return _build_flight_info_dict(segment_list)
        print('flying info: not current, fetching from slow ass api')
        return get_flying_to_resort_data_from_api(resort)

    def _get_info_query_params(self, resort: str, cur_dt: tuple):
        self._get_cursor()
        return {
            'resort': resort,
            'date': cur_dt[0],
            'hour': cur_dt[1]
        }

    def _check_flying_err(self, query_params):
        self.cursor.execute(check_flying_for_error, query_params)
        errors = self.cursor.fetchone()
        if errors[0]:
            return True
        return False


class WeatherDbBackgroundProcess(BaseWeatherDb):
    resort_list: list = None

    def __init__(self, source: str = None):
        super(WeatherDbBackgroundProcess, self).__init__(source)
        self.init_db()
        self.resort_list = get_list_of_resorts()

    def init_db(self):
        self.cursor.execute(enable_foreign_keys)
        self.connection.commit()
        self.make_tables()

    def make_tables(self):
        self.cursor.execute(create_main_weather_table)
        self.cursor.execute(create_weather_forecast_table)
        self.connection.commit()

    def update_resorts_check(self):
        for resort in self.resort_list:
            if not self._check_weather_is_current(resort):
                print('weather not current')
                weather_info = get_weather_info_from_api(resort)
                self.add_weather_info(resort, weather_info)

    def add_weather_info(self, resort: str, weather_info: dict):
        cur_dt = _get_cur_date_hour()
        insert_tup = (
            resort,
            cur_dt[0],
            cur_dt[1],
            weather_info.get('today', {}).get('temp', 'unknown temp'),
            weather_info.get('today', {}).get('icon', ''),
            weather_info.get('today', {}).get('details', 'unknown forecast')
        )
        self._get_cursor()
        self.cursor.execute(write_main_weather_info, insert_tup)
        self.connection.commit()
        weather_id = self._get_last_inserted_id()
        self._add_forecast_info(weather_entry_id=weather_id, forecast_info=weather_info)

    def _add_forecast_info(self, weather_entry_id: int, forecast_info: dict):
        for forecast in forecast_info.get('forecast', []):
            insert_tup = (
                forecast.get('date', 'unknown date'),
                forecast.get('day', 'unknown day of week'),
                forecast.get('temp', 'unknown temp'),
                forecast.get('forecast', 'unknown forecast'),
                forecast.get('icon', ''),
                weather_entry_id
            )
            self.cursor.execute(write_weather_forecast_info, insert_tup)
        self.connection.commit()

    def _get_last_inserted_id(self):
        self.cursor.execute("SELECT last_insert_rowid();")
        last_id = self.cursor.fetchone()
        return last_id[0]


class TravelDbBackgroundProcess(BaseTravelDb):
    resort_list: list = None

    def __init__(self, source=None):
        super(TravelDbBackgroundProcess, self).__init__(source)
        self.init_db()
        self.resort_list = get_list_of_resorts()

    def init_db(self):
        self.cursor.execute(enable_foreign_keys)
        self.connection.commit()
        self.make_tables()

    def make_tables(self):
        self.cursor.execute(create_main_driving_table)
        self.cursor.execute(create_main_flying_table)
        self.cursor.execute(create_segment_info_table)
        self.cursor.execute(create_flying_segment_rel)
        self.connection.commit()

    def add_drive_info(self, drive_time_info: dict, resort: str):
        """ (resort, date, hour, drive_time, drive_distance) """
        print(f'adding driving info from api for {resort}')
        cur_dt_hour = _get_cur_date_hour()
        drive_tup = (
            resort,
            cur_dt_hour[0],
            cur_dt_hour[1],
            drive_time_info.get('time'),
            drive_time_info.get('distance')
        )
        self._get_cursor()
        self.cursor.execute(write_drive_info, drive_tup)
        self.connection.commit()

    def add_flight_info(self, flight_info: dict, resort: str):
        """ (resort, date, hour, price, err) """
        print(f'adding flying info from api for {resort}')
        cur_dt = _get_cur_date_hour()
        flight_write_data = (
            resort,
            cur_dt[0],
            cur_dt[1],
            flight_info.get('price', 'unknown price'),
            0
        )
        self._get_cursor()
        self.cursor.execute(write_flying_info, flight_write_data)
        self.connection.commit()
        flight_id = self._get_last_inserted_id()
        self._add_departure_segments(flight_info.get('depart', []), flight_id)
        self._add_return_segments(flight_info.get('return', []), flight_id)

    def update_resorts_check(self):
        for resort in self.resort_list:
            if get_resort_driving(resort) and not self._check_driving_is_current(resort):
                drive_info = get_driving_to_resort_data_from_api(resort)
                self.add_drive_info(drive_info, resort)
            if not get_resort_driving(resort) and not self._check_flying_is_current(resort):
                flying_info = get_flying_to_resort_data_from_api(resort)
                if 'could not' in flying_info.get('depart', 'could not') or 'could not' in flying_info.get('return', 'could not'):
                    self._add_error_flight(flying_info, resort)
                else:
                    self.add_flight_info(flying_info, resort)

    def _add_departure_segments(self, flight_depart_info: list, flight_id: int):
        """(from_location, from_time, to_location, to_time, duration, 1)"""
        for segment in flight_depart_info:
            flight_seg_tup = (
                segment.get('departFrom'),
                segment.get('departAt'),
                segment.get('arriveIn'),
                segment.get('arriveAt'),
                segment.get('duration'),
                1,
                segment.get('code')
            )
            self._add_flight_segment(flight_seg_tup, flight_id)

    def _add_return_segments(self, flight_return_info: list, flight_id: int):
        """(from_location, from_time, to_location, to_time, duration, 0)"""
        for segment in flight_return_info:
            flight_seg_tup = (
                segment.get('departFrom'),
                segment.get('departAt'),
                segment.get('arriveIn'),
                segment.get('arriveAt'),
                segment.get('duration'),
                0,
                segment.get('code')
            )
            self._add_flight_segment(flight_seg_tup, flight_id)

    def _add_flight_segment(self, flight_seg_tup: tuple, flight_id: int):
        self.cursor.execute(write_flight_segment, flight_seg_tup)
        self.connection.commit()
        seg_id = self._get_last_inserted_id()
        self.cursor.execute(write_flight_rel_info, (flight_id, seg_id))
        self.connection.commit()

    def _add_error_flight(self, flying_info: dict, resort: str):
        """ (resort, date, hour, price, err) """
        cur_dt = _get_cur_date_hour()
        flight_write_data = (
            resort,
            cur_dt[0],
            cur_dt[1],
            flying_info.get('price', 'unknown price'),
            1
        )
        self._get_cursor()
        self.cursor.execute(write_flying_info, flight_write_data)
        self.connection.commit()

    def _get_last_inserted_id(self):
        self.cursor.execute("SELECT last_insert_rowid();")
        last_id = self.cursor.fetchone()
        return last_id[0]
