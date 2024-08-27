import time
from module.base.logger import logger
from module.base.exception import GamePageUnknownError
from module.base.timer import Timer
from module.image_processing.rule_image import RuleImage
from tasks.general.assets import GeneralAssets
from tasks.general.page import *
from tasks.main_page.assets import MainPageAssets
from tasks.task_base import TaskBase

class General(TaskBase, GeneralAssets):
    ui_current: Page = None
    ui_pages = [
        page_main, page_summon, page_exp,
        page_realm_raid, page_guild_raid, page_store, page_login, page_sleep
    ]
    ui_close = [
        GeneralAssets.I_V_EXP_TO_MAIN, GeneralAssets.I_V_GUILD_TO_MAIN,
        GeneralAssets.I_V_STORE_TO_MAIN, GeneralAssets.I_V_REALM_RAID_TO_EXP,
        MainPageAssets.I_STORE_EXIT, GeneralAssets.I_V_SLEEP_TO_MAIN
    ]

    def main_to_exp(self) -> bool:
        while 1:
            self.screenshot()
            if self.appear_then_click(self.I_V_MAIN_TO_EXP, interval=2):
                continue
            if self.appear(self.I_C_EXP):
                break

            print(self.appear(self.I_C_EXP))
        logger.info(f'## Click {self.I_V_MAIN_TO_EXP.name}')
        return True

    def exp_to_home(self) -> bool:
        while 1:
            self.screenshot()
            if self.appear_then_click(self.I_V_EXP_TO_MAIN, interval=2):
                continue
            if self.appear(self.I_C_MAIN_GATE):
                break
        logger.info(f'## Click {self.I_V_EXP_TO_MAIN.name}')
        return True

    def check_page_appear(self, page):
        """
        判断当前页面是否为page
        """
        return self.appear(page.check_button)

    def is_scroll_closed(self):
        """
        判断庭院界面卷轴是否打开
        """
        return self.appear(MainPageAssets.I_SCROLL_CLOSE)

    def is_button_executed(self, button):
        """
        确保button执行
        """
        if isinstance(button, RuleImage) and self.appear(button):
            return True
        elif callable(button) and button():
            return True
        else:
            return False

    def get_current_page(self, skip_first_screenshot=True) -> Page:
        timeout = Timer(10, count=20).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
                if not hasattr(self.device, "image") or self.device.image is None:
                    self.screenshot()
            else:
                self.screenshot()

            # 如果20S还没有到底，那么就抛出异常
            if timeout.reached():
                break

            # Known pages
            for page in self.ui_pages:
                if page.check_button is None:
                    continue
                if self.check_page_appear(page=page):
                    logger.info(f"[UI]: {page.name}")
                    self.ui_current = page
                    if page == page_main and self.is_scroll_closed():
                        logger.warning("[UI]: main page scroll closed")
                        self.click_until_disappear(
                            MainPageAssets.I_SCROLL_CLOSE)
                    return page

            # Try to close unknown page
            for close in self.ui_close:
                if self.appear_then_click(close, interval=1.5):
                    logger.warning('Trying to switch to supported page')
                    timeout = Timer(10, count=10).start()

        logger.critical("Starting from current page is not supported")
        raise GamePageUnknownError

    def goto(self, destination: Page, confirm_wait=0, skip_first_screenshot=True):
        # Reset connection
        for page in self.ui_pages:
            page.parent = None

        # Create connection
        visited = [destination]
        visited = set(visited)
        # 广度优先搜索
        while 1:
            new = visited.copy()
            for page in visited:
                for link in self.ui_pages:
                    if link in visited:
                        continue
                    if page in link.links:
                        link.parent = page
                        new.add(link)
            # 没有新的页面加入，说明已经遍历完毕
            if len(new) == len(visited):
                break
            visited = new
        logger.info(f"[UI goto]: {destination}")
        confirm_timer = Timer(confirm_wait, count=int(
            confirm_wait // 0.5)).start()
        while 1:
            if skip_first_screenshot:
                skip_first_screenshot = False
            else:
                self.screenshot()

            # Destination page
            if self.wait_until_appear(destination.check_button):
                if confirm_timer.reached():
                    logger.info(f'[UI] Page arrive: {destination}')
                    break
            else:
                confirm_timer.reset()

            # Other pages
            clicked = False
            for page in visited:
                if page.parent is None or page.check_button is None:
                    continue

                # 获取当前页面的要点击的按钮
                if self.appear(page.check_button, interval=4):
                    logger.info(f'[UI] Page switch: {page} -> {page.parent}')
                    button = page.links[page.parent]
                    if self.appear_then_click(button, interval=2):
                        confirm_timer.reset()
                        clicked = True
                        break

            if clicked:
                continue

        # Reset connection
        for page in self.ui_pages:
            page.parent = None

        time.sleep(1)


if __name__ == '__main__':
    from pathlib import Path
    import sys
    sys.path.append(str(Path(__file__).parent.parent.parent))
    from module.config.config_model import ConfigModel
    from module.server.device import Device

    config = ConfigModel('osa')
    device = Device(config)

    game = General(config, device)
    game.screenshot()
    print(game.appear(game.I_V_SLEEP_TO_MAIN))
    print(game.exp_to_home())
    game.goto(page_summon)
