from flask import Flask
from pydantic import BaseModel, Field
from py_framework.bootstrap.application_context import get_config_dict_by_prefix
from py_framework.py_constants import CONFIG_APP_WEB_KEY
from py_framework.web.request_mapping import registered_urls


class WebServerConfig(BaseModel):
    """web服务配置"""
    port: int = Field(title="端口", default=8080)
    context_path: str = Field(title="上下文路径", default='/')


def start_server():
    """启动web服务"""
    # 1. 获取配置
    web_config_props = get_config_dict_by_prefix(CONFIG_APP_WEB_KEY, False)
    web_server_config = WebServerConfig(**web_config_props)

    # 2. 构建服务
    app_web = Flask('app web服务')
    for index, app_url in enumerate(registered_urls):
        full_url = web_server_config.context_path.removesuffix('/') + '/' + app_url.path.removeprefix('/')
        app_web.add_url_rule(rule=full_url,
                             view_func=app_url.handler,
                             methods=app_url.methods,
                             endpoint=app_url.path)
        print('发布服务：' + app_url.path)

    # 3. 启动服务
    app_web.run(host='0.0.0.0', port=web_server_config.port, threaded=True, debug=False)
