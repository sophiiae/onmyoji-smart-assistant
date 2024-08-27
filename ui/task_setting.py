from typing import List
from enum import Enum

from flet import (
    Container,
    Column,
    TextField,
    TextThemeStyle,
    FontWeight,
    Text,
    Checkbox,
    Dropdown,
    dropdown,
    margin,
    ControlEvent
)

from module.config.config_model import ConfigModel
from module.config.enums import *

class TaskSetting(Container):
    task: str = ""
    subtask: str = ""
    label: str = ""

    def __init__(self, config: ConfigModel, task, task_settings):
        super().__init__()
        self.config = config
        self.task = task
        self.content = Column(
            controls=self.get_fields(task_settings),
            scroll=False if task == "wanted_quests" else True,
            expand=True
        )
        self.margin = margin.only(left=20)

    def get_fields(self, settings: List):
        controls = []
        for key in settings:
            controls.append(
                Text(key, theme_style=TextThemeStyle.TITLE_MEDIUM, weight=FontWeight.W_700))
            subtask = settings[key]
            for label in subtask:
                component = self.get_component_by_type(
                    key, label, subtask[label])
                if component:
                    controls.append(component)
        return controls

    def handle_checkbox_change(self, e: ControlEvent):
        print(e.data)
        # data = True if e.data == 'true' else False
        # self.config.update_field(
        #     self.task, self.subtask, self.label, data)

    def get_component_by_type(self, subtask, label, value):
        if isinstance(value, bool):
            self.subtask = subtask
            self.label = label
            return Checkbox(label=label, value=value, on_change=self.handle_checkbox_change)
        elif isinstance(value, Enum):
            self.subtask = subtask
            self.label = label
            return self.get_enum_component(subtask, label, value)
        elif isinstance(value, str) or isinstance(value, (int, float)):
            self.subtask = subtask
            self.label = label
            return TextField(label=label, value=value)
        return None

    # todo: find a good way save dropdown changes
    def handle_dropdown_change(self, e: ControlEvent):
        print(e.data)
        # print(self.type.value)
        # self.config.update_field(
        #     self.task, self.subtask, self.label, e.data)

    def get_enum_component(self, subtask, label, value):
        self.label = label
        self.subtask = subtask

        options = []
        if isinstance(value, Chapters):
            options = [e.value for e in Chapters]
        elif isinstance(value, ChooseRarity):
            options = [e.value for e in ChooseRarity]
        elif isinstance(value, WantedQuestType):
            options = [e.value for e in WantedQuestType]
        elif isinstance(value, GoryouClass):
            options = [e.value for e in GoryouClass]
        elif isinstance(value, GoryouLevel):
            options = [e.value for e in GoryouLevel]
        elif isinstance(value, ScreenshotMethod):
            options = [e.value for e in ScreenshotMethod]
        elif isinstance(value, ControlMethod):
            options = [e.value for e in ControlMethod]
        elif isinstance(value, ErrorHandleMethod):
            options = [e.value for e in ErrorHandleMethod]

        return Dropdown(
            options=[dropdown.Option(val) for val in options],
            label=label,
            value=value.value,
            on_change=self.handle_dropdown_change
        )
