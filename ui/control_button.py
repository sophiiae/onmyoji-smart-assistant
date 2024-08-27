from flet import (
    Container,
    Row,
    padding,
    margin,
    IconButton,
    icons,
    TextButton,
    MainAxisAlignment,
    border,
    ControlEvent,
)

from module.config.config_model import ConfigModel
from module.server.process_manager import ProcessManager
from ui.statics import AppColors
from ui.zh import ZH_LABELS

class ControlButton(Container):
    pm: ProcessManager = None

    def __init__(self, pm: ProcessManager, config: ConfigModel):
        super().__init__()
        self.pm = pm
        self.text_button = TextButton(text=ZH_LABELS.get("control_button"))
        self.control_button = IconButton(icon=icons.CIRCLE,
                                         icon_color=AppColors.circle_deactivate_color,
                                         on_click=self.toggle_control,
                                         selected=False,
                                         selected_icon=icons.CIRCLE,
                                         selected_icon_color=AppColors.circle_activate_color
                                         )
        self.content = Row(
            controls=[self.text_button, self.control_button],
            alignment=MainAxisAlignment.CENTER
        )
        self.margin = margin.symmetric(10, 0)
        self.padding = padding.only(bottom=10)
        self.border = border.only(
            bottom=border.BorderSide(
                1, color=AppColors.horizontal_divider_color)
        )
        self.is_isolated = True

    def toggle_control(self, e: ControlEvent):
        self.control_button.selected = not self.control_button.selected
        if self.control_button.selected:
            self.pm.start_processing()
        else:
            self.pm.stop_processing()
        e.control.update()
