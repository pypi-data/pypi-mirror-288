import json
import os
import uuid
from typing import Literal


class DataAssert:

    def __init__(self):
        self.data_assert_set = []

    # 添加数据校验
    def add_assert(self, result: Literal['success', 'failed', 'skipped'], content: str) -> uuid.UUID:
        """添加一条数据校验

        Args:
            result (Literal['success', 'failed', 'skipped']): 结果类型，只接受以上三种（success、failed、skipped）
            content (str): 校验文本内容

        Returns:
            uuid.UUID: 返回添加该条数据内容的uuid
        """
        data_id = uuid.uuid4()
        self.data_assert_set.append({"result": result, "content": content, "id": data_id})
        return data_id

    # 删除数据校验
    def delete_assert(self, assert_id: uuid.UUID) -> dict[str, str]:
        """删除一条数据校验

        Args:
            assert_id (uuid.UUID): 需要删除的数据验证id

        Returns:
            dict[str, str]: 返回被删除的内容
        """
        try:
            for data in self.data_assert_set:
                if data["id"] == assert_id:
                    self.data_assert_set.remove(data)
                    return data
        except Exception as e:
            print(f'需要删除的数据验证信息不存在:{e}')

    # 清空所有数据校验
    def clear_assert(self) -> None:
        self.data_assert_set = []

    # 获取数据校验
    def get_assert(self) -> list[dict[str, str]]:
        """获取所有已经添加的数据校验

        Returns:
            list[dict[str, str]]: 返回一个包含已添加数据校验的数组
        """
        return self.data_assert_set

    # 将数据校验写入文件
    def write_assert_file(self, path: str) -> str:
        """将数据校验写入文件

        Args:
            path (str): 需要写入的文件路径（包含文件名）

        Returns:
            str: 返回文件的绝对路径
        """
        try:
            with open(path, 'w', encoding="utf-8") as file:
                result = [
                    {"result": data["result"], "content": data["content"]}
                    for data in self.data_assert_set
                ]
                json.dump(result, file, ensure_ascii=False)
            return os.path.abspath(path)

        except Exception as e:
            print(f"数据写入失败：{e}")
