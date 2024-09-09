import json

from tqdm.contrib.concurrent import process_map
from pathlib import Path

MODULE_FOLDER = 'tasks'
ASSETS_FILE = 'assets.py'
ASSETS_CLASS = '\nclass Assets: \n'
IMPORT_EXP = """
from module.image_processing.rule_image import RuleImage
from module.image_processing.rule_ocr import RuleOcr
from module.image_processing.rule_swipe import RuleSwipe
from module.image_processing.rule_click import RuleClick

# This file was automatically generated by ./module/impage_processing/assets_extractor.py.
# Don't modify it manually.
"""
IMPORT_EXP = IMPORT_EXP.strip().split('MODULE_FOLDER') + ['']

def name_transform(name: str) -> str:
    """
    转换名称, 把小写的转化为大写的, 带有数字的不变，有下划线继续有下划线,
    如果是全部的大写就不管
    :param name: 任务名
    :return: 转换后的名称
    """
    if name.isupper():
        return name
    if name.islower():
        return name.upper()
    return name.upper()


class ImageExtractor:

    def __init__(self, file: str, data: list) -> None:
        """
        image rule 提取
        :param data:  json解析后的数据
        """
        # 这个时候的路径分隔符变成了 /
        self.file = str(Path(file).resolve().relative_to(
            (Path.cwd()).resolve()).as_posix())
        self.image_path = Path(self.file).parent.as_posix()

        self._result = '\n\t# Image Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        my_file = Path(item["file"])
        if item["file"] != "" and not my_file.is_file():
            print(f"Error: cannot find {item['name']} in {item['file']}")

        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tI_{name_transform(item["name"])} = RuleImage(\n' \
            f'\t\troi=({item["roi"]}),\n' \
            f'\t\tarea=({item["area"]}),\n' \
            f'\t\tfile="{item["file"]}"\n\t)\n'

        return description + name

class SwipeExtractor:

    def __init__(self, data: list) -> None:
        """
        swipe rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Swipe Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tS_{name_transform(item["name"])} = RuleSwipe(\n' \
            f'\t\troi_start=({item["roi_start"]}),\n' \
            f'\t\troi_end=({item["roi_end"]}),\n' \
            f'\t\tname="{item["name"]}"\n\t)\n'
        return description + name

class OcrExtractor:
    def __init__(self, data: list) -> None:
        """
        swipe rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\t# Ocr Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    @classmethod
    def extract_item(cls, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tO_{name_transform(item["name"])} = RuleOcr(\n' \
            f'\t\troi=({item["roi"]}),\n' \
            f'\t\tarea=({item["area"]}),\n' \
            f'\t\tkeyword="{item["keyword"]}",\n' \
            f'\t\tname="{item["name"]}"\n\t)\n'
        return description + name

class ClickExtractor:

    def __init__(self, data: list) -> None:
        """
        click rule 提取
        :param data:  json解析后的数据
        """
        self._result = '\n\n\t# Click Rule Assets\n'
        for item in data:
            self._result += self.extract_item(item)

    @property
    def result(self) -> str:
        return self._result

    def extract_item(self, item) -> str:
        """
        解析每一项，返回字符串
        :param item:
        :return:
        """
        description: str = f'\t# {item["description"]} \n'
        name: str = f'\tC_{name_transform(item["itemName"])} = RuleClick(' \
            f'roi=({item["roi"]}), ' \
            f'area=({item["area"]}), ' \
            f'name="{item["itemName"]}")\n'
        return description + name

class AssetsExtractor:
    def __init__(self, task_path: str) -> None:
        """
        assets 提取某个任务文件夹下的所以的资源
        :param task_name: 任务名
        """

        self.task_path = Path(task_path)
        self.task_name = self.task_path.name
        self.assets_file = self.task_path / ASSETS_FILE

        self.class_name = f'\nclass {
            self.titlize_class_name(self.task_name)}Assets: \n'

        self._result = ''
        for import_exp in IMPORT_EXP:
            self._result += import_exp
        self._result += self.class_name

    def titlize_class_name(self, name) -> str:
        words = [w.title() for w in name.split("_")]
        return "".join(words)

    def all_json_file(self) -> list:
        """
        获取所有json文件
        :return: json文件（带后缀）列表
        """
        return [str(x) for x in self.task_path.rglob('*.json') if 'temp' not in str(x)]

    @classmethod
    def read_file(cls, file: str) -> list:
        """
        读文件并随带解析
        :param file:
        :return:
        """
        with open(file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        if not isinstance(data, list) and not isinstance(data, dict):
            print(f'{file} 文件解析错误，不是list 或者 dict')
            return None
        return data

    def write_file(self) -> None:
        """
        将自身的_resule写入文件
        :return:
        """
        with open(self.assets_file, 'w', encoding='utf-8', newline='\n') as f:
            f.write(self._result)

    def extract(self):
        """
        生成一个assets.py文件
        :return:
        """
        result = ''
        for file in self.all_json_file():
            data = self.read_file(file)
            if not data:
                continue

            data_type = data[0]['type']
            if data_type == 'image':
                result += ImageExtractor(file, data).result
            elif data_type == 'text':
                result += OcrExtractor(data).result
            elif data_type == 'swipe':
                result += SwipeExtractor(data).result
            elif data_type == 'click':
                result += ClickExtractor(data).result

        if result == '':
            print(f'No resource files under the {self.task_name} task')
            self._result += '\tpass'
        else:
            self._result += result
        self._result += '\n\n'
        self.write_file()

class AllAssetsExtractor:
    def __init__(self):
        """
        获取./tasks目录下的所有任务文件夹,遍历每一个任务文件夹提取assets
        """
        print('** All assets extract')
        self.task_path = Path.cwd() / MODULE_FOLDER
        self.task_list = [
            x.name for x in self.task_path.iterdir() if x.is_dir()]
        self.task_paths = [str(x)
                           for x in self.task_path.iterdir() if x.is_dir()]

        process_map(self.work, self.task_paths, max_workers=1)

    @staticmethod
    def work(task_path: str):
        me = AssetsExtractor(task_path)
        me.extract()


if __name__ == "__main__":
    AllAssetsExtractor()
