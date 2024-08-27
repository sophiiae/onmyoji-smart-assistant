
from module.base.logger import logger
from module.config.config import Config
from module.server.connection import Connection

class Device:
    device = None
    cnn: Connection = None
    config: Config
    image = None

    def __init__(self, config: Config):
        self.config = config
        self.cnn = Connection(config)
        self.device = self.cnn.device

    def screenshot(self):
        """
        Returns:
            np.ndarray:
        """
        self.image = self.cnn.get_screenshot()
        return self.image

    def click(self, x, y):
        logger.info(f"[Device] Click {x} {y}.")
        self.device.shell("input tap {} {}".format(x, y))

    def swipe(self, start_x, start_y, end_x, end_y, duration=300):
        logger.info(f"[Device] Swipe from ({start_x},{start_y}) to ({
            end_x},{end_y}) in {duration}.")
        self.device.shell("input swipe {} {} {} {} {}".format(
            start_x,
            start_y,
            end_x,
            end_y,
            duration
        ))

    def stop_app(self, package_name=None):
        """ Stop one application: am force-stop"""
        self.device.shell(f"am force-stop {package_name}")
