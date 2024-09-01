import sys
from module.config.config import Config
from module.server.device import Device
from tasks.general.summon import Summon
from tasks.realm_raid.guild_raid import GuildRaid
from tasks.exploration.colla import Colla
from tasks.realm_raid.task_script import TaskScript

from module.base.logger import logger

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

def RunThreeWindRealmRaid(config_name: str):
    logger.info(f"Start running 3 win realm raid for script: {config_name}")

    c = Config(config_name)
    d = Device(c)
    rr = TaskScript(c, d)
    rr.run_three_win()


if __name__ == "__main__":
    if len(sys.argv) < 3:
        logger.error("Missing config name")
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
            case 'help':
                logger.warning("Args[0]: config name")
                logger.warning(
                    "Args[1]: -g: run guild raid | -r: run 3 win realm raid")
                logger.warning(
                    "Agrs[1]: -s: run regular summon | -c: run daily collaboration")
            case _:
                logger.warning("Missing args, try 'help' for instruction")