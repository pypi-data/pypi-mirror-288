import os.path
from typing import Any

from .base_config_resolver import BaseConfigResolver
from .env_config_resolver import EnvConfigResolver
from .yml_config_resolver import YmlConfigResolver

from enum import Enum
from pydantic import BaseModel, Field


class AppProfile(str, Enum):
    """系统运行环境"""

    DEV = "dev"
    TEST = "test"
    PROD = "prod"


class AppConfigKey(str, Enum):
    """系统配置Key"""

    APPLICATION_NAME = "application.name"
    
    APPLICATION_PROFILE = "application.profile"


class AppBootstrap(BaseModel):
    """应用bootstrap配置"""

    name: str = Field(default='应用名称', title="系统名称")
    profile: AppProfile = Field(default=AppProfile.DEV, title="系统运行环境")

    @staticmethod
    def from_config(config_resolver: BaseConfigResolver):
        app_bootstrap = AppBootstrap(name=config_resolver.get_config(AppConfigKey.APPLICATION_NAME, ''),
                                     profile=config_resolver.get_config(AppConfigKey.APPLICATION_PROFILE,
                                                                        AppProfile.DEV))
        return app_bootstrap


class BootstrapConfigResolver(BaseConfigResolver):
    """启动配置解析器"""
    config_source_list: list[BaseConfigResolver]

    base_dir: str

    application_config: YmlConfigResolver

    def __init__(self, base_dir: str = './'):
        super().__init__('bootstrap')
        self.base_dir = base_dir if base_dir.endswith('/') else base_dir + '/'
        self.config_source_list = [
            YmlConfigResolver(self.base_dir + 'bootstrap.yml'),
            EnvConfigResolver()
        ]
        # 开始装载配置
        self.load_config()

    def load_config(self):
        for config_source in self.config_source_list:
            config_source.load_config()
        self.load_app_profile_config()

    def load_app_profile_config(self):
        app_bootstrap = AppBootstrap.from_config(self)
        try:
            app_config_resolver = YmlConfigResolver(self.base_dir + 'application-' + app_bootstrap.profile + '.yml')
            app_config_resolver.load_config()
            self.config_source_list.insert(0, app_config_resolver)
        except Exception as e:
            print('应用环境配置文件异常', e)

    def get_config(self, key: str, default: Any = None) -> Any:
        config_value = None
        # 按照优先级获取配置
        for config_source in self.config_source_list:
            config_value = config_source.get_config(key)
            if config_value is not None:
                break
        # 如果有值则使用配置的值，否则返回默认值
        return config_value if config_value is not None else default

    def contain_key(self, key: str) -> bool:
        return self.get_config(key) is not None
