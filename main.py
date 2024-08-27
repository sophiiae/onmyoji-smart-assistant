import flet as ft

from flet import ThemeMode, Theme

from module.config.config_model import ConfigModel
from module.config.config import *
from module.config.utils import get_json_files
from ui.user_tabs import UserTabs

def main(page: ft.Page):
    config_file_list = get_json_files()
    tabs_list = [
        ConfigModel(file_name) for file_name in config_file_list
    ]
    page.theme = Theme(font_family="source-hs")
    page.theme_mode = ThemeMode.LIGHT
    page.add(UserTabs(tabs_list))
    page.fonts = {"source-hs": "SourceHanSansSC-Normal.otf"}
    page.window_width = 500


ft.app(main, assets_dir="../assets")
