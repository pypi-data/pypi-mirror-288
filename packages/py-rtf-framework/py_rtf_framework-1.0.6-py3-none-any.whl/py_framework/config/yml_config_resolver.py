from .base_config_resolver import BaseConfigResolver
import os
import yaml
import re


def render_env_constructor(loader, node):
    """渲染环境变量的值"""
    value = loader.construct_scalar(node)
    value_name = str(value).strip('${}')
    if value_name.find(":") != -1:
        var_name = value_name[0:value_name.find(":")].strip()
        default_value = value_name[value_name.find(":") + 1:].strip()
    else:
        var_name = value_name
        default_value = None

    target_value = os.getenv(var_name) if os.getenv(var_name) is not None else default_value

    return target_value


# 添加对环境变量的解析
yaml.SafeLoader.add_constructor('!env', render_env_constructor)
yaml.SafeLoader.add_implicit_resolver('!env', re.compile('\${(\S|\s)+}'), None)


class YmlConfigResolver(BaseConfigResolver):
    """配置文件配置解析器"""

    config_file: str = None

    def __init__(self, config_file: str):
        super().__init__('yml:' + config_file)
        self.config_file = config_file

    def load_config(self):
        # 校验配置是否存在
        if not os.path.exists(self.config_file):
            raise ValueError(self.config_file + '不存在')

        with open(self.config_file, 'r') as file:
            yml_config = yaml.safe_load(file)
        # 添加配置文件
        for key, value in yml_config.items():
            self.config[key] = value
