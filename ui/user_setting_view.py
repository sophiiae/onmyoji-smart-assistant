from flet import (
    Container,
    Row,
)

from module.config.config_model import ConfigModel
from ui.sidebar import Sidebar
from ui.task_view import TaskView

class UseSettingView(Container):
    def __init__(self, config: ConfigModel):
        super().__init__()
        self.sidebar = Sidebar(self, config)
        self.task_view = TaskView(
            self, config)
        self.content = Row(
            controls=[self.sidebar, self.task_view],
            spacing=10,
            expand=True
        )
        self.expand = True
        self.is_isolated = True
