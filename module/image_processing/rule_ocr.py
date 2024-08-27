from functools import cached_property
from pathlib import Path
import re
import cv2
import numpy as np
from ppocronnx.predict_system import TextSystem

from module.base.logger import logger

text_sys = TextSystem()

class RuleOcr:
    roi: tuple = ()
    area: tuple = ()
    name: str = "ocr"

    def __init__(self, name: str, roi: tuple, area: tuple) -> None:
        self.name = name.upper()
        self.roi = roi
        self.area = area

    @cached_property
    def name(self) -> str:
        """

        :return:
        """
        return Path(self.file).stem.upper()

    def coord(self) -> tuple:
        """
        获取坐标, 从roi随机获取坐标
        :return:
        """
        tl_x, tl_y, br_x, br_y = self.roi
        x = np.random.randint(tl_x, br_x)
        y = np.random.randint(tl_y, br_y)
        return x, y

    def crop(self, screenshot: np.array) -> np.array:
        """
        截取图片
        """
        tl_x, tl_y, br_x, br_y = self.roi
        return screenshot[tl_y: br_y, tl_x: br_x]

    def ocr_single(self, screenshot) -> str:
        screenshot = self.crop(screenshot)
        res = text_sys.ocr_single_line(screenshot)
        # print(f"text detected: {res}")
        return res[0]

    def digit_counter(self, screenshot) -> list:
        result = self.ocr_single(screenshot)
        if result == "":
            return [0, 0]

        result = re.search(r'(\d+)/(\d+)', result)
        if result:
            result = [int(s) for s in result.groups()]
            logger.info(f"ticket ocr result: {result}")
            count, total = result[0], result[1]
            if count > total:
                logger.critical(
                    f"realm raid ticket overflow!! Must be something wrong with OCR.")
            return result
        else:
            logger.warning(f'Unexpected ocr result: {result}')
            return [0, 0]

    def digit(self, image) -> int:
        """
        返回数字
        :param image:
        :return:
        """
        result = self.ocr_single(image)

        if result == "":
            return 0
        else:
            return int(result)
