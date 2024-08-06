from abc import ABC, abstractmethod
from typing import Any, Union

import cv2
import numpy as np
from PIL import Image

from ascript.ios import system
from ascript.ios.screen import ascv
from ascript.ios.screen.color_tools import find_colors
from ascript.ios.screen.gp import GP, GpInOut


def capture() -> Image.Image:
    if system.client:
        return system.client.screenshot()
    return None


class FindColors(GP):
    name = "多点找色"
    ui_path = "/static/gp/find_colors"

    def __init__(self, colors: str, rect: list = None, space: int = 5, ori: int = 2, diff: list = (5, 5, 5), num=-1,
                 image: Image.Image = capture()):
        self.colors = colors
        self.rect = rect
        self.space = space
        self.ori = ori
        self.diff = diff
        self.num = num
        self.image = image

    def run(self, inout: GpInOut) -> GpInOut:
        data = find_colors(self.colors, self.rect, self.space, self.ori, self.diff, self.num, inout.image)
        print("找色", data)
        return GpInOut(inout.image, inout.offset_x, inout.offset_y, data)

    def find_all(self):
        self.num = -1
        return self.run(GpInOut(self.image)).data

    def find(self):
        self.num = 1
        res = self.run(GpInOut(self.image)).data
        if len(res) > 0:
            return res[0]
        return None


class CompareColors(GP):
    name = "多点比色"
    ui_path = "/static/gp/compare_colors"

    def __init__(self, colors: str, diff: tuple = (5, 5, 5), image: Image.Image = capture()):
        self.colors = colors
        self.diff = diff
        self.image = image

    def run(self, gp_inout: GpInOut) -> GpInOut:
        colors = color_tools.ana_colors(self.colors)
        image = np.array(gp_inout.image)
        for color in colors:
            color2 = image[color.y, color.x]
            if not color_tools.compare_color(color2, color.rgb, self.diff if color.diff is None else color.diff):
                return GpInOut(gp_inout.image, data=False)

        return GpInOut(gp_inout.image, data=True)

    def compare(self):
        return self.run(GpInOut(self.image)).data


class FindImages(GP):
    name = "找图"
    ui_path = ""
    M_TEMPLATE = 1
    M_SIFT = 2

    def __init__(self, part_image: Union[str, list], rect: list = None, confidence=0.1, rgb: bool = True,
                 mode=M_TEMPLATE, num=-1,
                 image: Image.Image = capture()):
        self.part_image = part_image
        self.rect = rect
        self.image = image
        self.confidence = confidence
        self.mode = mode
        self.num = num
        self.rgb = rgb

    def run(self, gp_inout: GpInOut) -> GpInOut:
        source_img = cv2.cvtColor(np.array(gp_inout.image), cv2.COLOR_RGB2BGR)
        data = None
        if self.mode == FindImages.M_TEMPLATE:
            data = ascv.find_all_template(source_img, self.part_image, rect=self.rect, threshold=self.confidence,
                                          rgb=self.rgb,
                                          maxcnt=self.num)
            if self.num == 1 and data and len(data) > 0:
                data = data[0]
        elif self.mode == FindImages.M_SIFT:
            data = ascv.find_surf(source_img, self.part_image, off_rect=self.rect, threshold=self.confidence,
                                  rgb=self.rgb, maxcnt=self.num)
            if self.num == 1 and data and len(data) > 0:
                data = data[0]
        gp_inout.data = data
        return gp_inout

    def find(self):
        data = self.find_template()
        if data is None or len(data) < 1:
            data = self.find_sift()

        return data

    def find_all(self):
        data = self.find_all_template()
        if data is None or len(data) < 1:
            data = self.find_all_template()

        return data

    def find_template(self):
        self.num = 1
        self.mode = FindImages.M_TEMPLATE
        return self.run(GpInOut(self.image)).data

    def find_all_template(self):
        self.num = -1
        self.mode = FindImages.M_TEMPLATE
        return self.run(GpInOut(self.image)).data

    def find_sift(self):
        self.num = 1
        self.mode = FindImages.M_SIFT
        return self.run(GpInOut(self.image)).data

    def find_all_sift(self):
        self.num = -1
        self.mode = FindImages.M_SIFT
        return self.run(GpInOut(self.image)).data


def gp_list():
    gp_s_list = []
    gp_s_list.append("ascript.ios.screen.FindColors")
    gp_s_list.append("ascript.ios.screen.CompareColors")
    class_list = []
    for gp_s in gp_s_list:
        module_name, class_name = gp_s.rsplit('.', 1)
        module = gp.load_or_reload_module(module_name)
        gp_class = getattr(module, class_name)
        dao = {"name": gp_class.name, "ui_path": gp_class.ui_path, "id": gp_s, "class_name": class_name,
               "type": "图色工具"}
        class_list.append(dao)
    print(class_list)
    return class_list
