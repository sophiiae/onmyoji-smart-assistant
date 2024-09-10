import time
from module.base.exception import RequestHumanTakeover
from tasks.exploration.task_script import TaskScript as EXP
from tasks.general.page import page_exp, page_main
from module.base.logger import logger


class Colla(EXP):

    def start_colla(self):
        # 进入探索页面
        if not self.check_page_appear(page_exp):
            self.goto(page_exp)

        fight_count = 0
        while fight_count < 10:
            self.click(self.I_EXP_CHAPTER_28)

            fight_count = self.colla_enter_chapter(fight_count)

            if fight_count > 9:
                break

            # 如果回到了探索界面 -> 检查宝箱
            if self.wait_until_appear(self.I_C_EXP, 5):
                self.check_treasure_box()
            else:
                # 出现章节入口 -> 没有发现 -> 关闭
                self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 1)

        if self.wait_until_appear(self.I_AUTO_ROTATE_ON, 1) or self.wait_until_appear(self.I_AUTO_ROTATE_OFF, 1):
            self.appear_then_click(self.I_B_BLUE_LEFT_ANGLE)
            time.sleep(0.3)
            if not self.wait_until_click(self.I_EXP_CHAPTER_EXIT_CONFIRM):
                logger.critical("Not able to exit chapter")
                exit()
            # 关闭章节探索提示
            self.wait_until_click(self.I_EXP_CHAPTER_DISMISS_ICON, 2)

        self.goto(page_main)

    def colla_enter_chapter(self, c) -> int:
        # 点击 “探索” 按钮进入章节
        if not self.wait_until_appear(self.I_EXP_BUTTON):
            logger.error("Cannot find chapter exploration button")
            raise RequestHumanTakeover

        self.click(self.I_EXP_BUTTON)
        time.sleep(0.5)
        logger.info("Start battle...")
        while 1:
            if c > 9:
                break

            if not self.wait_until_appear(self.I_EXP_C_CHAPTER, 1.5):
                logger.warning(
                    "***** Not inside chapter or battle finished.")
                raise RequestHumanTakeover

            # BOSS 挑战
            if self.appear(self.I_EXP_BOSS):
                time.sleep(0.6)
                self.appear_then_click(self.I_EXP_BOSS)

                if self.run_battle():
                    c += 1
                    self.get_chapter_reward()
                    break
            # 普通怪挑战
            if self.appear_then_click(self.I_EXP_BATTLE):
                c += 1
                self.run_battle()

            else:
                self.swipe(self.S_EXP_TO_RIGHT)

            time.sleep(0.3)

        return c
