# MoviePilot 插件开发指南

本文档详细介绍如何开发 MoviePilot 插件，包括环境准备、开发规范、最佳实践等。

## 环境准备

### 1. 开发环境

- Python 3.10+
- MoviePilot 开发环境
- Git 版本控制
- IDE（推荐 PyCharm 或 VSCode）

### 2. 目录结构

```
your-plugin/
├── __init__.py         # 插件主文件
├── requirements.txt    # 依赖文件
├── config.yaml        # 配置文件（可选）
├── templates/          # 模板文件（可选）
├── static/            # 静态资源（可选）
└── README.md          # 插件说明
```

## 插件开发

### 1. 基础插件结构

```python
from app.plugins import _PluginBase
from app.log import logger
from typing import Any, List, Dict, Optional, Tuple

class YourPlugin(_PluginBase):
    # 插件基本信息
    plugin_name = "你的插件"
    plugin_desc = "插件功能描述"
    plugin_icon = ""
    plugin_version = "1.0.0"
    plugin_author = "你的名字"
    author_url = "https://github.com/yourusername"
    plugin_config_prefix = "yourplugin_"
    plugin_order = 1
    auth_level = 2

    # 私有变量
    _enabled = False
    _config = {}

    def init_plugin(self, config: dict = None):
        """初始化插件"""
        if config:
            self._enabled = config.get("enabled", False)
            self._config = config
        
        logger.info(f"{self.plugin_name} 插件初始化完成")

    def get_state(self) -> bool:
        """获取插件状态"""
        return self._enabled

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """拼装插件配置页面"""
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {'cols': 12, 'md': 6},
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False
        }

    def stop_service(self):
        """退出插件"""
        logger.info(f"{self.plugin_name} 插件服务停止")
```

### 2. 配置界面组件

MoviePilot 支持多种 Vuetify 组件：

```python
# 开关组件
{
    'component': 'VSwitch',
    'props': {
        'model': 'enabled',
        'label': '启用功能',
    }
}

# 文本输入框
{
    'component': 'VTextField',
    'props': {
        'model': 'api_url',
        'label': 'API地址',
        'placeholder': 'http://localhost:8080'
    }
}

# 选择框
{
    'component': 'VSelect',
    'props': {
        'model': 'download_path',
        'label': '下载路径',
        'items': [
            {'title': '路径1', 'value': '/downloads'},
            {'title': '路径2', 'value': '/media'}
        ]
    }
}

# 数字输入框
{
    'component': 'VTextField',
    'props': {
        'model': 'timeout',
        'label': '超时时间（秒）',
        'type': 'number'
    }
}
```

### 3. 事件处理

```python
from app.core.event import eventmanager, Event
from app.schemas.types import EventType

@eventmanager.register(EventType.DownloadAdded)
def download_added_handler(self, event: Event):
    """下载添加事件处理"""
    event_data = event.event_data
    logger.info(f"新增下载任务: {event_data}")

@eventmanager.register(EventType.TransferComplete)
def transfer_complete_handler(self, event: Event):
    """转移完成事件处理"""
    event_data = event.event_data
    logger.info(f"转移完成: {event_data}")
```

## 开发规范

### 1. 代码规范

- 使用 PEP 8 代码风格
- 添加类型提示
- 编写文档字符串
- 使用有意义的变量名

### 2. 错误处理

```python
def api_request(self, url: str) -> Optional[dict]:
    """API请求"""
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"API请求失败: {e}")
        return None
    except Exception as e:
        logger.error(f"未知错误: {e}")
        return None
```

### 3. 日志记录

```python
from app.log import logger

# 信息日志
logger.info("插件运行正常")

# 警告日志
logger.warning("配置项缺失，使用默认值")

# 错误日志
logger.error("API请求失败")

# 调试日志
logger.debug("调试信息")
```

## 最佳实践

### 1. 配置管理

```python
def get_config(self, key: str, default=None):
    """获取配置项"""
    return self._config.get(key, default)

def validate_config(self) -> bool:
    """验证配置"""
    required_fields = ["api_url", "api_key"]
    for field in required_fields:
        if not self.get_config(field):
            logger.error(f"配置项 {field} 不能为空")
            return False
    return True
```

### 2. 异步处理

```python
import threading
import time

def background_task(self):
    """后台任务"""
    while self._enabled:
        try:
            # 执行任务
            self.do_work()
            time.sleep(60)  # 等待60秒
        except Exception as e:
            logger.error(f"后台任务错误: {e}")

def start_background_task(self):
    """启动后台任务"""
    thread = threading.Thread(target=self.background_task)
    thread.daemon = True
    thread.start()
```

### 3. 数据持久化

```python
from app.core.config import settings
import json
import os

def save_data(self, data: dict):
    """保存数据"""
    data_dir = settings.CONFIG_PATH / "plugins" / self.plugin_name.lower()
    data_dir.mkdir(parents=True, exist_ok=True)
    
    data_file = data_dir / "data.json"
    with open(data_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def load_data(self) -> dict:
    """加载数据"""
    data_dir = settings.CONFIG_PATH / "plugins" / self.plugin_name.lower()
    data_file = data_dir / "data.json"
    
    if data_file.exists():
        with open(data_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}
```

## 测试与调试

### 1. 本地测试

```python
def test_function(self):
    """测试函数"""
    try:
        result = self.your_function()
        assert result is not None
        logger.info("测试通过")
        return True
    except Exception as e:
        logger.error(f"测试失败: {e}")
        return False
```

### 2. 日志调试

在开发过程中，使用详细的日志记录来跟踪程序执行：

```python
logger.debug(f"开始处理: {data}")
logger.debug(f"处理结果: {result}")
```

## 发布指南

### 1. 版本管理

- 使用语义化版本号（如 1.0.0）
- 在 `package.v2.json` 中更新版本信息
- 维护更新日志

### 2. 文档完善

- 编写详细的 README.md
- 提供配置说明
- 包含使用示例

### 3. 代码审查

- 检查代码质量
- 确保功能正常
- 移除调试代码

## 常见问题

### Q: 插件无法加载？
A: 检查插件代码语法、依赖安装、配置文件格式。

### Q: 配置界面不显示？
A: 检查 `get_form()` 方法返回格式是否正确。

### Q: 事件处理不生效？
A: 确保正确注册事件处理器，检查事件类型是否匹配。

## 参考资源

- [MoviePilot 官方文档](https://github.com/jxxghp/MoviePilot)
- [Vuetify 组件文档](https://vuetifyjs.com/)
- [Python 类型提示](https://docs.python.org/3/library/typing.html)
