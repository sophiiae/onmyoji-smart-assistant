
import sys
from module.base.logger import logger
from module.base.exception import RequestHumanTakeover, TaskEnd
from module.config.enums import BuffClass
from tasks.battle.battle import Battle
from tasks.exploration.assets import ExplorationAssets as EA
from tasks.general.page import Page, page_exp, page_main

from datetime import datetime, timedelta
import time

class TaskScript(EA, Battle):
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

        self.open_config_buff()
        count = 0
        while exp_count > 0 and count < exp_count:
            # 检查票数
            self.check_ticket()

            if self.wait_until_click(self.I_EXP_CHAPTER_28):
                self.wait_until_click(self.I_EXP_BUTTON)

            logger.info(f"======== Round {count + 1} Exp Started =========")
            # 进入章节战斗
            self.battle_process()

            # 如果回到了探索界面 -> 检查宝箱
            if self.wait_until_appear(self.I_C_EXP, 2):
                self.check_treasure_box()
            else:
                # 出现章节入口 -> 没有发现 -> 关闭
                self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 2)

            count += 1

        # 关闭章节探索提示
        self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 2)

        self.close_config_buff()
        self.goto(page_main, page_exp)
        self.set_next_run(task='Exploration', success=True, finish=False)

        raise TaskEnd(self.name)

    def check_treasure_box(self):
        time.sleep(1)
        if self.wait_until_click(
            self.I_EXP_TREASURE_BOX_MAP,
            threshold=0.95
        ):
            got_reward = self.wait_until_appear(
                self.I_REWARD, 3)
            if got_reward:   # 领取宝箱物品
                time.sleep(0.7)
                self.random_click_right()

    def battle_process(self):
        # ************************* 进入设置并操作 *******************
        # 自动轮换功能打开
        while 1:
            self.screenshot()
            # 自动轮换开着 则跳过
            if self.appear(self.I_AUTO_ROTATE_ON):
                break
            # 自动轮换关着 则打开
            if self.appear_then_click(self.I_AUTO_ROTATE_OFF):
                if self.appear(self.I_AUTO_ROTATE_ON):
                    break

        # 进入战斗环节
        logger.info("Start battle...")
        while 1:
            if not self.wait_until_appear(self.I_EXP_C_CHAPTER, 1.5):
                logger.warning(
                    "***** Not inside chapter or battle finished.")
                raise RequestHumanTakeover

            # BOSS 挑战
            if self.appear(self.I_EXP_BOSS):
                time.sleep(0.6)
                self.appear_then_click(self.I_EXP_BOSS)

                if self.run_battle():
                    self.get_chapter_reward()
                    break

            # 普通怪挑战
            if self.appear_then_click(self.I_EXP_BATTLE):
                self.run_battle()

            else:
                self.swipe(self.S_EXP_TO_RIGHT)

            time.sleep(0.3)

        time.sleep(1)

    def get_chapter_reward(self):
        logger.info("Trying to find chapter reward...")
        # 章节通关奖励，好像最多只有三个
        found = False
        time.sleep(1)
        while 1:
            time.sleep(0.3)
            if self.appear(self.I_C_EXP) or self.appear(self.I_C_EXP_MODAL):
                break

            if self.wait_until_click(self.I_EXP_CHAP_REWARD):
                if self.appear(self.I_GAIN_REWARD):
                    self.random_click_right()
                    found = True

        if found:
            logger.info("Got all chapter reward.")
        return found

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

    def open_config_buff(self):
        buff = []
        config = self.exp_config.exploration_config
        if config.buff_gold_50:
            buff.append(BuffClass.GOLD_50)
        if config.buff_gold_100:
            buff.append(BuffClass.GOLD_100)
        if config.buff_exp_50:
            buff.append(BuffClass.EXP_50)
        if config.buff_exp_100:
            buff.append(BuffClass.EXP_100)

        return self.check_buff(buff, page_exp)

    def close_config_buff(self):
        buff = []
        config = self.exp_config.exploration_config
        if config.buff_gold_50:
            buff.append(BuffClass.GOLD_50_CLOSE)
        if config.buff_gold_100:
            buff.append(BuffClass.GOLD_100_CLOSE)
        if config.buff_exp_50:
            buff.append(BuffClass.EXP_50_CLOSE)
        if config.buff_exp_100:
            buff.append(BuffClass.EXP_100_CLOSE)

        return self.check_buff(buff, page_exp)
