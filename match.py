import json
from pathlib import Path
import sys
from module.base.logger import logger
from module.config.config import Config
from module.image_processing.image_processor import ImageProcessor
from module.server.connection import Connection

if __name__ == "__main__":
    # match target
    if len(sys.argv) < 3:
        logger.error("Missing config name or save file name")
        logger.warning("Format: py .utils.py [config_name] [file_name]")
    else:
        name = sys.argv[1]
        target = sys.argv[2]

    name = sys.argv[1]
    config = Config(name)
    cn = Connection(config)
    screenshot = cn.get_screenshot()
    pro = ImageProcessor(screenshot)
    result = pro.parse_image_file(target)
    print(json.dumps(result))
    pro.write_output(f"output")
