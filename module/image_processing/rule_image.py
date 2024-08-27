from functools import cached_property
from pathlib import Path
import cv2
import numpy as np

from module.base.logger import logger

class RuleImage:
    def __init__(self, roi: tuple, area: tuple, file: str) -> None:
        """
        初始化
        :param roi: roi
        :param area: 用于匹配的区域
        :param threshold: 阈值  0.8
        :param file: 相对路径, 带后缀
        """
        self._match_init = False  # 这个是给后面的 等待图片稳定
        self._image = None  # 这个是匹配的目标

        self.roi: list = list(roi)
        self.area = area
        self.file = file

    @cached_property
    def name(self) -> str:
        """

        :return:
        """
        return Path(self.file).stem.upper()

    def crop(self, screenshot: np.array) -> np.array:
        """
        截取图片
        """
        x, y, w, h = self.area
        return screenshot[y: y + h, x: x + w]

    def coord(self) -> tuple:
        """
        获取坐标, 从roi随机获取坐标
        :return:
        """
        x, y, w, h = self.roi
        x += np.random.randint(0, w)
        y += np.random.randint(0, h)
        return x, y

    @property
    def image(self):
        """
        获取图片
        :return:
        """
        if self._image is None:
            self.load_image()
        return self._image

    def load_image(self) -> None:
        """
        加载图片
        :return:
        """
        if self._image is not None:
            return

        image = cv2.imread(self.file)
        self._image = image

    def get_target_size(self):
        """
        获取目标大小
        """
        tl_x, tl_y, br_x, br_y = self.roi
        return {'w': br_x - tl_x, 'h': br_y - tl_y}

    def match_target(self, screenshot: np.array, threshold=0.9, debug=False, cropped=False) -> bool:
        if not cropped:
            screenshot = self.crop(screenshot)
        target = self.image
        # print(f"{self.name} area: {len(area)}, {len(area[0])}")
        result = cv2.matchTemplate(screenshot, target, cv2.TM_CCORR_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        logger.info(f"[Rule Image] {self.name} match rate: {max_val}")

        if max_val > threshold:
            self.roi[0] = max_loc[0] + self.area[0]
            self.roi[1] = max_loc[1] + self.area[1]
            logger.info(f"[Rule Image] {self.name} updated roi: {self.roi}")
            if debug:
                self.draw_and_save(screenshot)
            return True
        return False

    def draw_and_save(self, screenshot):
        """For test ONLY

        Args:
            screenshot (np.array):
        """
        x, y, w, h = self.roi
        ax, ay, aw, ah = self.area
        target_rectangle_color = (101, 67, 196)
        area_rectangle_color = (56, 176, 0)
        cv2.rectangle(screenshot, (x, y), (x + w, y + h),
                      target_rectangle_color, 2)
        cv2.rectangle(screenshot, (ax, ay), (ax + aw, ay + ah),
                      area_rectangle_color, 2)

        path = f"{Path.cwd()}/{self.name}_output.png"
        logger.info(f"[Rule Image] Save output with rectangle in {path}")
        cv2.imwrite(path, screenshot)
