from datetime import datetime
import json
import os
from pathlib import Path
import re
from typing import List
from pydantic import BaseModel, Field
from module.base.logger import logger
from module.config.enums import *
from module.config.config_base import *

class ConfigModel(BaseModel):
    config_name: str = Field(default="osa")
    script: ScriptSetting = Field(default_factory=ScriptSetting)
    daily_routine: DailyRoutine = Field(
        default_factory=DailyRoutine)
    wanted_quests: WantedQuests = Field(
        default_factory=WantedQuests)
    exploration: Exploration = Field(
        default_factory=Exploration)
    realm_raid: RealmRaid = Field(default_factory=RealmRaid)
    goryou_realm: GoryouRealm = Field(
        default_factory=GoryouRealm)
    shikigami_activity: ShikigamiActivity = Field(
        default_factory=ShikigamiActivity)

    def __init__(self, config_name: str):
        data = self.read_json(config_name)
        data["config_name"] = config_name
        super().__init__(**data)

    def __setattr__(self, key, value):
        """
        只要修改属性就会触发这个函数 自动保存
        :param key:
        :param value:
        """
        super().__setattr__(key, value)
        print("auto save config")
        self.write_json(self.config_name)

    @staticmethod
    def read_json(config_name: str) -> dict:
        """
        :param config_name:  no ext
        :return: dict
        """
        file = Path.cwd() / "config" / f"{config_name}.json"

        if not os.path.exists(file):
            return {}

        with open(file, encoding='utf-8') as f:
            data = json.load(f)
            return data

    def write_json(self, config_name: str) -> None:
        """
        :param config_name: no ext
        :param data: dict
        :return:
        """
        filepath = Path.cwd() / "config" / f"{config_name}.json"
        data = self.model_dump()
        with open(filepath, 'w') as fp:
            json.dump(data, fp, indent=2, ensure_ascii=False)

    @staticmethod
    def type(key: str) -> str:
        """
        输入模型的键值，获取这个字段对象的类型 比如输入是orochi输出是Orochi
        :param key:
        :return:
        """
        field_type: str = str(ConfigModel.__annotations__[key])
        # return field_type
        if '.' in field_type:
            classname = field_type.split('.')[-1][:-2]
            return classname
        else:
            classname = re.findall(r"'([^']*)'", field_type)[0]
            return classname

    @staticmethod
    def deep_get(obj, keys: str, default=None):
        """
        递归获取模型的值
        :param obj:
        :param keys:
        :param default:
        :return:
        """
        if not isinstance(keys, list):
            keys = keys.split('.')
        value = obj
        try:
            for key in keys:
                value = getattr(value, key)
        except AttributeError:
            return default
        return value

    @staticmethod
    def deep_set(obj, keys: str, value) -> bool:
        if (isinstance(value, datetime)):
            value = value.strftime("%Y-%m-%d %H:%M:%S")

        if not isinstance(keys, list):
            keys = keys.split('.')
        current_obj = obj
        try:
            for key in keys[:-1]:
                current_obj = getattr(current_obj, key)
            setattr(current_obj, keys[-1], value)
            return True
        except (AttributeError, KeyError):
            return False

    def get_task(self, task: str):
        task = getattr(self, task, None)
        if task is None:
            return None
        return task.model_dump()

    def update(self, data: dict):
        update = self.model_dump()
        update.update(data)
        for k, v in self.model_validate(update).model_dump(exclude_defaults=True).items():
            print(f"updating value of '{k}' from '{
                  getattr(self, k, None)}' to '{v}'")
            setattr(self, k, v)
        return self

    def update_field(self, task, subtask, field, value):
        updated = False
        task_dict = getattr(self, task, None)
        if task_dict:
            sub = getattr(task_dict, subtask)
            if sub:
                setattr(sub, field, value)
                updated = True
        if updated:
            self.write_json(self.config_name)
