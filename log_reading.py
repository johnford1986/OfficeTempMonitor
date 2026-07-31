from sensor import get_sensor_data
from database import save_reading

print("Reading sensor...")

data = get_sensor_data()

temperature_c = data["va_temperature"] / 10
temperature_f = (temperature_c * 9 / 5) + 32

humidity = data["va_humidity"]
battery = data["battery_state"].title()

print(f"Temperature: {temperature_f:.1f}°F")
print(f"Humidity: {humidity}%")
print(f"Battery: {battery}")

save_reading(
    round(temperature_f, 1),
    humidity,
    battery
)

print("✅ Reading saved to database!")