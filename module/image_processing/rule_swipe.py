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
        start_tl_x, start_tl_y, start_br_x, start_br_y = self.roi_start
        sx = np.random.randint(start_tl_x, start_br_x)
        sy = np.random.randint(start_tl_y, start_br_y)

        end_tl_x, end_tl_y, end_br_x, end_br_y = self.roi_end
        ex = np.random.randint(end_tl_x, end_br_x)
        ey = np.random.randint(end_tl_y, end_br_y)

        return (sx, sy, ex, ey)
