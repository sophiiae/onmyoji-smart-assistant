from typing import List
from flet import (
    Container,
    Column,
    padding,
    margin,
    colors,
    alignment,
)

from module.config.config_model import ConfigModel
from module.server.process_manager import ProcessManager
from ui.control_button import ControlButton
from ui.statics import AppColors
from ui.task_button import TaskButton

class Sidebar(Container):
    def __init__(self, setting_view, config: ConfigModel):
        super().__init__()
        self.setting_view = setting_view
        self.config = config
        self.padding = padding.all(15)
        self.margin = margin.symmetric(10, 0)
        self.width = 140
        self.bgcolor = AppColors.sidebar_bgcolor
        self.border_radius = 10
        self.alignment = alignment.center
        process_manager = ProcessManager(config=config)
        self.pm = process_manager
        self.content = self.sidebar_list(process_manager)

    def sidebar_list(self, pm) -> Column:
        self.buttons = [TaskButton(self.setting_view, field)
                        for field in self.config.model_fields
                        if field != "config_name"]
        self.buttons.insert(0, ControlButton(pm, self.config))
        list = Column(
            controls=self.buttons,
            spacing=3,
        )
        return list
