import sqlite3

DATABASE = "office_monitor.db"


def initialize_database():

    """Create the database and table if they don't already exist."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity INTEGER,
            battery TEXT
        )
    """)

    conn.commit()
    conn.close()
    
def save_reading(temperature, humidity, battery):
    """Save a sensor reading to the database."""

    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO readings
        (temperature, humidity, battery)
        VALUES (?, ?, ?)
    """, (temperature, humidity, battery))

    conn.commit()
    conn.close()
    
def get_latest_reading():
    """Return the most recent sensor reading."""

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM readings
        ORDER BY timestamp DESC
        LIMIT 1
    """)

    row = cursor.fetchone()

    conn.close()

    return row

def get_history(limit=100):
    """Return the most recent readings."""

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            temperature,
            humidity
        FROM readings
        ORDER BY timestamp DESC
        LIMIT ?
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return list(reversed(rows))