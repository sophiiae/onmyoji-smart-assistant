from datetime import datetime
from typing import Union
import numpy as np
import time

from module.base.exception import RequestHumanTakeover
from module.config.config import Config
from module.image_processing.rule_click import RuleClick
from module.image_processing.rule_image import RuleImage
from module.image_processing.rule_swipe import RuleSwipe
from tasks.main_page.assets import MainPageAssets
from module.server.device import Device
from module.base.timer import Timer
from module.base.logger import logger

class TaskBase(MainPageAssets):
    config: Config = None
    device: Device = None

    limit_time = None  # 限制运行的时间，是软时间，不是硬时间
    limit_count: int = None  # 限制运行的次数
    current_count: int = None  # 当前运行的次数

    def __init__(self, config: Config, device: Device) -> None:
        """

        :rtype: object
        """
        self.config = config
        self.device = device

        self.interval_timer = {}  # 这个是用来记录每个匹配的运行间隔的，用于控制运行频率
        self.animates = {}  # 保存缓存
        self.start_time = datetime.now()  # 启动的时间
        self.current_count = 0  # 战斗次数

    def _burst(self) -> bool:
        """
        游戏界面突发异常检测
        :return: 没有出现返回False, 其他True
        """

        appear_invitation = self.appear(self.I_QUEST_ACCEPT)
        if not appear_invitation:
            return False
        logger.info('Invitation appearing')

        # 只接受勾协
        if self.appear(self.I_QUEST_JADE) or self.appear(self.I_QUEST_CAT) or self.appear(self.I_QUEST_DOG):
            click_button = self.I_QUEST_ACCEPT
        elif self.appear(self.I_QUEST_VIRTUAL):
            click_button = self.I_QUEST_ACCEPT
        else:
            click_button = self.I_QUEST_IGNORE

        while 1:
            self.device.screenshot()
            if not self.appear(target=click_button):
                logger.info('Deal with invitation done')
                break
            if self.appear_then_click(click_button):
                continue
        return True

    def wait_request(self) -> bool:
        self.device.screenshot()
        return self._burst()

    def appear(self, target: RuleImage, threshold: float = 0.9, delay: float = 0.1) -> bool:
        if not isinstance(target, RuleImage):
            return False
        time.sleep(0.1)
        screenshot = self.device.image
        if screenshot is None:
            screenshot = self.screenshot()
        return target.match_target(screenshot, threshold)

    def wait_until_click(self,
                         target: RuleImage, limit: float = 5, interval: float = 0.3,
                         delay: float = 0.3, wait_after: float = 0.5,
                         threshold: float = 0.9) -> bool:
        """等待出现了再点击，用于不移动的图标

        Args:
            target (RuleImage): 
            limit (float, optional): waiting time limit (s). Defaults to 5.
            interval (float, optional): interval between retry. Defaults to 0.4.
            delay (float, optional): Defaults to 0.5.
            wait_after (float, optional): Defaults to 0.8.
            threshold (float, optional): Defaults to 0.9.
        """

        if self.wait_until_appear(target, limit, interval, threshold=threshold):
            time.sleep(delay)
            self.appear_then_click(target)
            time.sleep(wait_after)
            return True

        logger.critical(f"Not able to find and click {target.name}.")
        raise RequestHumanTakeover

    def wait_until_appear(self,
                          target: RuleImage, limit: float = 5,
                          interval: float = 0.4, threshold: float = 0.9
                          ) -> bool:
        """等待出现了再点击，比如需要等过场动画，减少不必要的运行消耗
        Args:
            target (RuleImage):
            limit (float, optional): waiting time limit (s). Defaults to 3.
            interval (float, optional): interval between retry. Defaults to 0.4.
            threshold (float, optional): Defaults to 0.9.
        """
        if not isinstance(target, RuleImage):
            return False

        timeout = Timer(limit + interval, 2).start()
        while not timeout.reached():
            time.sleep(interval)
            self.screenshot()
            if self.appear(target, threshold=threshold):
                return True
        return False

    def appear_then_click(self,
                          target: RuleImage,
                          threshold: float = 0.9,
                          ) -> bool:
        """出现就点击，用于会移动的怪物/图标
        Args:
            target (RuleImage): _description_
            threshold (float, optional): _description_. Defaults to 0.9.
            interval (float, optional): _description_. Defaults to 1.
        """
        if not isinstance(target, RuleImage):
            return False

        appear = self.appear(target, threshold=threshold)
        if appear:
            x, y = target.coord()
            self.device.click(x, y)
        return appear

    def wait_for_result(self, pass_t: RuleImage, fail_t: RuleImage,
                        limit: float = 10,
                        interval: float = 0.4) -> bool:
        """判断其中一种结果出现，比如战斗胜利/失败
        Args:
            pass_t (RuleImage):
            fail_t (RuleImage):
            limit (float, optional):. Defaults to 10.
            interval (float, optional):. Defaults to 0.4.
        """

        timeout = Timer(limit).start()
        while not timeout.reached():
            time.sleep(interval)

            self.screenshot()
            if self.appear(pass_t):
                logger.info(f"---- Got Action Success Target: {pass_t.name}")
                return True
            if self.appear(fail_t):
                logger.info(f"---- Got Action failed Target: {fail_t.name}")
                return False

        logger.warning(
            f"Wait until appear {pass_t.name} or {fail_t.name} timeout")

        raise RequestHumanTakeover

    def screenshot(self):
        """截图 引入中间函数的目的是 为了解决如协作的这类突发的事件

        Returns:
            np.array: image
        """
        self.device.screenshot()
        # 判断勾协
        self._burst()
        return self.device.image

    def swipe(self, swipe: RuleSwipe, interval: float = None, duration: int = 400) -> None:
        """swipe

        Args:
            swipe (RuleSwipe): 
            interval (float, optional): Defaults to None.
            duration (int, optional): [200,800] Defaults to 300.
        """
        if not isinstance(swipe, RuleSwipe):
            return

        if interval:
            if swipe.name in self.interval_timer:
                # 如果传入的限制时间不一样，则替换限制新的传入的时间
                if self.interval_timer[swipe.name].waiting_limit != interval:
                    self.interval_timer[swipe.name] = Timer(interval)
            else:
                # 如果没有限制时间，则创建限制时间
                self.interval_timer[swipe.name] = Timer(interval)
            # 如果时间还没到达，则不执行
            if not self.interval_timer[swipe.name].reached():
                return

        logger.info(f"Executing Swipe for {swipe.name}")
        sx, sy, ex, ey = swipe.coord()
        self.device.swipe(start_x=sx, start_y=sy, end_x=ex,
                          end_y=ey, duration=duration)

        # 执行后，如果有限制时间，则重置限制时间
        if interval:
            # logger.info(f'Swipe {swipe.name}')
            self.interval_timer[swipe.name].reset()

    def click(self, target: Union[RuleImage, RuleClick], click_delay: float = 0.2) -> bool:
        """click

        Args:
            target (RuleImage):
            interval (float, optional): Defaults to None.

        Returns:
            bool:
        """
        time.sleep(click_delay)
        x, y = target.coord()
        self.device.click(x=x, y=y)
        time.sleep(0.5)
        return False

    def random_click_right(self, click_delay=0.2):
        """Perform random click within screen
        """
        time.sleep(click_delay)
        x = np.random.randint(990, 1260)
        y = np.random.randint(180, 550)
        self.device.click(x=x, y=y)

    def click_until_disappear(self, target: RuleImage, interval: float = 1):
        """点击一个按钮直到消失

        Args:
            target (RuleImage):
            interval (float, optional): Defaults to 1.
        """
        while 1:
            self.screenshot()
            if not self.appear(target):
                break
            elif self.wait_until_appear(target, click=True):
                continue

    def set_next_run(self, task: str, finish: bool = False,
                     success: bool = None, target_time: datetime = None) -> None:
        if finish:
            start_time = datetime.now().replace(microsecond=0)
        else:
            start_time = self.start_time
        self.config.task_delay(task, start_time=start_time,
                               success=success, target_time=target_time)
