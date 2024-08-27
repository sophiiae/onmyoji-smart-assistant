from flet import (
    TextButton,
    Text,
)

from ui.zh import ZH_LABELS

class TaskButton(TextButton):
    task: str = ''

    def __init__(self, setting_view, task: str):
        super().__init__()
        self.setting_view = setting_view
        self.is_selected = True
        self.task = task
        self.on_click = self.toggle_select
        self.content = Text(
            value=ZH_LABELS[task],
            font_family={"source-hs"},
        )

    def toggle_select(self, e):
        self.setting_view.task_view.set_task(self.task)
