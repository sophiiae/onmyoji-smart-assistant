from module.config.function import Function


class ConfigState:
    """
    这个类用于 先定义运行过程中所需要的变量
    """

    def __init__(self, config_name: str) -> None:
        self.config_name = config_name
        self.pending_task: list["Function"] = []
        self.waiting_task: list["Function"] = []
        self.task: str = None  # 任务名大驼峰
