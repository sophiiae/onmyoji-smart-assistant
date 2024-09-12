import sys
from module.config.config import Config
from module.server.device import Device
from module.base.logger import logger
from tasks.shikigami_activity.task_script import TaskScript

def RunShikigamiActivity(name):
    c = Config(name)
    d = Device(c)
    a = TaskScript(c, d)
    logger.warning(f"Running Shikigami Activity for {c.model.config_name}")
    a.run()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        logger.error("Missing config name")
    else:
        name = sys.argv[1]
        RunShikigamiActivity(name)
