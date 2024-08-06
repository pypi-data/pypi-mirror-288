# main.py

import os
import importlib.util

# 指定插件目录
PLUGIN_DIR = 'nodes_sample/'

# 存储加载的插件
loaded_plugins = []

# 动态加载插件
def load_plugins(plugin_dir):
    for filename in os.listdir(plugin_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            module_name = filename[:-3]  # 去掉 .py 后缀
            module_path = os.path.join(plugin_dir, filename)

            # 动态导入模块
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)

            # 查找派生类
            for attr in dir(module):
                obj = getattr(module, attr)
                if isinstance(obj, type) and issubclass(obj, BasePlugin) and obj is not BasePlugin:
                    loaded_plugins.append(obj())

# 运行所有加载的插件
def run_plugins():
    for plugin in loaded_plugins:
        plugin.run()

if __name__ == "__main__":
    load_plugins(PLUGIN_DIR)
    run_plugins()
