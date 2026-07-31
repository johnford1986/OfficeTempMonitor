from flask import Flask, render_template, jsonify
from database import get_latest_reading, get_history

app = Flask(__name__)


@app.route("/")
def home():

    reading = get_latest_reading()

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

    return jsonify({
        "temperature": reading["temperature"],
        "humidity": reading["humidity"],
        "battery": reading["battery"],
        "timestamp": reading["timestamp"]
    })


@app.route("/api/history")
def history():

    readings = get_history()

    return jsonify([
        {
            "timestamp": row["timestamp"],
            "temperature": row["temperature"],
            "humidity": row["humidity"]
        }
        for row in readings
    ])

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )

    