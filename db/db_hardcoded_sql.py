
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
    flight_seg_rel_id INTEGER PRIMARY KEY,
    resort TEXT, 
    date TEXT, 
    hour INTEGER,
    price TEXT
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
    depart INTEGER
    );
    """

write_flying_info = """
    INSERT INTO flying
    (resort, date, hour, price)
    VALUES
    (?, ?, ?, ?);
"""

write_flight_segment = """
    INSERT INTO segment_info
    (from_location, from_time, to_location, to_time, duration, depart)
    VALUES
    (?, ?, ?, ?, ?, ?);
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
    SELECT price, from_location, from_time, to_location, to_time, duration, depart
    FROM flying
    INNER JOIN flying_rel fr ON flying.flight_seg_rel_id = fr.flight_rel_id
    INNER JOIN segment_info si ON fr.segment_rel_id = si.segment_id
    WHERE date = :date
    AND hour = :hour
    AND resort = :resort
"""