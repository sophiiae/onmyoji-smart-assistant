import sys
from module.config.config import Config
from module.server.device import Device
from tasks.general.summon import Summon
from tasks.realm_raid.guild_raid import GuildRaid

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


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Missing config name")
    else:
        name, t = sys.argv[1:]
        match t:
            case "-g":
                RunGuildRaid(name)
            case '-s':
                RunRegularSummon(name)
            case _:
                logger.error("Arg format: [script_name] [-g | -s]")
