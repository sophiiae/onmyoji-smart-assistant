
import numpy as np

class RuleClick:

    def __init__(self, roi: tuple, area: tuple, name: str = None) -> None:
        """
        初始化
        :param roi:
        :param area:
        """
        self.roi = roi
        self.area = area
        if name:
            self.name = name
        else:
            self.name = 'click'

    def coord(self) -> tuple:
        """
        获取坐标, 从roi随机获取坐标
        :return:
        """
        x, y, w, h = self.roi
        x = np.random.randint(x, x + w)
        y = np.random.randint(y, y + h)
        return x, y

    @property
    def center(self) -> tuple:
        """
        返回roi的中心坐标
        :return:
        """
        x, y, w, h = self.roi
        return x + w // 2, y + h // 2
