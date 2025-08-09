# MoviePilot-Plugin-Market

MoviePilot第三方插件市场：<https://github.com/cqubioyj/MoviePilot-Plugins/>

## 📋 插件列表

### 索引器插件
1. **BrushFlow增强版** v1.0.0 `支持 MoviePilot 媒体过滤和资源过滤的 BrushFlow 搜索插件`

### 自动化插件
<!-- 预留位置 -->

### 媒体管理插件
<!-- 预留位置 -->

### 通知推送插件
<!-- 预留位置 -->

### 工具类插件
<!-- 预留位置 -->

## 🚀 安装方法

### 方法1：插件市场安装（推荐）

1. 在 MoviePilot 设置中，将插件源地址添加到环境变量 `PLUGIN_MARKET`：
   ```
   https://github.com/cqubioyj/MoviePilot-Plugins
   ```
2. 重启 MoviePilot
3. 在插件市场中找到所需插件并安装

### 方法2：手动安装

1. 从 [GitHub 仓库](https://github.com/cqubioyj/MoviePilot-Plugins) 下载插件文件
2. 将插件文件复制到 MoviePilot 的 `plugins` 目录
3. 重启 MoviePilot
4. 在插件管理中启用所需插件

## 📁 仓库结构

```
MoviePilot-Plugins/
├── data/                   # 插件数据文件
├── docs/                   # 插件文档
├── icons/                  # 插件图标
├── img/                    # 图片资源
├── plugins/                # V1版本插件
├── plugins.v2/             # V2版本插件
│   └── brushflowplus/      # BrushFlow增强版插件
├── package.json           # V1插件配置
├── package.v2.json        # V2插件配置
├── README.md              # 说明文档
└── LICENSE                # 许可证
```

## 🛠️ 插件开发

本仓库严格遵循 [MoviePilot 插件开发规范](https://github.com/jxxghp/MoviePilot-Plugins?tab=readme-ov-file#%E7%AC%AC%E4%B8%89%E6%96%B9%E6%8F%92%E4%BB%B6%E5%BA%93%E5%BC%80%E5%8F%91%E8%AF%B4%E6%98%8E)。

### 贡献插件

欢迎提交您的插件！请确保：

1. 遵循 MoviePilot 插件开发规范
2. 提供完整的插件文档
3. 包含测试用例（如适用）
4. 更新相应的 package.json / package.v2.json

### 插件类型

- **索引器插件**：搜索和过滤功能
- **自动化插件**：定时任务和自动化处理
- **媒体管理插件**：媒体库管理和整理
- **通知推送插件**：消息通知和推送
- **工具类插件**：实用工具和辅助功能

## 📞 联系方式

- **作者**：[cqubioyj](https://github.com/cqubioyj)
- **项目地址**：[https://github.com/cqubioyj/MoviePilot-Plugins](https://github.com/cqubioyj/MoviePilot-Plugins)
- **问题反馈**：[Issues](https://github.com/cqubioyj/MoviePilot-Plugins/issues)

## 📄 许可证

本项目采用 GPL-3.0 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。
