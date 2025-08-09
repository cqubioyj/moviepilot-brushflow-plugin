# MoviePilot 插件模板

本文档提供了 MoviePilot 插件开发的标准模板，可以作为新插件开发的起点。

## 基础插件模板

### __init__.py

```python
import time
import threading
from typing import Any, List, Dict, Optional, Tuple
from datetime import datetime

from app.core.config import settings
from app.core.event import eventmanager, Event
from app.log import logger
from app.plugins import _PluginBase
from app.schemas.types import EventType, MediaType


class PluginTemplate(_PluginBase):
    # 插件名称
    plugin_name = "插件模板"
    # 插件描述
    plugin_desc = "这是一个插件开发模板，展示了基本的插件结构和功能"
    # 插件图标
    plugin_icon = ""
    # 插件版本
    plugin_version = "1.0.0"
    # 插件作者
    plugin_author = "Your Name"
    # 作者主页
    author_url = "https://github.com/yourusername"
    # 插件配置项ID前缀
    plugin_config_prefix = "plugintemplate_"
    # 加载顺序
    plugin_order = 1
    # 可使用的用户级别
    auth_level = 2

    # 私有属性
    _enabled = False
    _api_url = ""
    _api_key = ""
    _check_interval = 300  # 5分钟
    _notify_enabled = True
    _auto_process = False
    
    # 运行状态
    _running = False
    _thread = None

    def init_plugin(self, config: dict = None):
        """
        初始化插件
        """
        if config:
            self._enabled = config.get("enabled", False)
            self._api_url = config.get("api_url", "")
            self._api_key = config.get("api_key", "")
            self._check_interval = config.get("check_interval", 300)
            self._notify_enabled = config.get("notify_enabled", True)
            self._auto_process = config.get("auto_process", False)

        # 启动后台服务
        if self._enabled:
            self.start_service()

        logger.info(f"{self.plugin_name} 插件初始化完成：{'启用' if self._enabled else '禁用'}")

    def get_state(self) -> bool:
        """
        获取插件状态
        """
        return self._enabled and self._running

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        """
        定义远程控制命令
        """
        return [
            {
                "cmd": "/plugin_template",
                "event": EventType.PluginAction,
                "desc": "插件模板测试命令",
                "category": "插件",
                "data": {
                    "action": "test"
                }
            }
        ]

    def get_api(self) -> List[Dict[str, Any]]:
        """
        获取插件API
        """
        return [
            {
                "path": "/plugin_template/status",
                "endpoint": self.get_status,
                "methods": ["GET"],
                "summary": "获取插件状态",
                "description": "获取插件运行状态和统计信息"
            }
        ]

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面
        """
        return [
            {
                'component': 'VForm',
                'content': [
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'enabled',
                                            'label': '启用插件',
                                            'hint': '开启后插件将开始工作'
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'notify_enabled',
                                            'label': '启用通知',
                                            'hint': '发送处理结果通知'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'api_url',
                                            'label': 'API地址',
                                            'placeholder': 'http://localhost:8080/api',
                                            'hint': '第三方服务API地址'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'api_key',
                                            'label': 'API密钥',
                                            'placeholder': '请输入API密钥',
                                            'type': 'password',
                                            'hint': 'API访问密钥，可选'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VTextField',
                                        'props': {
                                            'model': 'check_interval',
                                            'label': '检查间隔（秒）',
                                            'type': 'number',
                                            'hint': '后台任务执行间隔'
                                        }
                                    }
                                ]
                            },
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12,
                                    'md': 6
                                },
                                'content': [
                                    {
                                        'component': 'VSwitch',
                                        'props': {
                                            'model': 'auto_process',
                                            'label': '自动处理',
                                            'hint': '自动处理发现的内容'
                                        }
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        'component': 'VRow',
                        'content': [
                            {
                                'component': 'VCol',
                                'props': {
                                    'cols': 12
                                },
                                'content': [
                                    {
                                        'component': 'VAlert',
                                        'props': {
                                            'type': 'info',
                                            'variant': 'tonal',
                                            'text': '这是插件模板的示例配置界面，展示了常用的配置组件。'
                                        }
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ], {
            "enabled": False,
            "api_url": "",
            "api_key": "",
            "check_interval": 300,
            "notify_enabled": True,
            "auto_process": False
        }

    def get_page(self) -> List[dict]:
        """
        拼装插件详情页面
        """
        return [
            {
                'component': 'VRow',
                'content': [
                    {
                        'component': 'VCol',
                        'props': {
                            'cols': 12
                        },
                        'content': [
                            {
                                'component': 'VCard',
                                'props': {
                                    'variant': 'tonal'
                                },
                                'content': [
                                    {
                                        'component': 'VCardTitle',
                                        'props': {
                                            'text': '插件状态'
                                        }
                                    },
                                    {
                                        'component': 'VCardText',
                                        'content': [
                                            {
                                                'component': 'VChip',
                                                'props': {
                                                    'color': 'success' if self.get_state() else 'error',
                                                    'text': '运行中' if self.get_state() else '已停止'
                                                }
                                            }
                                        ]
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]

    def start_service(self):
        """
        启动后台服务
        """
        if self._running:
            return

        self._running = True
        self._thread = threading.Thread(target=self._background_task, daemon=True)
        self._thread.start()
        logger.info(f"{self.plugin_name} 后台服务启动")

    def stop_service(self):
        """
        停止后台服务
        """
        self._running = False
        if self._thread and self._thread.is_alive():
            self._thread.join(timeout=5)
        logger.info(f"{self.plugin_name} 后台服务停止")

    def _background_task(self):
        """
        后台任务
        """
        while self._running:
            try:
                if self._enabled:
                    self._do_work()
                
                # 等待指定间隔
                for _ in range(self._check_interval):
                    if not self._running:
                        break
                    time.sleep(1)
                    
            except Exception as e:
                logger.error(f"{self.plugin_name} 后台任务错误: {e}")
                time.sleep(60)  # 错误时等待1分钟

    def _do_work(self):
        """
        执行主要工作
        """
        logger.debug(f"{self.plugin_name} 执行工作任务")
        
        # 这里实现你的主要功能
        # 例如：API调用、数据处理、文件操作等
        
        if self._api_url:
            result = self._call_api()
            if result and self._auto_process:
                self._process_result(result)

    def _call_api(self) -> Optional[dict]:
        """
        调用第三方API
        """
        try:
            import requests
            
            headers = {}
            if self._api_key:
                headers["Authorization"] = f"Bearer {self._api_key}"
            
            response = requests.get(
                self._api_url,
                headers=headers,
                timeout=30
            )
            response.raise_for_status()
            
            return response.json()
            
        except Exception as e:
            logger.error(f"API调用失败: {e}")
            return None

    def _process_result(self, result: dict):
        """
        处理API结果
        """
        logger.info(f"处理结果: {result}")
        
        # 实现结果处理逻辑
        
        if self._notify_enabled:
            self.post_message(
                title=f"{self.plugin_name}",
                text=f"处理完成: {result.get('message', '未知结果')}"
            )

    @eventmanager.register(EventType.PluginAction)
    def plugin_action(self, event: Event):
        """
        响应插件命令
        """
        event_data = event.event_data
        if not event_data or event_data.get("action") != "test":
            return

        logger.info("收到测试命令")
        
        self.post_message(
            title=f"{self.plugin_name}",
            text="插件测试命令执行成功！",
            userid=event_data.get("user")
        )

    def get_status(self) -> dict:
        """
        获取插件状态API
        """
        return {
            "enabled": self._enabled,
            "running": self._running,
            "last_run": datetime.now().isoformat(),
            "config": {
                "api_url": self._api_url,
                "check_interval": self._check_interval,
                "notify_enabled": self._notify_enabled,
                "auto_process": self._auto_process
            }
        }

    def __del__(self):
        """
        析构函数
        """
        self.stop_service()
```

### requirements.txt

```
requests>=2.28.0
```

### README.md

```markdown
# 插件模板

这是一个 MoviePilot 插件开发模板，展示了基本的插件结构和功能。

## 功能特性

- ✅ 基础插件框架
- ✅ 配置界面示例
- ✅ 后台任务处理
- ✅ API接口示例
- ✅ 事件处理机制
- ✅ 远程命令支持

## 安装配置

1. 在 MoviePilot 插件市场中安装
2. 在插件设置中配置相关参数
3. 启用插件

## 配置说明

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| 启用插件 | 开启/关闭插件 | false |
| API地址 | 第三方服务API地址 | 空 |
| API密钥 | API访问密钥 | 空 |
| 检查间隔 | 后台任务执行间隔（秒） | 300 |
| 启用通知 | 是否发送处理结果通知 | true |
| 自动处理 | 是否自动处理发现的内容 | false |

## 使用方法

1. 配置API地址和密钥
2. 设置合适的检查间隔
3. 启用插件开始工作

## 远程命令

- `/plugin_template` - 测试插件功能

## 版本历史

- v1.0.0: 初始版本
```

## 使用说明

1. 复制模板代码到新的插件目录
2. 修改插件基本信息（名称、描述、作者等）
3. 实现具体的业务逻辑
4. 调整配置界面组件
5. 编写插件文档
6. 测试插件功能

这个模板提供了完整的插件开发框架，包括配置管理、后台任务、事件处理、API接口等常用功能，可以大大简化插件开发过程。
