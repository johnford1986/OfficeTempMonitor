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
    print("8 - Creating API object")

    openapi = TuyaOpenAPI(
        ENDPOINT,
        ACCESS_ID,
        ACCESS_SECRET
    )

    print("9 - Connecting")

    openapi.connect()

    print("10 - Connected")

    response = openapi.get(f"/v1.0/devices/{DEVICE_ID}")

    print("11 - Got response")

    status = response["result"]["status"]

    data = {}

    for item in status:
        data[item["code"]] = item["value"]

    return data

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET")
ENDPOINT = os.getenv("TUYA_ENDPOINT")
DEVICE_ID = os.getenv("TUYA_DEVICE_ID")


def get_sensor_data():
    print("Connecting to Tuya...")
    """Retrieve the latest data from the Tuya temperature sensor."""

    openapi = TuyaOpenAPI(
        ENDPOINT,
        ACCESS_ID,
        ACCESS_SECRET
    )

    openapi.connect()

    response = openapi.get(f"/v1.0/devices/{DEVICE_ID}")

    status = response["result"]["status"]

    data = {}

    for item in status:
        data[item["code"]] = item["value"]

    return data