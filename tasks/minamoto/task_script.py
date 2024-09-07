import time
from tasks.general.general import General
from tasks.minamoto.assets import MinamotoAssets
from tasks.general.page import page_minamoto, page_main
from module.base.exception import RequestHumanTakeover, TaskEnd
from tasks.battle.battle import Battle
from module.base.logger import logger

class TaskScript(General, MinamotoAssets, Battle):

    def run(self):
        if not self.check_page_appear(page_minamoto):
            self.goto(page_minamoto)

        # 进入鬼兵演武
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if self.appear(self.I_GHOST_CHALLENGE):
                break

            if self.wait_until_appear(self.I_GHOST_ENT):
                self.appear_then_click(self.I_GHOST_ENT)
                continue

        image = self.screenshot()
        level = self.O_GHOST_LEVEL.digit(image)
        self.toggle_team_lock()
        while level < 40:
            self.enter_battle()
            if not self.run_battle():
                break

        # 满级了，结束
        self.goto(page_main)
        raise TaskEnd(self.name)

    def enter_battle(self):
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if not self.appear(self.I_GHOST_CHALLENGE):
                break

            if self.appear_then_click(self.I_GHOST_CHALLENGE):
                continue

    def toggle_team_lock(self, lock: bool = True):
        # 锁定队伍
        if not lock:
            if self.wait_until_appear(self.I_TEAM_LOCK, 1):
                self.wait_until_click(self.I_TEAM_LOCK)
                logger.info("Unlock the team")
                return True

        # 不锁定队伍
        if lock:
            if self.wait_until_appear(self.I_TEAM_UNLOCK, 1):
                self.wait_until_click(self.I_TEAM_UNLOCK)
                logger.info("Lock the team")
                return True

        return False
