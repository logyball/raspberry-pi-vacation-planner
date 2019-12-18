import sqlite3
from datetime import datetime
from helpers.config import get_resort_driving, get_list_of_resorts
from db.db_hardcoded_sql import (
    enable_foreign_keys, create_main_driving_table, read_travel_info_driving,
    create_main_flying_table, create_flying_segment_rel, create_segment_info_table,
    write_flying_info, write_flight_segment, write_drive_info, check_driving_resort_current,
    check_flying_resort_current, write_flight_rel_info, read_travel_info_flying
)
from helpers.travel import _get_driving_to_resort_data, _get_flying_to_resort_data

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


class BaseTravelDb(object):
    source: str = None
    connection: sqlite3.Connection = None
    cursor: sqlite3.Cursor = None

    def __init__(self, source=None):
        self.source = source
        self.set_up_connection()

    def set_up_connection(self):
        self.connection = sqlite3.connect(self.source)
        self.cursor = self.connection.cursor()

    def _check_driving_is_current(self, resort: str):
        query_params = _check_currentness_query_params(resort)
        self.cursor.execute(check_driving_resort_current, query_params)
        return self._check_currentness_result()

    def _check_flying_is_current(self, resort: str):
        query_params = _check_currentness_query_params(resort)
        self.cursor.execute(check_flying_resort_current, query_params)
        return self._check_currentness_result()

    def _check_currentness_result(self):
        results = self.cursor.fetchone()
        if results[0] > 0:
            return True
        return False

    def _get_cursor(self):
        self.cursor = self.connection.cursor()

    def __del__(self):
        self.connection.close()


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


class TravelDbReader(BaseTravelDb):
    def __init__(self, source=None):
        super().__init__(source)

    def get_travel_info(self, resort: str):
        cur_dt = _get_cur_date_hour()
        if get_resort_driving(resort):
            return self._get_cur_driving_info(resort, cur_dt)
        return self._get_cur_flying_info(resort, cur_dt)

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
        return _get_driving_to_resort_data(resort)

    def _get_cur_flying_info(self, resort: str, cur_dt: tuple):
        """{'resort': resort, 'date': date, 'hour': hour}"""
        if self._check_flying_is_current(resort):
            query_params = self._get_info_query_params(resort, cur_dt)
            self.cursor.execute(read_travel_info_flying, query_params)
            segment_list = self.cursor.fetchall()
            return _build_flight_info_dict(segment_list)
        print('flying info: not current, fetching from slow ass api')
        return _get_flying_to_resort_data(resort)

    def _get_info_query_params(self, resort: str, cur_dt: tuple):
        self._get_cursor()
        return {
            'resort': resort,
            'date': cur_dt[0],
            'hour': cur_dt[1]
        }


class TravelDbBackgroundProcess(BaseTravelDb):
    resort_list: list = None

    def __init__(self, source=None):
        super().__init__(source)
        self.source = source
        self.init_db()
        self.resort_list = get_list_of_resorts()

    def init_db(self):
        self.cursor.execute(enable_foreign_keys)
        self.connection.commit()
        self.make_tables()  # todo - smarter way than if not exists

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
        """ (resort, date, hour, price) """
        print(f'adding flying info from api for {resort}')
        cur_dt = _get_cur_date_hour()
        flight_write_data = (
            resort,
            cur_dt[0],
            cur_dt[1],
            flight_info.get('price', 'unknown price')
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
                drive_info = _get_driving_to_resort_data(resort)
                self.add_drive_info(drive_info, resort)
            if not get_resort_driving(resort) and not self._check_flying_is_current(resort):
                flying_info = _get_flying_to_resort_data(resort)
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
                1
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
                0
            )
            self._add_flight_segment(flight_seg_tup, flight_id)

    def _add_flight_segment(self, flight_seg_tup: tuple, flight_id: int):
        self.cursor.execute(write_flight_segment, flight_seg_tup)
        self.connection.commit()
        seg_id = self._get_last_inserted_id()
        self.cursor.execute(write_flight_rel_info, (flight_id, seg_id))
        self.connection.commit()

    def _get_last_inserted_id(self):
        self.cursor.execute("SELECT last_insert_rowid();")
        last_id = self.cursor.fetchone()
        return last_id[0]

