import time
from module.config.enums import BuffClass
from tasks.minamoto.assets import MinamotoAssets
from tasks.general.page import page_minamoto, page_main
from module.base.exception import TaskEnd
from tasks.battle.battle import Battle
from module.base.logger import logger

class TaskScript(MinamotoAssets, Battle):

    def run(self):
        if not self.check_page_appear(page_minamoto):
            self.goto(page_minamoto)

        # 进入鬼兵演武
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if self.appear(self.I_GHOST_CHALLENGE):
                break

            if self.wait_until_appear(self.I_GHOST_ENT, 2):
                self.appear_then_click(self.I_GHOST_ENT)
                continue

        image = self.screenshot()
        level = self.O_GHOST_LEVEL.digit(image)
        self.toggle_m_team_lock()
        self.check_buff([BuffClass.EXP_100], page_minamoto)
        count = 0
        while level < 60 and count < 5:
            logger.info(f"======== Round {count + 1} Minamoto =========")
            self.enter_battle()
            if not self.run_battle():
                break
            count += 1

        self.check_buff([BuffClass.EXP_100_CLOSE], page_minamoto)
        # 满级了，结束
        self.appear_then_click(self.I_B_YELLOW_LEFT_ANGLE)

        self.goto(page_main, page_minamoto)
        raise TaskEnd(self.name)

    def enter_battle(self):
        while 1:
            time.sleep(0.3)
            self.screenshot()
            if not self.appear(self.I_GHOST_CHALLENGE):
                break

            if self.appear_then_click(self.I_GHOST_CHALLENGE):
                continue

    def toggle_m_team_lock(self, lock: bool = True):
        return self.toggle_team_lock(self.I_TEAM_LOCK, self.I_TEAM_UNLOCK, lock)
