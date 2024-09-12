import time
from tasks.general.page import page_summon, page_main
from tasks.general.general import General
from module.base.logger import logger

class Summon(General):

    def run(self):
        if not self.check_page_appear(page_summon):
            self.goto(page_summon)

        image = self.screenshot()
        ticket = self.O_REG_SUMMON_TICKET.digit(image)
        if ticket < 10:
            print("No enough ticket to summon")

        if self.wait_until_appear(self.I_REG_SUMMON, 2, 1):
            self.click(self.I_REG_SUMMON)

        time.sleep(3)

        r = (ticket - 10) // 10
        for i in range(r):
            logger.info(f"Summon round {i + 1}")
            if not self.wait_until_appear(self.I_SUMMON_AGAIN, 10, 1, click=True, click_delay=3):
                break
        self.goto(page_main, page_summon)
        exit()
