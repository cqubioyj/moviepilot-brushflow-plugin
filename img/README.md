# 图片资源目录

本目录用于存放插件相关的图片资源，如：

- 插件截图
- 使用示例图片
- 架构图
- 流程图等

## 目录结构

```
img/
├── screenshots/             # 插件截图
│   ├── brushflowplus/
│   │   ├── config.png
│   │   └── usage.png
│   └── other_plugin/
├── diagrams/               # 架构图、流程图
└── README.md
```

## 图片规范

- **文件格式**: PNG, JPG, SVG
- **命名规则**: 使用描述性的英文名称
- **文件大小**: 单个文件不超过 2MB
- **分辨率**: 截图建议 1920x1080 或以下

## 引用方式

在文档中引用图片：

```markdown
![配置界面](../img/screenshots/brushflowplus/config.png)
```

