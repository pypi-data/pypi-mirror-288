import sys

import requests
from ascript.ios import wdapy


def guess_client(device_id: str = None):
    if device_id:
        return wdapy.AppiumUSBClient(device_id)
    else:
        response = requests.get("http://127.0.0.1:9097/api/device")
        if response.status_code == 200:
            data = response.json()
            if data["data"] and len(data["data"]) > 0:
                for device in data["data"]:
                    if device["statue"] == 0:
                        print("猜测运行:", device)
                        return wdapy.AppiumUSBClient(device['udid'])


client = None

try:
    if len(sys.argv) > 1:
        client = guess_client(sys.argv[1])
    else:
        client = guess_client()
except Exception as e:
    print(e)


class R:
    work_space = None
    client = None

    @staticmethod
    def root(child_path=None):
        if child_path:
            file_path = child_path.lstrip("/")
            file_path = os.path.join(asR.module_path, file_path)
            return file_path
        return asR.module_path


    def __init__(self):
        pass


class Device:
    @staticmethod
    def display():
        return client.window_size()
