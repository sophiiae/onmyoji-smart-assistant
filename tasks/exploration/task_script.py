
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
    name = "Exploration"

    def run(self):
        self.exp_config = self.config.model.exploration

        # 进入探索页面
        if not self.check_page_appear(page_exp):
            self.goto(page_exp)

        # 判断是否开启绘卷模式
        scroll_mode = self.exp_config.scroll_mode
        if scroll_mode.scroll_mode_enable:
            exp_count = 50
        else:
            exp_count = self.exp_config.exploration_config.count_max

        count = 0
        while exp_count > 0 and count < exp_count:
            # 检查票数
            self.check_ticket()

            self.open_chapter_entrance()

            logger.info(f"======== Round {count + 1} Exp Started =========")
            # 进入章节探索
            self.enter_chapter()

            # 如果回到了探索界面 -> 检查宝箱
            if self.wait_until_appear(self.I_C_EXP, 5):
                self.check_treasure_box()
            else:
                # 出现章节入口 -> 没有发现 -> 关闭
                self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 2)

            count += 1

        # 关闭章节探索提示
        self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 2)

        self.goto(page_main)
        self.set_next_run(task='Exploration', success=True, finish=False)

        raise TaskEnd(self.name)

    def open_chapter_entrance(self) -> bool:
        if self.wait_until_appear(self.I_C_EXP, 2):
            if not self.wait_until_click(self.I_EXP_CHAPTER_28):
                logger.error(":: Fatal: CH 28 not found! ::")
                return False
            return True

        logger.error(":: Fatal: Not in Exploration page ::")
        return False

    def check_treasure_box(self):
        if self.appear_then_click(
            self.I_EXP_TREASURE_BOX_MAP,
            threshold=0.9
        ):
            got_reward = self.wait_until_appear(
                self.I_FIGHT_REWARD, 3)
            if got_reward:   # 领取宝箱物品
                time.sleep(0.7)
                self.random_click_right()

    def enter_chapter(self):
        # 点击 “探索” 按钮进入章节
        if not self.wait_until_appear(self.I_EXP_BUTTON):
            logger.error("Cannot find chapter exploration button")
            raise RequestHumanTakeover

        self.click(self.I_EXP_BUTTON)
        time.sleep(0.5)
        logger.info("Start battle...")
        swipe_count = 0
        while 1:
            if not (self.wait_until_appear(self.I_AUTO_ROTATE_ON, 1)
                    or self.wait_until_appear(self.I_AUTO_ROTATE_OFF, 1)):
                logger.warning(
                    "***** Not inside chapter or battle finished.")
                raise RequestHumanTakeover

            # BOSS 挑战
            if self.appear(self.I_EXP_BOSS):
                time.sleep(1)
                self.appear_then_click(self.I_EXP_BOSS)

                if self.fight():
                    if self.wait_until_appear(
                        self.I_EXP_CHAPTER_DISMISS_ICON, 1
                    ) or self.appear(self.I_C_EXP, threshold=0.95):
                        return
                    else:
                        self.get_chapter_reward()
                        return
                else:
                    raise RequestHumanTakeover
            # 普通怪挑战
            if self.appear_then_click(self.I_EXP_BATTLE):
                self.fight()

            # 如果超过滑动次数
            elif swipe_count > 10:
                logger.error("Not able to find fight target")
                raise RequestHumanTakeover
            else:
                self.swipe(self.S_EXP_TO_RIGHT)
        time.sleep(0.5)

    def get_chapter_reward(self):
        logger.info("Trying to find chapter reward...")
        # 章节通关奖励，好像最多只有三个
        found = False
        time.sleep(2)
        for _ in range(3):
            if self.wait_until_appear(self.I_C_EXP, 1) or self.wait_until_appear(self.I_EXP_CHAPTER_DISMISS_ICON, 1):
                break

            if self.wait_until_click(self.I_EXP_CHAP_REWARD, 2, interval=0.5, wait_after=1):
                if self.wait_until_appear(self.I_EXP_GAIN_REWARD, 1):
                    self.random_click_right()
                    found = True
            else:
                break
        if found:
            logger.info("Got all chapter reward.")

    def fight(self) -> bool:
        # 等战斗结束
        time.sleep(3)

        # 领取战斗奖励，需要等动画
        if self.wait_until_appear(self.I_FIGHT_REWARD, 100, interval=0.5):
            time.sleep(0.5)
            self.random_click_right()
        else:
            logger.warning("!! Fight Failed !!")
            raise RequestHumanTakeover
        time.sleep(1)
        return True

    def check_ticket(self):
        if not self.exp_config.scroll_mode.scroll_mode_enable:
            return

        image = self.screenshot()
        count, total = self.O_EXP_VIEW_TICKET_COUNT.digit_counter(image)

        # 判断突破票数量
        if count is None or count < self.exp_config.scroll_mode.ticket_threshold:
            return

        self.activate_realm_raid()

    def activate_realm_raid(self):
        # 设置下次执行行时间
        logger.info("|| RealmRaid and Exploration set_next_run ||")
        hr, min, sec = self.exp_config.scroll_mode.scrolls_cd.split(":")
        next_run = datetime.now() + timedelta(hours=int(hr),
                                              minutes=int(min),
                                              seconds=int(sec))
        logger.warning(f"next run time: {next_run}")
        self.set_next_run(task='Exploration', success=False,
                          finish=False, target_time=next_run)
        self.set_next_run(task='RealmRaid', success=False,
                          finish=False, target_time=datetime.now())

        raise TaskEnd(self.name)
