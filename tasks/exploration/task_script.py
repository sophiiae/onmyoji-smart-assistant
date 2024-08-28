
from module.base.logger import logger
from module.base.exception import RequestHumanTakeover, TaskEnd
from module.base.timer import Timer
from module.config.config_base import ScrollModeConfig
from tasks.exploration.assets import ExplorationAssets as EA
from tasks.general.general import General
from tasks.general.page import page_exp, page_main

from datetime import datetime, timedelta
import time

class TaskScript(General, EA):

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

            if self.appear(EA.I_EXP_BUTTON, 2):
                self.wait_until_appear(
                    self.I_EXP_CHAPTER_DISMISS_ICON, 2, click=True)

            # 查看宝箱
            if self.wait_until_appear(self.I_C_EXP):
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
        if self.wait_until_appear(self.I_C_EXP, threshold=0.95):
            if not self.appear_then_click(EA.I_EXP_CHAPTER_28):
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
            self.I_EXP_TREASURE_BOX_MAP,
            threshold=0.9
        ):
            got_reward = self.wait_until_appear(
                self.I_FIGHT_REWARD, 3)
            if got_reward:   # 领取宝箱物品
                time.sleep(1)
                self.click(self.I_FIGHT_REWARD)

    def enter_battle(self):
        self.screenshot()

        # 点击 “探索” 按钮进入章节
        if self.wait_until_appear(EA.I_EXP_BUTTON):
            self.click(EA.I_EXP_BUTTON)
            logger.info("** Entered ch 28")

        swipe_count = 0

        while 1:
            if not self.wait_until_appear(EA.I_AUTO_ROTATE_ON, 1, 0.5):
                if not self.wait_until_appear(EA.I_AUTO_ROTATE_OFF, 1, 0.5):
                    logger.warning(
                        "***** Not inside chapter or battle finished.")
                    raise RequestHumanTakeover

            # BOSS 挑战
            if self.appear(EA.I_EXP_BOSS):
                time.sleep(0.3)
                self.appear_then_click(EA.I_EXP_BOSS)
                if self.fight():
                    if self.wait_until_appear(EA.I_EXP_CHAPTER_DISMISS_ICON, 1):
                        return
                    else:
                        self.get_chapter_reward()
                        return
                else:
                    raise RequestHumanTakeover
            # 普通怪挑战
            if self.appear_then_click(EA.I_EXP_BATTLE):
                self.fight()

            # 如果超过滑动次数
            elif swipe_count > 10:
                logger.error("Not able to find fight target")
                raise RequestHumanTakeover
            else:
                self.swipe(self.S_EXP_TO_RIGHT)
        time.sleep(0.3)

    def get_chapter_reward(self):
        # 章节通关奖励，好像最多只有三个
        found = False
        for _ in range(4):
            if self.wait_until_appear(self.I_EXP_CHAP_REWARD, 5, waiting_interval=1):
                self.click(self.I_EXP_CHAP_REWARD)
                time.sleep(1)
                if self.wait_until_appear(self.I_EXP_GAIN_REWARD, 3, click=True, click_delay=0.5):
                    found = True
        if found:
            logger.info("Got all chapter reward.")

    def fight(self) -> bool:
        win = True

        # 等战斗结束
        time.sleep(8)
        win = self.wait_until_appear(
            self.I_EXP_BATTLE_WIN, waiting_limit=30, waiting_interval=1)
        self.click(self.I_EXP_BATTLE_WIN)

        if win:
            # 领取战斗奖励，需要等动画
            got_reward = self.wait_until_appear(
                self.I_FIGHT_REWARD, waiting_limit=5, waiting_interval=1)
            if got_reward:
                time.sleep(1)
                self.click(self.I_FIGHT_REWARD)

        if not win:
            logger.warning("!! Fight Failed !!")
        time.sleep(0.4)
        return win

    def activate_realm_raid(self, scroll_mode: ScrollModeConfig):
        logger.info("Activate realm raid...")
        if not scroll_mode.scroll_mode_enable:
            return

        # 章节探索确认界面
        if self.wait_until_appear(self.I_EXP_BUTTON, 2):
            time.sleep(0.2)
            image = self.screenshot()
            count, total = self.O_EXP_CHAPTER_TICKET_COUNT.digit_counter(image)
        elif self.appear(self.I_C_EXP):
            time.sleep(0.2)
            image = self.screenshot()
            count, total = self.O_EXP_VIEW_TICKET_COUNT.digit_counter(image)
        else:
            logger.error(":: Not able to found ticket number ::")
            return

        # 判断突破票数量
        if count is None or count < scroll_mode.ticket_threshold:
            return

        # 关闭章节探索确认界面
        self.appear_then_click(EA.I_EXP_CHAPTER_DISMISS_ICON)

        # 设置下次执行行时间
        logger.info("|| RealmRaid and Exploration set_next_run ||")

        # TODO: update time format in config
        hr, min, sec = scroll_mode.scrolls_cd.split(":")
        next_run = datetime.now() + timedelta(hours=int(hr),
                                              minutes=int(min),
                                              seconds=int(sec))
        logger.warning(f"##########  next run time: {next_run}")
        self.set_next_run(task='Exploration', success=False,
                          finish=False, target_time=next_run)
        self.set_next_run(task='RealmRaid', success=False,
                          finish=False, target_time=datetime.now())

        raise TaskEnd
