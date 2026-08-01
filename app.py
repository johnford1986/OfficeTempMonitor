from flask import Flask, render_template, jsonify, request
from dotenv import load_dotenv
from database import initialize_database, get_latest_reading, get_history
from logger import log_once
from zoneinfo import ZoneInfo
import os

load_dotenv()

app = Flask(__name__)

initialize_database()


def format_timestamp(timestamp):

    if timestamp is None:
        return ""

    if timestamp.tzinfo is None:
        timestamp = timestamp.replace(tzinfo=ZoneInfo("UTC"))

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


@app.route("/update")
def update():

    token = request.args.get("token")

    if token != os.getenv("UPDATE_TOKEN"):
        return jsonify({"status": "unauthorized"}), 401

    try:

        log_once()

        reading = get_latest_reading()

        reading["timestamp"] = format_timestamp(reading["timestamp"])

        return jsonify({
            "status": "success",
            "temperature": reading["temperature"],
            "humidity": reading["humidity"],
            "battery": reading["battery"],
            "timestamp": reading["timestamp"]
        })

    except Exception as e:

        return jsonify({
            "status": "error",
            "message": str(e)
        }), 500


if __name__ == "__main__":

    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )