from dotenv import load_dotenv
from tuya_connector import TuyaOpenAPI
import os
import json

load_dotenv()

ACCESS_ID = os.getenv("TUYA_ACCESS_ID")
ACCESS_SECRET = os.getenv("TUYA_ACCESS_SECRET")
ENDPOINT = os.getenv("TUYA_ENDPOINT")
DEVICE_ID = os.getenv("TUYA_DEVICE_ID")

print("Connecting...")

openapi = TuyaOpenAPI(
    ENDPOINT,
    ACCESS_ID,
    ACCESS_SECRET
)

openapi.connect()

print("Connected!")

response = openapi.get(f"/v1.0/devices/{DEVICE_ID}")

print(json.dumps(response, indent=4))