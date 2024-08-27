
from module.base.logger import logger
from module.base.exception import RequestHumanTakeover, TaskEnd
from module.config.config_base import ScrollModeConfig
from tasks.exploration.assets import ExplorationAssets
from tasks.general.general import General
from tasks.general.page import page_exp, page_main

from datetime import datetime, timedelta
import time

class TaskScript(General, ExplorationAssets):

    def run(self):
        config = self.config.model.exploration

        # 进入探索页面
        if not self.check_page_appear(page_exp):
            self.goto(page_exp)

        if not self.open_chapter_entrance():
            logger.critical(":: Not able to reach Exploration page ::")
            return

        # 判断是否开启绘卷模式
        scroll_mode = config.scroll_mode
        if scroll_mode.scroll_mode_enable:
            exp_count = 50
        else:
            exp_count = config.exploration_config.count_max

        count = 0
        while exp_count > 0 and count < exp_count:
            logger.info(f"======== Round {count + 1} Exp Started =========")
            # 检测绘卷模式
            self.activate_realm_raid(scroll_mode)

            # 进入章节探索
            self.enter_battle()

            # 查看宝箱
            if self.wait_until_appear(self.I_C_EXP, 2):
                self.check_treasure_box()
                self.open_chapter_entrance()

            count += 1

        # 关闭章节探索提示
        if self.wait_until_appear(self.I_EXP_CHAPTER_DISMISS_ICON, 2):
            self.appear_then_click(self.I_EXP_CHAPTER_DISMISS_ICON)

        self.goto(page_main)
        self.set_next_run(task='Exploration', success=True, finish=False)

        raise TaskEnd

    def open_chapter_entrance(self) -> bool:
        if self.wait_until_appear(self.I_C_EXP, wait_time=5, threshold=0.95):
            if not self.appear_then_click(ExplorationAssets.I_EXP_CHAPTER_28):
                logger.critical(":: Fatal: CH 28 not found! ::")
                return False
            return True
        elif self.wait_until_appear(self.I_EXP_BUTTON):
            self.click(self.I_EXP_CHAPTER_DISMISS_ICON)
            return True

        logger.critical(":: Fatal: Not in Exploration page ::")
        return False

    def check_treasure_box(self):
        if self.appear_then_click(
            self.I_EXP_TREASURE_BOX_LEFT,
            threshold=0.95
        ):
            got_reward = self.wait_until_appear(
                self.I_FIGHT_REWARD, wait_time=3)
            if got_reward:   # 领取宝箱物品
                time.sleep(1)
                self.click(self.I_FIGHT_REWARD)

    def enter_battle(self):
        self.screenshot()

        # 点击 “探索” 按钮进入章节
        if self.wait_until_appear(ExplorationAssets.I_EXP_BUTTON):
            self.click(ExplorationAssets.I_EXP_BUTTON)
            logger.info("** Entered ch 28")

        beat_boss = False

        while 1:
            if not self.wait_until_appear(ExplorationAssets.I_AUTO_ROTATE_ON):
                logger.warning("***** Not inside chapter or battle finished.")
                break

            # 章节通关奖励
            if beat_boss and self.wait_until_appear(self.I_EXP_CHAP_REWARD, 2):
                self.click(self.I_EXP_CHAP_REWARD)
                if self.wait_until_appear(self.I_EXP_GAIN_REWARD):
                    self.random_click()

            # start chapter battle
            if self.appear_then_click(ExplorationAssets.I_EXP_BOSS):
                beat_boss = self.fight()

            if self.appear_then_click(ExplorationAssets.I_EXP_FIGHT_BUTTON):
                self.fight()

            elif self.appear(self.I_C_EXP, threshold=0.95) or self.appear(ExplorationAssets.I_EXP_BUTTON, threshold=0.95):
                break

            else:
                self.swipe(self.S_EXP_TO_RIGHT)

    def fight(self) -> bool:
        win = True

        # 等战斗结束
        win = self.wait_until_appear(self.I_EXP_BATTLE_WIN, 30)
        self.click(self.I_EXP_BATTLE_WIN)

        if win:
            # 领取战斗奖励，需要等动画
            got_reward = self.wait_until_appear(self.I_FIGHT_REWARD, 5)
            if got_reward:
                time.sleep(1)
                self.click(self.I_FIGHT_REWARD)

        if not win:
            logger.critical("!! Fight Failed !!")
        return win

    def activate_realm_raid(self, scroll_mode: ScrollModeConfig):
        logger.info("Activate realm raid...")
        if not scroll_mode.scroll_mode_enable:
            return

        if self.wait_until_appear(self.I_EXP_BUTTON, 2):
            image = self.screenshot()
            res = self.O_EXP_CHAPTER_TICKET_COUNT.ocr_single(image)
        elif self.appear(self.I_C_EXP):
            image = self.screenshot()
            res = self.O_EXP_VIEW_TICKET_COUNT.ocr_single(image)
        else:
            logger.error(":: Not able to found ticket number ::")
            return

        count = res.split("/")[0]
        if count.isdigit():
            count = int(count)
        else:
            logger.error(":: Invalid ocr ticket number ::")
            return

        # 判断突破票数量
        if count < scroll_mode.ticket_threshold:
            return

        # 设置下次执行行时间
        logger.info("|| RealmRaid and Exploration set_next_run ||")

        # TODO: update time format in config
        hr, min, sec = scroll_mode.scrolls_cd.split(":")
        next_run = datetime.now() + timedelta(hours=int(hr),
                                              minutes=int(min),
                                              seconds=int(sec))
        logger.critical(f"##########  next run time: {next_run}")
        self.set_next_run(task='Exploration', success=False,
                          finish=False, target_time=next_run)
        self.set_next_run(task='RealmRaid', success=False,
                          finish=False, target_time=datetime.now())

        raise TaskEnd
