import sqlite3
from datetime import datetime
from helpers.config import get_resort_driving, get_list_of_resorts


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

    def __del__(self):
        self.connection.close()


class TravelDbReader(BaseTravelDb):
    def __init__(self, source=None):
        super().__init__(source)

    def get_travel_info(self, resort: str):
        cur_dt = _get_cur_date_hour()
        if get_resort_driving(resort):
            return self._get_cur_driving_info(resort, cur_dt)
        return self._get_cur_flying_info(resort, cur_dt)

    def _get_cur_driving_info(self, resort: str, cur_dt: tuple):
        pass

    def _get_cur_flying_info(self, resort: str, cur_dt: tuple):
        pass


class TravelDbBackgroundProcess(BaseTravelDb):
    resort_list: list = None

    def __init__(self, source=None):
        super().__init__(source)
        self.source = source
        self.init_db()
        self.resort_list = get_list_of_resorts()

    def init_db(self):
        self.cursor.execute(enable_foreign_keys)  # todo - smarter way than if not exists
        self.connection.commit()
        self.make_tables()

    def make_tables(self):
        self.cursor.execute(create_main_driving_table)
        self.cursor.execute(create_main_flying_table)
        self.cursor.execute(create_segment_info_table)
        self.connection.commit()

    def add_drive_time(self, drive_time_info: dict, resort: str):
        """ (resort, date, hour, drive_time, drive_distance) """
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

    def add_flight_segment(self, flight_seg_info: dict, resort: str, depart: int):
        """ (from_location, from_time, to_location, to_time) """
        flight_seg_tup = (
            flight_seg_info.get('departFrom'),
            flight_seg_info.get('departAt'),
            flight_seg_info.get('arriveIn'),
            flight_seg_info.get('arriveAt')
        )
        self._get_cursor()
        self.cursor.execute(write_flight_segment, flight_seg_tup)
        self.connection.commit()
        self._add_flight_seg_to_flying_table(resort=resort, depart=depart)

    def _add_flight_seg_to_flying_table(self, resort: str, depart: int):
        """ (resort, date, hour, depart, segment_id) """
        segment_id = self._get_last_seg_id()
        cur_dt_hour = _get_cur_date_hour()
        flying_tup = (
            resort,
            cur_dt_hour[0],
            cur_dt_hour[1],
            depart,
            segment_id
        )
        self._get_cursor()
        self.cursor.execute(write_flying_info, flying_tup)
        self.connection.commit()

    def _get_last_seg_id(self):
        self.cursor.execute("SELECT last_insert_rowid();")
        last_id = self.cursor.fetchone()
        return last_id[0]

    def update_resorts_check(self):
        for resort in self.resort_list:
            if get_resort_driving(resort) and not self._check_driving_is_current(resort):
                print('need update to driving')  # todo - update driving info
            if not get_resort_driving(resort) and not self._check_flying_is_current(resort):
                print('need update to flying')  # todo -update flying info

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


enable_foreign_keys = "PRAGMA foreign_keys = ON;"

create_main_driving_table = """
    CREATE TABLE IF NOT EXISTS driving
    (
    resort TEXT, 
    date TEXT, 
    hour INTEGER,
    drive_time TEXT,
    drive_distance TEXT
    );
    """

create_main_flying_table = """
    CREATE TABLE IF NOT EXISTS flying
    (
    resort TEXT, 
    date TEXT, 
    hour INTEGER,
    depart INTEGER,
    segment_id INTEGER,
    FOREIGN KEY(segment_id) REFERENCES segment_info(segment_id)    
    );
    """

create_segment_info_table = """
    CREATE TABLE IF NOT EXISTS segment_info
    (
    segment_id INTEGER PRIMARY KEY,
    from_location TEXT,
    from_time TEXT,
    to_location TEXT,
    to_time TEXT
    );
    """

query_travel_info_driving = """
    SELECT *
    FROM driving
    WHERE resort = resort
    AND date = date
    AND hour = hour
"""

query_travel_info_flying = """
    SELECT *
    FROM flying as f
    INNER JOIN segment_info as s
    ON (
        f.segment_id = s.segment_id
    )
    WHERE resort = resort
    AND f.date = date
    AND f.hour = hour
    AND f.depart = depart
"""

write_flying_info = """
    INSERT INTO flying
    (resort, date, hour, depart, segment_id)
    VALUES
    (?, ?, ?, ?, ?);
"""

write_flight_segment = """
    INSERT INTO segment_info
    (from_location, from_time, to_location, to_time)
    VALUES
    (?, ?, ?, ?);
"""

write_drive_info = """
    INSERT INTO driving
    (resort, date, hour, drive_time, drive_distance)
    VALUES
    (?, ?, ?, ?, ?);
"""

check_driving_resort_current = """
    SELECT COUNT(*)
    FROM driving
    WHERE resort = :resort
    AND date = :date
    AND hour = :hour;
"""

check_flying_resort_current = """
    SELECT COUNT(*)
    FROM flying
    WHERE resort = :resort
    AND date = :date
    AND hour = :hour;
"""