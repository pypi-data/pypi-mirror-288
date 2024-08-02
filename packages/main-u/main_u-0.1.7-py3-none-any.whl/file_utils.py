#!/usr/bin/env python
# coding=utf-8

import json, yaml, xlrd, csv
from abc import ABCMeta, abstractmethod
from typing import Dict, List, Tuple, Union
from openpyxl import workbook


class FileUtils(metaclass=ABCMeta):
    @abstractmethod
    def read(self, file_path: str):
        """
        抽象方法，用于读取文件
        :param file_path: 文件路径
        :return: 文件内容，可能是字符串或字节数组
        """
        pass

    @abstractmethod
    def write(self, file_path: str, content: Union[List, Dict, Tuple, str, bytes], mode: str = 'w'):
        """
        抽象方法，用于写入文件
        :param file_path: 文件路径
        :param content: 要写入的内容，可以是列表、字典、元组、字符串或字节数组
        :param mode: 写入模式，默认为'w'，表示覆盖写入
        """
        pass

class JsonFileUtils(FileUtils):
    def read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def write(self, file_path, content: Dict, mode='w'):
        """
        将内容写入json文件

        Args:
            file_path (str): 文件路径
            content (Dict): 要写入的内容
            mode (str, optional): 写入模式，默认为'w'，表示覆盖写入. Defaults to 'w'.
        """
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=4, ensure_ascii=False)

class YamlFileUtils(FileUtils):
    def read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def write(self, file_path, content: Union[Dict, List, Tuple, str], mode='w'):
        """
        将数据写入到yaml文件中

        Args:
            file_path: 文件路径
            content: 要写入的数据，可以是字典、列表、元组等
            mode: 写入模式，默认为'w'
        """
        with open(file_path, mode=mode, encoding='utf-8') as f:
            yaml.dump(content, f, allow_unicode=True)  # 写入的中文不进行转码

class ExcelFileUtils(FileUtils):
    def read(self, file_path):
        with xlrd.open_workbook(file_path) as f:
            sheet = f.sheet_by_index(0)
            rows = sheet.nrows
            cols = sheet.ncols
            data = []
            for row in range(rows):
                row_data = []
                for col in range(cols):
                    row_data.append(sheet.cell_value(row, col))
                data.append(row_data)
            return data

            

    def write(self, file_path, content: list[list]):
        """
        将数据写入 Excel 文件

        Args:
            file_path (str): 文件保存路径     
            content (list[list]): 要写入的数据，二维列表
        """
        wb = workbook.Workbook()
        sheet = wb.active

        for row, row_data in enumerate(content):
            for col, value in enumerate(row_data):
                sheet.cell(row=row + 1, column=col + 1, value=value)

        wb.save(file_path)

class CSVFileUtils(FileUtils):
    def read(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = [row for row in reader]
            return data

    def write(self, file_path, content: list[list], mode='w'):
        """
        将数据写入 CSV 文件

        Args:
            file_path (str): 文件保存路径
            content (list[list]): 要写入的数据，二维列表
            mode (str): 文件打开模式，默认为 'w'
        """
        with open(file_path, mode=mode, encoding='utf-8', newline='') as f:
            writer = csv.writer(f)
            writer.writerows(content)
            