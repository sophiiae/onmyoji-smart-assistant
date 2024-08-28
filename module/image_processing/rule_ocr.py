from functools import cached_property
from pathlib import Path
import re
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
        x, y, w, h = self.roi
        x += np.random.randint(0, w)
        y += np.random.randint(0, h)
        return x, y

    def crop(self, screenshot: np.array) -> np.array:
        """
        截取图片
        """
        x, y, w, h = self.roi
        return screenshot[y: y + h, x: x + w]

    def ocr_single(self, screenshot) -> str:
        screenshot = self.crop(screenshot)
        res = text_sys.ocr_single_line(screenshot)
        logger.info(f"text detected: {res}")
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
