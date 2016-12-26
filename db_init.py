import sqlite3

conn = sqlite3.connect(r"db_project.db")


def init():
    conn.execute('''CREATE TABLE IF NOT EXISTS traffic_lights
                    (id               INTEGER PRIMARY KEY AUTOINCREMENT,
                    longitude            REAL NOT NULL DEFAULT 0,
                    latitude             REAL NOT NULL DEFAULT 0,
                    direction             INT NOT NULL DEFAULT 0,
                    intersection_mac CHAR(17) NOT NULL,
                    FOREIGN KEY (intersection_mac) REFERENCES intersections (mac));''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_traffic_lights_on_intersection_mac
                    ON traffic_lights (intersection_mac);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS intersections
                    (mac CHAR(17) PRIMARY KEY,
                    ip CHAR(15));''')

    conn.execute('''CREATE TABLE IF NOT EXISTS streets
                    (id             INTEGER PRIMARY KEY AUTOINCREMENT,
                    start_longitude    REAL NOT NULL DEFAULT 0,
                    end_longitude      REAL NOT NULL DEFAULT 0,
                    start_latitude     REAL NOT NULL DEFAULT 0,
                    end_latitude       REAL NOT NULL DEFAULT 0);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS drivers
                    (national_id        CHAR(14) NOT NULL PRIMARY KEY,
                    first_name         CHAR(255) NOT NULL DEFAULT '',
                    last_name          CHAR(255) NOT NULL DEFAULT '',
                    username           CHAR(255) NOT NULL DEFAULT '',
                    encrypted_password CHAR(255) NOT NULL DEFAULT '');''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_drivers_on_national_id
                    ON drivers (national_id)''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_drivers_on_username
                    ON drivers (username);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS emergency_vehicles
                    (id       INTEGER PRIMARY KEY AUTOINCREMENT,
                    priority      INT NOT NULL DEFAULT 0);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS intersections_streets
                    (intersection_mac CHAR(17) NOT NULL,
                    street_id        INT NOT NULL,
                    PRIMARY KEY (intersection_mac, street_id),
                    FOREIGN KEY (street_id)        REFERENCES streets (id),
                    FOREIGN KEY (intersection_mac) REFERENCES intersections (mac));''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_intersections_streets_on_intersection_mac
                    ON intersections_streets (intersection_mac);''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_intersections_streets_on_street_id
                    ON intersections_streets (street_id);''')

    conn.execute('''CREATE TABLE IF NOT EXISTS uses
                    (driver_national_id   CHAR(14) NOT NULL,
                    emergency_vehicle_id INT NOT NULL,
                    date                 DATETIME NOT NULL,
                    PRIMARY KEY (driver_national_id, emergency_vehicle_id),
                    FOREIGN KEY (driver_national_id)   REFERENCES drivers (national_id),
                    FOREIGN KEY (emergency_vehicle_id) REFERENCES emergency_vehicles (id));''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_uses_on_driver_national_id
                    on uses (driver_national_id);''')

    conn.execute('''CREATE INDEX IF NOT EXISTS index_uses_on_driver_national_id
                    on uses (emergency_vehicle_id);''')
