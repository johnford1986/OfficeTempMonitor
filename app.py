from flask import Flask, render_template, jsonify
from dotenv import load_dotenv
from database import initialize_database, get_latest_reading, get_history
from zoneinfo import ZoneInfo
import os

# Load environment variables
load_dotenv()

print(os.getenv("DATABASE_URL"))

app = Flask(__name__)

initialize_database()


def format_timestamp(timestamp):
    """
    Convert UTC timestamp from the database to Central Time.
    """

    if timestamp is None:
        return ""

    # If the timestamp has no timezone info, assume UTC
    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))

    # Convert to Central Time
    timestamp = timestamp.astimezone(ZoneInfo("America/Chicago"))

    return timestamp.strftime("%A, %B %d, %Y\n%-I:%M:%S %p")


@app.route("/")
def home():

    reading = get_latest_reading()

    if reading:
        reading["timestamp"] = format_timestamp(reading["timestamp"])

    return render_template(
        "index.html",
        temperature=reading["temperature"],
        humidity=reading["humidity"],
        battery=reading["battery"],
        timestamp=reading["timestamp"]
    )


@app.route("/api/latest")
def latest():

    reading = get_latest_reading()

    if reading:
        reading["timestamp"] = format_timestamp(reading["timestamp"])

    return jsonify(reading)


@app.route("/api/history")
def history():

    readings = get_history()

    history = []

    for row in readings:

        ts = row["timestamp"]

        if ts.tzinfo is None:
            ts = ts.replace(tzinfo=ZoneInfo("UTC"))

        ts = ts.astimezone(ZoneInfo("America/Chicago"))

        history.append({
            "timestamp": ts.strftime("%Y-%m-%d %H:%M:%S"),
            "temperature": row["temperature"],
            "humidity": row["humidity"]
        })

    return jsonify(history)


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )