from dotenv import load_dotenv
from tuya_connector import TuyaOpenAPI
import os

# Load environment variables
load_dotenv()

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET")
ENDPOINT = os.getenv("TUYA_ENDPOINT")
DEVICE_ID = os.getenv("TUYA_DEVICE_ID")


def get_sensor_data():
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