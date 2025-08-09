# V2版本插件目录

本目录用于存放 MoviePilot V2 版本的插件。V2 版本是推荐的插件开发版本，具有更好的功能和性能。

## 插件结构

每个 V2 插件应包含以下文件：

```
plugins.v2/
├── plugin_name/
│   ├── __init__.py         # 插件主文件
│   ├── requirements.txt    # Python依赖文件
│   ├── config.yaml        # 配置文件（可选）
│   ├── templates/          # 模板文件目录（可选）
│   └── static/            # 静态资源目录（可选）
└── README.md
```

## V2 插件开发规范

V2 插件相比 V1 版本具有以下特点：

1. 更强大的配置界面支持
2. 更好的事件处理机制
3. 支持插件间通信
4. 更完善的生命周期管理
5. 支持自定义页面和API

## 基础插件类结构

```python
from app.plugins import _PluginBase
from typing import Any, List, Dict, Optional, Tuple

class YourPlugin(_PluginBase):
    # 插件名称
    plugin_name = "插件名称"
    # 插件描述
    plugin_desc = "插件描述"
    # 插件图标
    plugin_icon = ""
    # 插件版本
    plugin_version = "1.0.0"
    # 插件作者
    plugin_author = "作者名称"
    # 作者主页
    author_url = ""
    # 插件配置项ID前缀
    plugin_config_prefix = "your_plugin_"
    # 加载顺序
    plugin_order = 1
    # 可使用的用户级别
    auth_level = 2

    def init_plugin(self, config: dict = None):
        """初始化插件"""
        pass

    def get_state(self) -> bool:
        """获取插件状态"""
        return True

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """拼装插件配置页面"""
        return [], {}

    def get_page(self) -> List[dict]:
        """拼装插件详情页面"""
        return []

    def stop_service(self):
        """退出插件"""
        pass
```

## 配置文件

插件信息需要在根目录的 `package.v2.json` 中配置：

```json
{
  "PluginName": {
    "name": "插件显示名称",
    "description": "插件描述",
    "version": "1.0.0",
    "author": "作者名称",
    "level": 2,
    "category": "插件分类",
    "icon": "图标地址",
    "history": {
      "v1.0.0": "初始版本"
    }
  }
}
```

## 插件分类

- **索引器**: 搜索和资源索引功能
- **下载器**: 下载管理和控制
- **媒体服务器**: 媒体库管理和整理
- **通知**: 消息推送和通知
- **站点**: 站点管理和维护
- **订阅**: 订阅管理和自动化
- **认证**: 认证和授权管理
- **工具**: 实用工具和辅助功能

## 开发指南

1. 遵循 MoviePilot 插件开发规范
2. 使用类型提示增强代码可读性
3. 实现完整的错误处理机制
4. 提供详细的配置说明
5. 编写完整的文档和示例

## 现有插件

- **BrushFlow增强版**: 支持媒体过滤和资源过滤的搜索插件

## 贡献插件

欢迎贡献您的插件！请确保：

1. 代码质量符合规范
2. 提供完整的文档
3. 包含使用示例
4. 测试功能正常
