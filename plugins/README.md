# V1版本插件目录

本目录用于存放 MoviePilot V1 版本的插件。

## 插件结构

每个 V1 插件应包含以下文件：

```
plugins/
├── plugin_name/
│   ├── __init__.py         # 插件主文件
│   ├── requirements.txt    # 依赖文件（可选）
│   └── README.md          # 插件说明
└── README.md
```

## V1 插件开发规范

1. 继承 `_PluginBase` 基类
2. 实现必要的方法：`init_plugin()`, `get_state()`, `get_form()` 等
3. 在根目录的 `package.json` 中注册插件信息

## 配置文件

插件信息需要在根目录的 `package.json` 中配置：

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

## 注意事项

- V1 插件适用于 MoviePilot 早期版本
- 新开发的插件建议使用 V2 版本
- 现有 V1 插件可继续维护使用

