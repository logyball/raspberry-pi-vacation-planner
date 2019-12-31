enable_foreign_keys = "PRAGMA foreign_keys = ON;"

create_main_weather_table = """
    CREATE TABLE IF NOT EXISTS weather
    (
    entry_id INTEGER PRIMARY KEY,
    resort TEXT, 
    date TEXT, 
    hour INTEGER,
    temp TEXT,
    today_icon_path TEXT,
    today_forecast TEXT
    );
    """

create_weather_forecast_table = """
    CREATE TABLE IF NOT EXISTS weather_forecast
    (
    forecast_entry_id INTEGER PRIMARY KEY,
    forecast_date TEXT,
    forecast_day_of_week TEXT,
    forecast_temp TEXT,
    future_forecast TEXT,
    forecast_icon_path TEXT,
    weather_entry_id INTEGER,
    FOREIGN KEY(weather_entry_id) REFERENCES weather(entry_id)
    );
    """


check_weather_resort_current = """
    SELECT COUNT(*)
    FROM weather
    WHERE resort = :resort
    AND date = :date
    AND hour = :hour;
"""

write_main_weather_info = """
    INSERT INTO weather
    (resort, date, hour, temp, today_icon_path, today_forecast)
    VALUES
    (?, ?, ?, ?, ?, ?);
"""

write_weather_forecast_info = """
    INSERT INTO weather_forecast
    (forecast_date, forecast_day_of_week, forecast_temp, future_forecast, forecast_icon_path, weather_entry_id)
    VALUES
    (?, ?, ?, ?, ?, ?);
"""

read_weather_info = """
    SELECT temp, today_icon_path, today_forecast, forecast_date, forecast_day_of_week, forecast_temp, future_forecast, forecast_icon_path
    FROM weather
    INNER JOIN weather_forecast wf ON weather.entry_id = wf.weather_entry_id
    WHERE date = :date
    AND hour = :hour
    AND resort = :resort
"""

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
    flight_seg_rel_id INTEGER PRIMARY KEY,
    resort TEXT, 
    date TEXT, 
    hour INTEGER,
    price TEXT,
    err INTEGER
    );
    """

create_flying_segment_rel = """
    CREATE TABLE IF NOT EXISTS flying_rel
    (
    flight_rel_id INTEGER,
    segment_rel_id INTEGER,
    FOREIGN KEY(segment_rel_id) REFERENCES segment_info(segment_id),
    FOREIGN KEY(flight_rel_id) REFERENCES flying(flight_seg_rel_id)    
    );
"""

create_segment_info_table = """
    CREATE TABLE IF NOT EXISTS segment_info
    (
    segment_id INTEGER PRIMARY KEY,
    from_location TEXT,
    from_time TEXT,
    to_location TEXT,
    to_time TEXT,
    duration TEXT,
    depart INTEGER,
    flight_code TEXT
    );
    """

write_flying_info = """
    INSERT INTO flying
    (resort, date, hour, price, err)
    VALUES
    (?, ?, ?, ?, ?);
"""

write_flight_segment = """
    INSERT INTO segment_info
    (from_location, from_time, to_location, to_time, duration, depart, flight_code)
    VALUES
    (?, ?, ?, ?, ?, ?, ?);
"""

write_flight_rel_info = """
    INSERT INTO flying_rel
    (flight_rel_id, segment_rel_id) 
    VALUES 
    (?, ?);
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

read_travel_info_driving = """
    SELECT drive_distance, drive_time
    FROM driving
    WHERE resort = :resort
    AND date = :date
    AND hour = :hour
"""

read_travel_info_flying = """
    SELECT price, from_location, from_time, to_location, to_time, duration, depart, flight_code
    FROM flying
    INNER JOIN flying_rel fr ON flying.flight_seg_rel_id = fr.flight_rel_id
    INNER JOIN segment_info si ON fr.segment_rel_id = si.segment_id
    WHERE date = :date
    AND hour = :hour
    AND resort = :resort
"""

check_flying_for_error = """
    SELECT err
    from flying
    WHERE date = :date
    AND hour = :hour
    AND resort = :resort
"""