import time
from module.base.logger import logger
from module.base.exception import GamePageUnknownError
from module.base.timer import Timer
from module.image_processing.rule_image import RuleImage
from tasks.general.assets import GeneralAssets
from tasks.general.page import *
from tasks.general.page_map import PageMap
from tasks.main_page.assets import MainPageAssets
from tasks.exploration.assets import ExplorationAssets
from tasks.task_base import TaskBase

class General(TaskBase, GeneralAssets, PageMap):
    ui_current: Page = None
    ui_close = [
        GeneralAssets.I_V_EXP_TO_MAIN, GeneralAssets.I_V_GUILD_TO_MAIN,
        GeneralAssets.I_V_STORE_TO_MAIN, GeneralAssets.I_V_REALM_RAID_TO_EXP,
        MainPageAssets.I_STORE_EXIT, GeneralAssets.I_V_SLEEP_TO_MAIN,
        ExplorationAssets.I_EXP_CHAPTER_DISMISS_ICON
    ]

    def check_page_appear(self, page, check_delay: float = 0.01):
        """
        判断当前页面是否为page
        """
        time.sleep(check_delay)
        if not self.appear(page.check_button, threshold=0.90):
            logger.error(f"Not in {page.name} page")
            return False
        return True

    def is_scroll_closed(self):
        """
        判断庭院界面卷轴是否打开
        """
        return self.appear(MainPageAssets.I_SCROLL_CLOSE)

    def get_current_page(self) -> Page:
        timeout = Timer(5, 20).start()
        logger.info("Getting current page")

        while 1:
            self.screenshot()

            # 如果20S还没有到底，那么就抛出异常
            if timeout.reached():
                break

            for page in self.MAP.keys():
                if page.check_button is None:
                    continue
                if self.check_page_appear(page=page):
                    logger.info(f"[UI]: {page.name}")
                    self.ui_current = page
                    return page

            # Try to close unknown page
            for close in self.ui_close:
                if self.wait_until_appear(close, waiting_limit=0, retry_limit=0, click=True):
                    logger.warning('Trying to switch to supported page')
                    timeout = Timer(5, 10).start()
                time.sleep(0.2)
        logger.critical("Starting from current page is not supported")
        raise GamePageUnknownError

    def goto(self, destination: Page, waiting_limit=0):
        self.get_current_page()
        path = self.find_path(self.ui_current, destination)

        logger.info(f"[PATH] Start following the path: {
                    [p.name for p in path]}")

        for idx, page in enumerate(path):
            if self.check_page_appear(page, check_delay=0.3):
                logger.info(f"[UI] We are in page: {page.name}")

            # 已经到达页面，退出
            if page == destination:
                logger.info(f'[UI] Page arrive: {destination}')
                time.sleep(0.5)
                return

            # 路径/页面设置 出错
            if not self.wait_until_appear(page.check_button, 3):
                logger.error(f"[PATH] Current page not match page {page.name}")
                return

            goto_timer = Timer(waiting_limit, int(
                waiting_limit // 2)).start()

            while 1:
                self.screenshot()
                if page.check_button is None:
                    logger.error(
                        f"[PATH] Not able to find check_button for page {page.name}")
                    return

                print(page.name)
                button = page.links[path[idx + 1]]
                if self.wait_until_appear(button, click=True):
                    logger.info(f"[PATH] Heading from {
                                page.name} to {path[idx + 1].name}.")
                    time.sleep(0.2)
                    break

                if goto_timer.reached():
                    logger.error(f"[PATH] {page.name} is not reachable.")
                    return


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
