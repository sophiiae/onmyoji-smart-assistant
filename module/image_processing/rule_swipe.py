from functools import cached_property
import numpy as np

class RuleSwipe:

    def __init__(self, roi_start: tuple, roi_end: tuple, name: str) -> None:
        """
        初始化
        :param roi_start:
        :param roi_end:
        :param mode:
        """
        self.roi_start = roi_start
        self.roi_end = roi_end
        self.name = name

        self.interval: int = 8  # 每次移动的间隔时间

    @cached_property
    def name(self) -> str:
        """

        :return:
        """
        return self.name.stem.upper()

    def coord(self) -> tuple:
        """
        获取坐标, 从roi_start随机获取坐标 和从roi_end随机获取的坐标
        :return: 两个坐标的tuple
        """
        x, y, w, h = self.roi_start
        x = np.random.randint(x, x + w)
        y = np.random.randint(y, y + h)

        x2, y2, w2, h2 = self.roi_end
        x2 = np.random.randint(x2, x2 + w2)
        y2 = np.random.randint(y2, y2 + h2)

        return (x, y, x2, y2)
