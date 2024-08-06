import requests

from ascript.ios import wdapy
import argparse


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

        return None


client = None


def parse_args_with_argparse():
    parser = argparse.ArgumentParser(description='Give a default device.')
    parser.add_argument('-d', '--device', type=str, help='A default device')
    parser.add_argument('--', dest='args', nargs=argparse.REMAINDER)
    args,unknown = parser.parse_known_args()
    return args

try:
    args = parse_args_with_argparse()
    if args.device:
        client = guess_client(args.device)
    else:
        client = guess_client()

    if not client.is_locked():
        print("设备异常")
        # client = None

except Exception as e:
    print("设备异常:",str(e))
    client = None


class R:
    work_space = None
    client = None

    @staticmethod
    def root(child_path=None):
        pass
        # if child_path:
        #     file_path = child_path.lstrip("/")
        #     file_path = os.path.join(asR.module_path, file_path)
        #     return file_path
        # return asR.module_path

    def __init__(self):
        pass


class Device:
    @staticmethod
    def display():
        return client.window_size()

