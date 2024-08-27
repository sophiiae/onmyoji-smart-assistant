from flet import (
    Container,
    Column,
    padding,
    margin,
    TextField,
    Text,
    TextThemeStyle,
    FontWeight,
)

from module.config.config_model import ConfigModel
from ui.statics import AppColors
from ui.task_setting import TaskSetting

class TaskView(Container):
    def __init__(self, setting_view, config: ConfigModel):
        super().__init__()
        self.setting_view = setting_view
        self.config = config
        self.bgcolor = AppColors.task_view_bgcolor
        self.border_radius = 10
        self.content = TaskSetting(
            config, "script", self.config.get_task("script"))
        self.padding = padding.all(15)
        self.margin = margin.symmetric(10, 0)
        self.is_isolated = True
        self.expand = True

    def set_task(self, task: str):
        if (task != ""):
            self.content = TaskSetting(
                self.config, task, self.config.get_task(task))
        self.update()
