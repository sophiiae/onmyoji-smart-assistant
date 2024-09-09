from functools import cached_property
from pathlib import Path
import re
import time
import cv2
import numpy as np
from ppocronnx.predict_system import TextSystem, BoxedResult

from module.base.logger import logger
from module.base.utils import float2str, merge_area

text_sys = TextSystem()

class RuleOcr:
    roi: tuple = ()
    area: tuple = ()
    name: str = "ocr"
    keyword: str = ""
    score: float = 0.8  # 阈值默认为0.5

    def __init__(self, name: str, roi: tuple, area: tuple, keyword: str) -> None:
        self.name = name.upper()
        self.roi = roi
        self.area = area
        self.keyword = keyword

    @cached_property
    def name(self) -> str:
        """

        :return:
        """
        return Path(self.file).stem.upper()

    @cached_property
    def model(self) -> TextSystem:
        return TextSystem()

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

    def ocr_full(self, screenshot, keyword: str = None) -> tuple:
        """
        检测整个图片的文本,并对结果进行过滤。返回的是匹配到的keyword的左边。如果没有匹配到返回(0, 0, 0, 0)
        :param image:
        :param keyword:
        :return:
        """
        if keyword is None:
            keyword = self.keyword

        boxed_results = self.detect_and_ocr(screenshot)
        if not boxed_results:
            return 0, 0, 0, 0

        index_list = self.filter(boxed_results, keyword)
        logger.info(f"OCR [{self.name}] detected in {
                    index_list} with {boxed_results[index_list[0]]}")
        # 如果一个都没有匹配到
        if not index_list:
            return 0, 0, 0, 0

        # 如果匹配到了多个,则合并所有的坐标，返回合并后的坐标
        if len(index_list) > 1:
            area_list = [(
                boxed_results[index].box[0, 0],  # x
                boxed_results[index].box[0, 1],  # y
                boxed_results[index].box[1, 0] - \
                boxed_results[index].box[0, 0],     # width
                boxed_results[index].box[2, 1] - \
                boxed_results[index].box[0, 1],     # height
            ) for index in index_list]
            area = merge_area(area_list)
            self.area = area[0] + self.roi[0], area[1] + \
                self.roi[1], area[2], area[3]
        else:
            box = boxed_results[index_list[0]].box
            self.area = box[0, 0] + self.roi[0], box[0, 1] + \
                self.roi[1], box[1, 0] - box[0, 0], box[2, 1] - box[0, 1]

        # # 测试用
        # logger.warning(str(self.area))
        # rec = np.int64(self.area)
        # cv2.rectangle(screenshot, (rec[0], rec[1]),
        #               (rec[0] + rec[2], rec[1] + rec[3]), (101, 67, 196), 2)
        # cv2.imwrite(f'{Path.cwd()}/buff_output.png', screenshot)

        logger.info(f"OCR [{self.name}] detected in {self.area}")
        return self.area

    def ocr_single(self, screenshot) -> str:
        screenshot = self.crop(screenshot)
        res = text_sys.ocr_single_line(screenshot)
        logger.info(f"<ocr> result: {res[0]}")
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

    def enlarge_canvas(self, image):
        """
        copy from https://github.com/LmeSzinc/StarRailCopilot
        Enlarge image into a square fill with black background. In the structure of PaddleOCR,
        image with w:h=1:1 is the best while 3:1 rectangles takes three times as long.
        Also enlarge into the integer multiple of 32 cause PaddleOCR will downscale images to 1/32.
        """
        height, width = image.shape[:2]
        length = int(max(width, height) // 32 * 32 + 32)
        border = (0, length - height, 0, length - width)
        if sum(border) > 0:
            image = cv2.copyMakeBorder(
                image, *border, borderType=cv2.BORDER_CONSTANT, value=(0, 0, 0))
        return image

    def detect_and_ocr(self, image) -> list[BoxedResult]:
        """
        注意：这里使用了预处理和后处理
        :param image:
        :return:
        """
        # pre process
        start_time = time.time()
        image = self.crop(image)
        image = self.enlarge_canvas(image)

        # ocr
        boxed_results: list[BoxedResult] = self.model.detect_and_ocr(image)
        results = []
        # after proces
        for result in boxed_results:
            # logger.info("ocr result score: %s" % result.score)
            if result.score < self.score:
                continue
            results.append(result)

        logger.info('%s %ss' %
                    (self.name, float2str(time.time() - start_time)))
        logger.info(str([result.ocr_text for result in results]))
        return results

    def filter(self, boxed_results: list[BoxedResult], keyword: str = None) -> list or None:
        """
        使用ocr获取结果后和keyword进行匹配. 返回匹配的index list
        :param keyword: 如果不指定默认适用对象的keyword
        :param boxed_results:
        :return:
        """
        # 首先先将所有的ocr的str顺序拼接起来, 然后再进行匹配
        result = None
        strings = [boxed_result.ocr_text for boxed_result in boxed_results]
        concatenated_string = "".join(strings)
        if keyword is None:
            keyword = self.keyword
        if keyword in concatenated_string:
            result = [index for index, word in enumerate(
                strings) if keyword in word]
        else:
            result = None

        if result is not None:
            # logger.info("Filter result: %s" % result)
            return result
