import random
import time
from module.base.logger import logger
from module.base.timer import Timer
from module.config.enums import BuffClass
from tasks.battle.assets import BattleAssets
from tasks.buff.buff import Buff
from tasks.general.page import Page
from tasks.task_base import TaskBase
from module.base.exception import RequestHumanTakeover
from tasks.general.page import page_main

class Battle(Buff, BattleAssets):

    def run_battle(self) -> bool:
        # 有的时候是长战斗，需要在设置stuck检测为长战斗
        # 但是无需取消设置，因为如果有点击或者滑动的话 handle_control_check会自行取消掉
        self.device.stuck_record_add('BATTLE_STATUS_S')
        self.device.click_record_clear()

        # 战斗过程 随机点击和滑动 防封
        logger.info("Start battle process")
        win = False

        while 1:
            time.sleep(0.4)
            self.screenshot()

            if self.appear(self.I_BATTLE_WIN):
                win = True
                break

            if self.appear(self.I_BATTLE_REWARD):
                win = True
                break

            if self.appear(self.I_BATTLE_FIGHT_AGAIN):
                break

        logger.info(f"** Got battle result: {win}")
        if not win:
            action_click = random.choice(
                [self.C_WIN_1, self.C_WIN_2, self.C_WIN_3, self.C_WIN_4])
            self.click(action_click)
            return win

        logger.info("Get reward")
        timeout = Timer(5, 5).start()
        got_reward = False
        while 1:
            if timeout.reached():
                break

            self.screenshot()
            if got_reward and not self.appear(self.I_BATTLE_REWARD):
                break

            # 如果出现领奖励
            action_click = random.choice(
                [self.C_REWARD_1, self.C_REWARD_2])
            if self.appear(self.I_BATTLE_REWARD):
                self.click(action_click)
                got_reward = True
                continue

            if self.appear(self.I_BATTLE_WIN):
                self.click(action_click)

        time.sleep(1)
        return win

    def run_battle_quit(self):
        """
        进入挑战然后直接退出
        :param config:
        :return:
        """
        # 退出
        while 1:
            time.sleep(1)
            self.screenshot()
            if self.appear(self.I_BATTLE_FIGHT_AGAIN):
                break

            if self.appear_then_click(self.I_BATTLE_EXIT):
                self.appear_then_click(self.I_BATTLE_EXIT_CONFIRM)
                continue

        logger.info("Clicked exit battle confirm")
        while 1:
            time.sleep(0.5)
            self.screenshot()
            if self.appear(self.I_BATTLE_FIGHT_AGAIN):
                action_click = random.choice(
                    [self.C_WIN_1, self.C_WIN_2, self.C_WIN_3, self.C_WIN_4])
                self.click(action_click)
                continue
            if not self.appear(self.I_BATTLE_FIGHT_AGAIN):
                break

        return True

    def exit_battle(self) -> bool:
        self.screenshot()

        if not self.appear(self.I_BATTLE_EXIT):
            return False

        # 点击返回
        logger.info(f"Click {self.I_BATTLE_EXIT.name}")
        while 1:
            time.sleep(0.2)
            self.screenshot()
            if self.appear_then_click(self.I_BATTLE_EXIT):
                continue
            if self.appear(self.I_BATTLE_EXIT_CONFIRM):
                break

        # 点击返回确认
        while 1:
            time.sleep(0.2)
            self.screenshot()
            if self.appear_then_click(self.I_BATTLE_EXIT_CONFIRM):
                continue
            if self.appear_then_click(self.I_BATTLE_FAILED):
                continue
            if not self.appear(self.I_BATTLE_EXIT):
                break

        return True

    def check_buff(self, buff: list[BuffClass] = None, page: Page = page_main):
        if not buff:
            return

        match_buff = {
            BuffClass.AWAKE: (self.awake, True),
            BuffClass.SOUL: (self.soul, True),
            BuffClass.GOLD_50: (self.gold_50, True),
            BuffClass.GOLD_100: (self.gold_100, True),
            BuffClass.EXP_50: (self.exp_50, True),
            BuffClass.EXP_100: (self.exp_100, True),
            BuffClass.AWAKE_CLOSE: (self.awake, False),
            BuffClass.SOUL_CLOSE: (self.soul, False),
            BuffClass.GOLD_50_CLOSE: (self.gold_50, False),
            BuffClass.GOLD_100_CLOSE: (self.gold_100, False),
            BuffClass.EXP_50_CLOSE: (self.exp_50, False),
            BuffClass.EXP_100_CLOSE: (self.exp_100, False),
        }

        self.open_buff(page)
        for b in buff:
            func, is_open = match_buff[b]
            func(is_open)
            time.sleep(0.1)

        logger.info(f'Open buff success')
        self.close_buff()
