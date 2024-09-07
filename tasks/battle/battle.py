import random
import time
from module.base.logger import logger
from tasks.battle.assets import BattleAssets
from tasks.task_base import TaskBase
from module.base.exception import RequestHumanTakeover


class Battle(TaskBase, BattleAssets):

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

        if not self.wait_until_appear(self.I_BATTLE_REWARD, 1.2):
            action_click = random.choice(
                [self.C_WIN_1, self.C_WIN_2, self.C_WIN_3, self.C_WIN_4])
            self.click(action_click)
            return win

        logger.info("Get reward")
        got_reward = False
        while 1:
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
