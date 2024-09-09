import time
import cv2
from pathlib import Path

from module.base.logger import logger
from module.image_processing.rule_ocr import RuleOcr
from module.image_processing.rule_image import RuleImage
from tasks.buff.assets import BuffAssets
from tasks.task_base import TaskBase
from tasks.general.page import Page
from tasks.general.page import page_main, page_exp, page_minamoto


class Buff(TaskBase, BuffAssets):

    def open_buff(self, page: Page = page_main):
        """
        打开buff的总界面
        :return:
        """
        logger.info('Open buff')

        match_open = {
            page_main: self.I_BUFF_OPEN,
            page_exp: self.I_EXP_BUFF_OPEN,
            page_minamoto: self.I_MINAMOTO_BUFF_OPEN
        }
        open_button = match_open[page]

        while 1:
            time.sleep(0.3)
            self.screenshot()
            if self.appear(self.I_BUFF_AWAKE, 0.95):
                break

            if self.appear_then_click(open_button):
                continue

    def close_buff(self):
        """
        关闭buff的总界面, 但是要确保buff界面已经打开了
        :return:
        """
        logger.info('Close buff')

        while 1:
            time.sleep(0.3)
            self.screenshot()
            if not self.appear(self.I_BUFF_AWAKE, 0.95):
                break
            if self.appear_then_click(self.I_BUFF_CLOUD):
                continue

    def get_area(self, buff: RuleOcr) -> tuple:
        """
        获取要点击的开关buff的区域
        :param cls:
        :param image:
        :param buff:
        :return:  如果没有就返回None
        """
        self.screenshot()
        area = buff.ocr_full(self.device.image)

        if area == tuple([0, 0, 0, 0]):
            logger.info(f'No {buff.name} buff')
            return None

        # 开始的x坐标就是文字的右边
        start_x = area[0] + area[2] + 10  # 10是文字和开关之间的间隔
        start_y = area[1] - 10
        width = 80  # 开关的宽度 80够了
        height = area[3] + 20
        return int(start_x), int(start_y), int(width), int(height)

    def set_switch_area(self, area):
        """
        设置开关的区域
        :param area:
        :return:
        """
        self.I_BUFF_OPEN_YELLOW.area = list(area)  # 动态设置roi
        self.I_BUFF_CLOSE_RED.area = list(area)

    def toggle_buff(self, is_open: bool = True):
        if is_open:
            while 1:
                time.sleep(0.3)
                self.screenshot()
                if self.appear(self.I_BUFF_OPEN_YELLOW):
                    break
                if self.wait_until_click(self.I_BUFF_CLOSE_RED, 1):
                    continue
        else:
            while 1:
                time.sleep(0.3)
                self.screenshot()
                if self.appear(self.I_BUFF_CLOSE_RED):
                    break
                if self.wait_until_click(self.I_BUFF_OPEN_YELLOW, 1):
                    continue

    def awake(self, is_open: bool = True):
        """
        觉醒buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Awake buff')
        self.screenshot()
        area = self.get_area_image(self.I_BUFF_AWAKE)
        if not area:
            logger.warning('No awake buff')
            return None
        self.set_switch_area(area)
        self.toggle_buff(is_open)

    def soul(self, is_open: bool = True):
        """
        御魂buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Soul buff')
        self.screenshot()
        area = self.get_area_image(self.I_BUFF_SOUL)
        if not area:
            logger.warning('No soul buff')
            return None
        self.set_switch_area(area)
        self.toggle_buff(is_open)

    def gold_50(self, is_open: bool = True):
        """
        金币50buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Gold 50 buff')
        self.screenshot()
        area = self.get_area(self.O_GOLD_50)
        if not area:
            logger.warning('No gold 50 buff')
            return None
        self.I_BUFF_OPEN_YELLOW.area = list(area)  # 动态设置roi
        self.I_BUFF_CLOSE_RED.area = list(area)
        self.toggle_buff(is_open)

    def gold_100(self, is_open: bool = True):
        """
        金币100buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Gold 100 buff')
        self.screenshot()
        area = self.get_area(self.O_GOLD_100)
        if not area:
            logger.warning('No gold 100 buff')
            return None
        self.I_BUFF_OPEN_YELLOW.area = list(area)
        self.I_BUFF_CLOSE_RED.area = list(area)
        self.toggle_buff(is_open)

    def exp_50(self, is_open: bool = True):
        """
        经验50buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Exp 50 buff')
        while 1:
            time.sleep(0.3)
            self.screenshot()
            area = self.get_area(self.O_EXP_50)
            if not area:
                logger.warning('No exp 50 buff')
                continue
            self.set_switch_area(area)

            if not self.appear(self.I_BUFF_OPEN_YELLOW) and not self.appear(self.I_BUFF_CLOSE_RED):
                logger.info('No exp 50 buff')
                self.device.swipe(530, 240, 580, 320)
                time.sleep(0.7)
            else:
                break
        self.toggle_buff(is_open)

    def exp_100(self, is_open: bool = True):
        """
        经验100buff
        :param is_open: 是否打开
        :return:
        """
        logger.info('Exp 100 buff')

        while 1:
            time.sleep(0.3)
            self.screenshot()
            area = self.get_area(self.O_EXP_100)
            if not area:
                logger.warning('No exp 100 buff')
                continue
            self.set_switch_area(area)

            if not self.appear(self.I_BUFF_OPEN_YELLOW) and not self.appear(self.I_BUFF_CLOSE_RED):
                logger.info('No exp 100 buff')
                self.device.swipe(530, 240, 580, 320)
                time.sleep(0.7)
            else:
                break
        self.toggle_buff(is_open)

    def get_area_image(self, target: RuleImage) -> list:
        """
        获取觉醒加成或者是御魂加成所要点击的区域
        因为实在的图片比ocr快
        :param image:
        :param target:
        :return:
        """
        self.screenshot()
        if not self.appear(target):
            logger.warning(f'No {target.name} buff')
            return None
        x = int(target.front_center()[0] + 364)
        y = int(target.roi[1])
        w = 80
        h = int(target.roi[3])

        # cv2.rectangle(self.device.image, (x, y),
        #               (x + w, y + h), (101, 67, 196), 2)
        # cv2.imwrite(f'{Path.cwd()}/area.png', self.device.image)
        return [x, y, w, h]
