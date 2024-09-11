import time
import random
from module.base.logger import logger
from tasks.battle.battle import Battle
from tasks.general.page import Page, page_exp, page_shikigami
from tasks.shikigami_activity.assets import ShikigamiActivityAssets as SA
from module.base.exception import RequestHumanTakeover

class TaskScript(Battle, SA):

    def run(self):
        # 进入式神活动页面
        if not self.check_page_appear(page_shikigami):
            self.goto(page_shikigami)

        time.sleep(1)

        # 进入爬塔页面
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if not self.appear(self.I_SA_FIGHT_ENT):
                break

            if self.appear(self.I_SA_FIGHT_ENT):
                self.click(self.I_SA_FIGHT_ENT)

        self.toggle_team()
        no_ticket = self.appear(self.I_SA_NO_TICKETS)
        if not no_ticket:
            self.switch_mode(False)

        while not no_ticket:
            self.start_battle()
            if self.wait_until_appear(self.I_SA_FIGHT_CHECK, 2):
                no_ticket = self.appear(self.I_SA_NO_TICKETS)
            else:
                raise RequestHumanTakeover

        self.switch_mode()

        # 用体力刷999
        count = 0
        while count < 999:
            logger.info(f"======== Round {count + 1} by EP =========")
            self.start_battle()
            if not self.wait_until_appear(self.I_SA_FIGHT_CHECK, 2):
                raise RequestHumanTakeover

        # 返回庭院
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if self.appear(self.I_C_MAIN):
                break
            if self.appear(self.I_SA_EXIT):
                self.click(self.I_SA_EXIT)

    def start_battle(self):
        while 1:
            time.sleep(0.4)
            self.screenshot()
            if not self.appear(self.I_SA_FIGHT_CHECK):
                break

            if self.appear(self.I_SA_FIGHT):
                self.click(self.I_SA_FIGHT)

        while 1:
            time.sleep(0.4)
            self.screenshot()
            if self.appear(self.I_SA_FIGHT_CHECK):
                break

            if self.appear(self.I_SA_GAIN_REWARD):
                # 如果出现领奖励
                action_click = random.choice(
                    [self.C_REWARD_1, self.C_REWARD_2])
                if self.appear(self.I_SA_GAIN_REWARD):
                    self.click(action_click)
                    continue

            if self.appear(self.I_SA_BATTLE_WIN):
                # 出现胜利
                action_click = random.choice(
                    [self.C_WIN_1, self.C_WIN_2, self.C_WIN_3, self.C_WIN_4])
                self.click(action_click)

    def switch_mode(self, use_ep: bool = True):
        if use_ep:
            while 1:
                time.sleep(0.3)
                self.screenshot()
                if self.appear(self.I_SA_EP):
                    logger.info("Using EP")
                    return True

                if self.appear(self.I_SA_TICKET):
                    self.wait_until_click(self.I_SA_SWITCH)

        if not use_ep:
            while 1:
                time.sleep(0.3)
                self.screenshot()
                if self.appear(self.I_SA_TICKET):
                    logger.info("Using ticket")
                    return True

                if self.appear(self.I_SA_EP):
                    self.wait_until_click(self.I_SA_SWITCH)

    def toggle_team(self, lock: bool = True):
        return self.toggle_team_lock(self.I_SA_TEAM_LOCK, self.I_SA_TEAM_UNLOCK, lock)
