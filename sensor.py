print("1 - sensor.py started")

import os
print("2 - os imported")

from dotenv import load_dotenv
print("3 - dotenv imported")

print("4 - About to import tuya_connector")

from tuya_connector import TuyaOpenAPI

print("5 - Tuya connector imported")

print("6 - Loading .env")
load_dotenv()

print("7 - .env loaded")

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET")
ENDPOINT = os.getenv("TUYA_ENDPOINT")
DEVICE_ID = os.getenv("TUYA_DEVICE_ID")


def get_sensor_data():
    """Retrieve the latest data from the Tuya temperature sensor."""

    print("Connecting to Tuya...")

    try:
        print("Creating Tuya API object...")
        openapi = TuyaOpenAPI(
            ENDPOINT,
            ACCESS_ID,
            ACCESS_SECRET
        )

        print("Calling Tuya connect...")
        connect_response = openapi.connect()
        print("Tuya connect completed")

        print("Requesting device status...")
        response = openapi.get(f"/v1.0/devices/{DEVICE_ID}")

        print("Tuya response:", response)

        if not response.get("success"):
            raise RuntimeError(
                f"Tuya API error: {response.get('code')} - {response.get('msg')}"
            )

        status = response["result"]["status"]

        data = {}

        for item in status:
            data[item["code"]] = item["value"]

        print("Sensor data retrieved successfully")
        return data

    except Exception as e:
        print(f"TUYA ERROR: {type(e).__name__}: {e}")
        raise