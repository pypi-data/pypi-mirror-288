from typing import Self, Callable
from py_framework.bootstrap.application_context import ApplicationContext, set_default_application_context
from py_framework.py_constants import APP_ROOT_DIR_ENV_KEY
import os
from py_framework.web.web_server import start_server
from py_framework.config.bootstrap_config_resolver import BootstrapConfigResolver
import importlib
import importlib.util
import pkgutil
from pathlib import Path
from types import ModuleType
import inspect


def load_py_module(module: ModuleType) -> None:
    """加载py模块"""
    if module.__file__ is None:
        return

    module_path = Path(module.__file__).parent

    module_name = '' if module.__name__ == '__main__' else module.__name__
    for _, sub_module, is_module in pkgutil.iter_modules([str(module_path)]):
        if not is_module:
            full_path = Path(module_path) / f"{sub_module}.py"
            module_spec = importlib.util.spec_from_file_location(
                module_name, str(full_path)
            )
            if module_spec is not None:
                module_to_load = f"{sub_module}" if module_name == '' else f"{module_spec.name}.{sub_module}"
                importlib.import_module(module_to_load)
                # print(f"加载模块: {module_to_load} , {full_path}")
        else:
            sub_module_name = f"{sub_module}" if module_name == '' else f"{module_name}.{sub_module}"
            sub_module_rec = importlib.import_module(sub_module_name)
            load_py_module(sub_module_rec)


class PyApplication:
    """python应用初始化"""

    """是否启动Web"""
    _enable_web: bool = True

    """应用运行的根目录"""
    _root_dir: str = None

    fn_list: list[Callable] = None

    def module_scans(self: Self, module_list: list[ModuleType]) -> Self:
        """扫描模块，适用于带有注解的函数"""
        for module in module_list:
            load_py_module(module)
        return self

    def root_dir(self: Self, work_dir: str) -> Self:
        """应用根目录"""
        self._root_dir = work_dir if work_dir.endswith('/') else work_dir + '/'
        print('应用目录:', self._root_dir)
        return self

    def run_fn(self: Self, _fn_list: list[Callable]) -> Self:
        """运行函数列表"""
        for _fn in _fn_list:
            arg_specs = inspect.getfullargspec(_fn)
            if len(arg_specs.args) > 0:
                error_text = f"初始运行函数必须是无参函数"
                raise ValueError(error_text)
        self.fn_list = _fn_list
        return self

    def enable_web(self: Self, start_web: bool = True) -> Self:
        """是否启用web服务"""
        self._enable_web = start_web
        return self

    def start(self) -> ApplicationContext:
        """开始运行"""
        default_application_context = ApplicationContext()
        set_default_application_context(default_application_context)

        # 校验根目录
        if self._root_dir is None:
            self.root_dir(os.getenv(APP_ROOT_DIR_ENV_KEY))

        # 加载配置
        default_application_context.config_resolver = BootstrapConfigResolver(base_dir=os.getcwd())

        # 运行函数
        if self.fn_list is not None:
            for fn in self.fn_list:
                fn()

        # 校验是否开启web
        if self._enable_web:
            start_server()

        return default_application_context
