import sys
import time
from module.config.config import Config
from module.server.device import Device
from module.base.logger import logger
from tasks.general.summon import Summon
from tasks.realm_raid.guild_raid import GuildRaid
from tasks.main_page.colla import Colla
from tasks.realm_raid.task_script import TaskScript as RR
from tasks.minamoto.task_script import TaskScript as MINAMOTO
from tasks.task_base import TaskBase
from tasks.general.page import Page, page_minamoto, page_main
from tasks.main_page.routine import Routine


def RunRegularSummon(config_name: str):
    logger.info(f"Start running regualr summon for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    s = Summon(c, d)
    s.run()

def RunGuildRaid(config_name: str):
    logger.info(f"Start running regualr summon for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    g = GuildRaid(c, d)
    g.start_guild_raid()

def RunColla(config_name: str):
    logger.info(f"Start running regualr summon for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    colla = Colla(c, d)
    colla.start_colla()

def RunDailyRountine(name):
    c = Config(name)
    d = Device(c)
    r = Routine(c, d)
    r.run()
    # r.run_single_account()
    # r.quest_invite()

def RunThreeWindRealmRaid(config_name: str):
    logger.info(f"Start running 3 win realm raid for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    rr = RR(c, d)
    rr.run_three_win()

def RunMinamoto(config_name: str):
    logger.info(f"Start running minamoto for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    minamoto = MINAMOTO(c, d)
    minamoto.run()
    # minamoto.goto(page_minamoto)
    # minamoto.goto(page_main, page_minamoto)

def WaitingMode(name: str):
    c = Config(name)
    d = Device(c)
    b = TaskBase(c, d)
    count = 0
    while count < 3:
        time.sleep(1)
        if b.wait_request():
            count += 1


if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.warning("Args[0]: config name")
        logger.warning(
            "Args[1]: -g: run guild raid | -r: run 3 win realm raid")
        logger.warning(
            "Agrs[1]: -s: run regular summon | -c: run daily collaboration")
        logger.warning(
            "Agrs[1]: -m: run minamoto | -w: wating model | -d: daily routine(colla)")
    else:
        name, t = sys.argv[1:]
        match t:
            case '-g':
                RunGuildRaid(name)
            case '-s':
                RunRegularSummon(name)
            case '-c':
                RunColla(name)
            case '-r':
                RunThreeWindRealmRaid(name)
            case '-m':
                RunMinamoto(name)
            case '-w':
                WaitingMode(name)
            case '-d':
                RunDailyRountine(name)
            case _:
                logger.warning("Missing args, try 'help' for instruction")
