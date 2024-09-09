
from collections import deque
from module.base.exception import GameNotRunningError, GameStuckError, GameTooManyClickError
from module.base.logger import logger
from module.base.timer import Timer
from module.config.config import Config
from module.server.connection import Connection

class Device:
    device = None
    cnn: Connection = None
    config: Config
    image = None
    detect_record = set()
    click_record = deque(maxlen=15)
    stuck_timer = Timer(60, retry_max=60).start()
    stuck_timer_long = Timer(300, retry_max=300).start()
    stuck_long_wait_list = ['BATTLE_STATUS_S', 'PAUSE', 'LOGIN_CHECK']

    def __init__(self, config: Config):
        self.config = config
        self.cnn = Connection(config)
        self.device = self.cnn.device
        logger.warning(f"We are running script for {config.model.config_name}")

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

    def stuck_record_add(self, button):
        """
        当你要设置这个时候检测为长时间的时候，你需要在这里添加
        如果取消后，需要在`stuck_record_clear`中清除
        :param button:
        :return:
        """
        self.detect_record.add(str(button))
        logger.info(f'Add stuck record: {button}')

    def stuck_record_clear(self):
        self.detect_record = set()
        self.stuck_timer.reset()
        self.stuck_timer_long.reset()

    def stuck_record_check(self):
        """
        Raises:
            GameStuckError:
        """
        reached = self.stuck_timer.reached()
        reached_long = self.stuck_timer_long.reached()

        if not reached:
            return False
        if not reached_long:
            for button in self.stuck_long_wait_list:
                if button in self.detect_record:
                    return False

        logger.warning('Wait too long')
        logger.warning(f'Waiting for {self.detect_record}')
        self.stuck_record_clear()

        if self.app_is_running():
            raise GameStuckError(f'Wait too long')
        else:
            raise GameNotRunningError('Game died')

    def handle_control_check(self, button):
        self.stuck_record_clear()
        self.click_record_add(button)
        self.click_record_check()

    def click_record_add(self, button):
        self.click_record.append(str(button))

    def click_record_clear(self):
        self.click_record.clear()

    def click_record_remove(self, button):
        """
        Remove a button from `click_record`

        Args:
            button (Button):

        Returns:
            int: Number of button removed
        """
        removed = 0
        for _ in range(self.click_record.maxlen):
            try:
                self.click_record.remove(str(button))
                removed += 1
            except ValueError:
                # Value not in queue
                break

        return removed

    def click_record_check(self):
        """
        Raises:
            GameTooManyClickError:
        """
        count = {}
        for key in self.click_record:
            count[key] = count.get(key, 0) + 1
        count = sorted(count.items(), key=lambda item: item[1])
        if count[0][1] >= 12:
            logger.warning(f'Too many click for a button: {count[0][0]}')
            logger.warning(f'History click: {
                           [str(prev) for prev in self.click_record]}')
            self.click_record_clear()
            raise GameTooManyClickError(
                f'Too many click for a button: {count[0][0]}')
        if len(count) >= 2 and count[0][1] >= 6 and count[1][1] >= 6:
            logger.warning(f'Too many click between 2 buttons: {
                           count[0][0]}, {count[1][0]}')
            logger.warning(f'History click: {
                           [str(prev) for prev in self.click_record]}')
            self.click_record_clear()
            raise GameTooManyClickError(f'Too many click between 2 buttons: {
                                        count[0][0]}, {count[1][0]}')
