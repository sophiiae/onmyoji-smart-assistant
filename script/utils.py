import importlib
import sys


def load_module(moduleName: str, moduleFile: str):
    """
    加载模块
    :param moduleName:
    :param moduleFile: 文件路径带py
    :return:
    """
    spec = importlib.util.spec_from_file_location(moduleName, moduleFile)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    sys.modules[moduleName] = module
    return module
