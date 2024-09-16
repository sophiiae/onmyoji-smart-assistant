from pathlib import Path
import sys
from module.base.logger import logger
from module.config.config import Config
from module.server.connection import Connection

if __name__ == "__main__":
    # for screenshot
    if len(sys.argv) < 3:
        logger.error("Missing config name or save file name")
        logger.warning("Format: py .utils.py [config_name] [file_name]")
    else:
        name = sys.argv[1]
        file = sys.argv[2]

        config = Config(name)
        cn = Connection(config)
        filepath = Path.cwd() / f"{file}.png"
        cn.capture_screenshot(filepath)
