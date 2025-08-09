# 插件图标目录

本目录用于存放插件图标文件。

## 图标规范

- **文件格式**: PNG 或 SVG
- **命名规则**: `plugin_id.png` 或 `plugin_id.svg`
- **推荐尺寸**: 64x64px (PNG) 或矢量 (SVG)
- **背景**: 透明背景
- **风格**: 简洁明了，符合 Material Design 风格

## 示例

```
icons/
├── brushflowplus.png        # BrushFlow增强版图标
├── auto_backup.svg          # 自动备份插件图标
├── media_cleaner.png        # 媒体清理插件图标
└── README.md
```

## 图标使用

在插件的 `package.json` 或 `package.v2.json` 中引用：

```json
{
  "icon": "https://raw.githubusercontent.com/cqubioyj/MoviePilot-Plugins/main/icons/plugin_id.png"
}
```

