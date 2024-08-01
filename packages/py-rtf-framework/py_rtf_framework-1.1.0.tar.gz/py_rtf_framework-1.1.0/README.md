### 框架说明

py_framework开发框架，参照spring boot项目开发框架进行设计，重点提升python开发的便捷性和规范性。

### 重点功能

* 多环境配置支持。bootstrap.yml定义项目共享配置，根据不同的环境加载不同的配置文件：application-[环境].yml。
* 流式数据处理。通过json文件自定义数据处理流程，基于pandas完成多流程数据共享和存储，支持：jdbc数据、pandas、llm和自定义扩展函数。
* WEB框架支持。在python函数添加post_mapping或get_mapping，实现函数到web接口动态映射。

### 启动py应用

* 入口函数 : from py_framework.py_application import PyApplication
* module_scans([sys.modules[\__name__]]) : 扫描所有py文件。检查py语法、导入注解函数。例如：自动导入包含post_mapping的注解。
* .root_dir(os.path.abspath('.')) : 声明作业目录。用于加载配置文件等操作。
* .run_fn([fn]) : 启动运行函数。fn:为import的函数。
* .enable_web(True) : 是否启用web接口服务。默认读取：application.web下的web配置。
* .start() : 启动服务。

