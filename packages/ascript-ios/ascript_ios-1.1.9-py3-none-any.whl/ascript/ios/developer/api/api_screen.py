import io
import os
import sys
import time

from flask import request, Response, jsonify

from ascript.ios import system
from ascript.ios.developer.api import dao
from ascript.ios.developer.utils import env
from ascript.ios.developer.utils.env import get_asenv
from ascript.ios.screen import gp_list
from ascript.ios.screen.gp import loadfrom_json

current_dir = os.path.dirname(os.path.realpath(sys.argv[0]))
# print(current_dir)
module_space = os.path.join(get_asenv()["home"], 'modules')
data_space = os.path.join(get_asenv()["home"], 'data')
screen_shot_dir = os.path.join(data_space, 'screenshot')
gp_home_dir = os.path.join(data_space, 'gp')

if not os.path.exists(module_space):
    os.makedirs(module_space)

if not os.path.exists(screen_shot_dir):
    os.makedirs(screen_shot_dir)

if not os.path.exists(gp_home_dir):
    os.makedirs(gp_home_dir)


def api(app):
    @app.route("/api/screen/capture", methods=['GET'])
    def api_screen_capture():
        if "device_id" in request.args:
            device_id = request.args["device_id"]
            print(device_id)
            client = env.get_client(device_id)
            print(client)
            image = client.screenshot()
            byte_arr = io.BytesIO()
            image.save(byte_arr, format='PNG')
            byte_arr = byte_arr.getvalue()
            return Response(byte_arr, mimetype='image/png')
        else:
            jsonify(dao.api_result(code=-1, msg="device_id"))

    @app.route("/api/screen/capture/list", methods=['GET'])
    def api_screen_capture_list():
        if "device_id" in request.args:
            device_id = request.args["device_id"]
            capture = request.args["capture"]

            screenshot_device_dir = os.path.join(screen_shot_dir, device_id)
            if not os.path.exists(screenshot_device_dir):
                os.makedirs(screenshot_device_dir)

            if capture == 'true':
                client = env.get_client(device_id)
                image = client.screenshot()
                timestamp = time.time()
                screenshot_current = os.path.join(screenshot_device_dir, f'{timestamp}.png')
                image.save(screenshot_current, format='PNG')

            # 获取文件夹下的所有文件和文件夹名
            file_items = os.listdir(screenshot_device_dir)

            file_items = sorted(file_items,
                                key=lambda x: os.path.getmtime(os.path.join(screenshot_device_dir, x)), reverse=True)

            data = []
            # 过滤出文件列表，排除文件夹
            for file in file_items:
                file_img = os.path.join(screenshot_device_dir, file)
                if os.path.isfile(file_img):
                    img_length = os.path.getsize(file_img)
                    img_length_format = img_length
                    img_lastModified = os.path.getmtime(file_img)
                    data.append({
                        'path': file_img,
                        'name': os.path.basename(file_img),
                        'length': img_length_format,
                        'length_format': img_length,
                        'lastModified': img_lastModified,
                        'lastModified_format': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(img_lastModified))
                    })

            return jsonify(dao.api_result(data=data))
        else:
            return jsonify(dao.api_result(code=-1, msg="device_id"))

    @app.route("/api/screen/gplist", methods=['GET'])
    def api_screen_gplist():
        return jsonify(dao.api_result(data=gp_list()))

    @app.route("/api/screen/gp", methods=['POST'])
    def api_screen_gp():

        # print(request.form)
        device_id = request.form['device_id']
        strack = request.form['strack']
        image = request.form['image']
        gp = request.form['gp']

        gp_dir = os.path.join(gp_home_dir, device_id, gp)
        data = loadfrom_json(strack, image, gp,gp_dir)

        return jsonify(dao.api_result(data=data))

    @app.route("/api/screen/gp/create", methods=['POST'])
    def api_screen_gp_create():
        print("Enter Create", request.form)
        if "device_id" in request.form:
            device_id = request.form['device_id']
            gp_dir = request.form['path']
            gp_data_file = request.form['name']
            # print("Enter Create")
            return jsonify(dao.api_result(code=1, msg="success"))
        else:
            return jsonify(dao.api_result(code=-1, msg="device_id"))
