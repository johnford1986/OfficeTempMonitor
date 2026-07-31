from sensor import get_sensor_data
from database import save_reading


def log_once():
    """Read the sensor once and save the reading."""

    data = get_sensor_data()

    temperature_c = data["va_temperature"] / 10
    temperature_f = (temperature_c * 9 / 5) + 32

    humidity = data["va_humidity"]
    battery = data["battery_state"].title()

    save_reading(
        round(temperature_f, 1),
        humidity,
        battery
    )

    print(
        f"Saved {temperature_f:.1f}°F | "
        f"Humidity: {humidity}% | "
        f"Battery: {battery}"
    )


if __name__ == "__main__":
    print("Logger started...")
    log_once()
    print("Logger finished successfully.")