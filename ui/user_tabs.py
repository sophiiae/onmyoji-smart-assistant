from typing import List

from flet import (
    Tab,
    Tabs,
)

from module.config.config_model import ConfigModel
from ui.user_setting_view import UseSettingView
from ui.statics import AppColors

class UserTabs(Tabs):
    def __init__(self, config_list: List[ConfigModel]):
        super().__init__()
        self.tabs = [
            Tab(
                text=config.config_name,
                content=UseSettingView(config=config),
            )
            for config in config_list
        ]
        self.selected_index = 0
        self.animation_duration = 300
        self.expand = 1
        self.label_color = AppColors.label_color
        self.indicator_color = AppColors.tab_indicator_color
