
from module.config.config_model import ConfigModel
from datetime import datetime

import logging
logger = logging.getLogger(__name__)

DEFAULT_TIME = datetime(2024, 1, 1, 0, 0)

class Function:
    enable = False
    priority = 0

    def __init__(self, key: str, data: dict):
        """
        输入的是每一个ConfigModel的一个字段对象
        :param data:
        """
        if isinstance(data, dict) is False:
            self.enable = False
            self.name = "Unknown"
            self.next_run = DEFAULT_TIME
            return
        if data.get("scheduler") is None:
            self.enable = False
            self.name = "Unknown"
            self.next_run = DEFAULT_TIME
            return

        self.setting = data

        self.enable: bool = data['scheduler']['enable']
        self.name: str = ConfigModel.type(key)

        next_run = data['scheduler']['next_run']
        if isinstance(next_run, str):
            next_run = datetime.strptime(next_run, "%Y-%m-%d %H:%M:%S")
        self.next_run: datetime = next_run

        priority = data['scheduler']['priority']
        if isinstance(priority, str):
            priority = int(priority)
        self.priority: int = priority
        if not isinstance(self.priority, int):
            logger.error(f"Invalid priority: {self.priority}")

    def __str__(self):
        enable = "Enable" if self.enable else "Disable"
        return f"{self.name} ({enable}, {self.priority}, {str(self.next_run)})"

    __repr__ = __str__

    def __eq__(self, other):
        if not isinstance(other, Function):
            return False

        if self.name == other.name and self.next_run == other.next_run:
            return True
        else:
            return False
