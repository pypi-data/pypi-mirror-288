from abc import ABC, abstractmethod
from typing import Any


class BaseConfigResolver(ABC):
    """基础配置解析器"""

    config: dict[str, Any]

    name: str = None

    def __init__(self, name: str):
        self.name = name
        self.config = {}

    @abstractmethod
    def load_config(self):
        """装载指定类型的配置"""

    def get_config(self, key: str, default: Any = None) -> Any:
        """获取配置属性值"""
        level_config = self.config
        # 逐层获取配置属性值
        key_items = key.split('.')
        for index, key_item in enumerate(key_items):
            if key_item in level_config:
                level_config = level_config[key_item]
            else:
                level_config = None
                break

        return level_config if level_config is not None else default

    def contain_key(self, key: str) -> bool:
        """是否存在指定属性的配置项"""
        return key in self.config
