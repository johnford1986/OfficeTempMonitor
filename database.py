import os
import psycopg
from psycopg.rows import dict_row

def get_connection():
    database_url = os.getenv("DATABASE_URL")
    return psycopg.connect(database_url, row_factory=dict_row)


def initialize_database():
    """Create the database table if it doesn't exist."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id SERIAL PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            temperature REAL,
            humidity INTEGER,
            battery TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_reading(temperature, humidity, battery):
    """Save a sensor reading."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO readings
        (temperature, humidity, battery)
        VALUES (%s, %s, %s)
    """, (temperature, humidity, battery))

    conn.commit()
    conn.close()


def get_latest_reading():
    """Return the newest reading."""

    conn = get_connection()
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
    """Return recent readings."""

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            timestamp,
            temperature,
            humidity
        FROM readings
        ORDER BY timestamp DESC
        LIMIT %s
    """, (limit,))

    rows = cursor.fetchall()

    conn.close()

    return list(reversed(rows))