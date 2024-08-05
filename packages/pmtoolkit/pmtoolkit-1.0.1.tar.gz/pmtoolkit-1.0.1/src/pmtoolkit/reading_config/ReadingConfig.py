import configparser
import json
import os
from typing import Any

import xmltodict
import yaml


class ReadingConfig:
    def get(self, input_file: str) -> None:
        """获取config文件内容

        Args:
            input_file (str): 需要读取的文件路径

        Raises:
            ValueError: 当文件不是.ini/.json/.xml/.yaml的一种时抛出异常

        Returns:
            Any: 依据配置文件类型不同返回字典/字典数组形式
        """
        try:
            os.path.exists(input_file)
        except FileNotFoundError:
            return None
        else:
            file_type = input_file.split('.')[-1]
            # 读取ini
            if file_type == 'ini':
                return self._get_ini(input_file)

            # 读取json
            elif file_type == 'json':
                return self._get_json(input_file)

            # 读取yaml
            elif file_type == 'yaml':
                return self._get_yaml(input_file)

            # 读取xml
            elif file_type == 'xml':
                return self._get_xml(input_file)
            else:
                raise ValueError(f"Unsupported file type: {file_type}")

    @staticmethod
    def _get_ini(input_file: str) -> Any:
        """读取ini配置

        Args:
            input_file (str): 需读取文件

        Returns:
           Any: 返回字典类型
        """
        # 创建配置解析器 区分大小写
        config = configparser.RawConfigParser()
        config.optionxform = lambda option: option
        config.read(input_file)

        # 递归返回字典类型
        return {section: dict(config.items(section)) for section in config.sections()}

    @staticmethod
    def _get_json(input_file: str) -> Any:
        """读取json配置

        Args:
            input_file (str): 同_get_ini_

        Returns:
            Any: 返回字典/字典数组类型
        """
        with open(input_file, 'r') as f:
            return json.load(f)

    @staticmethod
    def _get_yaml(input_file: str) -> Any:
        """读取yaml配置

        Args:
            input_file (str): 同_get_ini_

        Returns:
            Any: 返回字典类型
        """
        with open(input_file, 'r') as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    @staticmethod
    def _get_xml(input_file: str) -> Any:
        """读取xml配置

        Args:
            input_file (str): 同_get_ini_

        Return s:
            Any: 返回字典类型
        """
        with open(input_file) as f:
            return xmltodict.parse(f.read())
