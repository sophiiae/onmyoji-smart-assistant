from datetime import datetime
import numpy as np
import time

from module.config.config import Config
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
        return

        appear_invitation = self.appear(self.I_QUEST_ACCEPT)
        if not appear_invitation:
            return False
        logger.info('Invitation appearing')

        # 只接受勾协
        if self.appear(self.I_QUEST_JADE) or self.appear(self.I_QUEST_CAT) or self.appear(self.I_QUEST_DOG):
            click_button = self.I_QUEST_ACCEPT
        elif self.appear(self.I_QUEST_VIRTUAL) and self.appear(self.I_QUEST_EP):
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

    def appear(self, target: RuleImage, threshold: float = 0.9) -> bool:
        if not isinstance(target, RuleImage):
            return False

        return target.match_target(self.device.image, threshold)

    def wait_until_appear(self, target: RuleImage, waiting_limit: float = 10, retry_limit: float = 5, waiting_interval: float = 0.2, threshold: float = 0.9, click: bool = False, click_delay: float = 0.2):
        if not isinstance(target, RuleImage):
            return False

        timeout = Timer(waiting_limit, retry_limit).start()
        while 1:
            time.sleep(waiting_interval)
            self.screenshot()
            if self.appear(target, threshold=threshold):
                logger.info(f"#### Found target: {target.name}")
                if click:
                    time.sleep(click_delay)
                    x, y = target.coord()
                    self.device.click(x, y)
                break

            if timeout.reached():
                logger.error(f"Wait until appear {target.name} timeout")
                return False

        return True

    def appear_then_click(self,
                          target: RuleImage,
                          threshold: float = 0.95,
                          ) -> bool:
        """wait until appear, then click

        Args:
            target (RuleImage): _description_
            threshold (float, optional): _description_. Defaults to 0.9.
            interval (float, optional): _description_. Defaults to 1.

        Returns:
            bool: _description_
        """
        if not isinstance(target, RuleImage):
            return False

        appear = self.appear(target, threshold=threshold)
        if appear:
            x, y = target.coord()
            self.device.click(x, y)
        return appear

    def screenshot(self):
        """截图 引入中间函数的目的是 为了解决如协作的这类突发的事件

        Returns:
            np.array: image
        """
        self.device.screenshot()
        # 判断勾协
        self._burst()
        return self.device.image

    def swipe(self, swipe: RuleSwipe, interval: float = None, duration: int = 300) -> None:
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
                if self.interval_timer[swipe.name].limit != interval:
                    self.interval_timer[swipe.name] = Timer(interval)
            else:
                # 如果没有限制时间，则创建限制时间
                self.interval_timer[swipe.name] = Timer(interval)
            # 如果时间还没到达，则不执行
            if not self.interval_timer[swipe.name].reached():
                return

        print(f"Executing Swipe for {swipe.name}")
        sx, sy, ex, ey = swipe.coord()
        self.device.swipe(start_x=sx, start_y=sy, end_x=ex,
                          end_y=ey, duration=duration)

        # 执行后，如果有限制时间，则重置限制时间
        if interval:
            # logger.info(f'Swipe {swipe.name}')
            self.interval_timer[swipe.name].reset()

    def click(self, target: RuleImage, click_delay: float = 0.2) -> bool:
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

    def random_click(self, click_delay=0.2):
        """Perform random click within screen
        """
        time.sleep(click_delay)
        x = np.random.randint(0, 1270)
        y = np.random.randint(0, 700)
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
