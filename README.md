# BrushFlow增强版插件

## 功能简介

这是一个为 [MoviePilot](https://github.com/jxxghp/MoviePilot) 开发的 BrushFlow 搜索增强插件，完全遵循 [MoviePilot 插件开发规范](https://github.com/jxxghp/MoviePilot-Plugins?tab=readme-ov-file#%E7%AC%AC%E4%B8%89%E6%96%B9%E6%8F%92%E4%BB%B6%E5%BA%93%E5%BC%80%E5%8F%91%E8%AF%B4%E6%98%8E)。

**项目地址：** [https://github.com/cqubioyj/MoviePilot-Plugins](https://github.com/cqubioyj/MoviePilot-Plugins)

## 主要功能

- ✅ **媒体过滤**：按类型、年份、评分过滤搜索结果
- ✅ **资源过滤**：按质量、来源、编码、文件大小过滤种子
- ✅ **MoviePilot 集成**：原生支持 MoviePilot 的搜索接口
- ✅ **插件规范**：严格按照 MoviePilot 插件规范开发

## 安装方法

### 方法1：通过 MoviePilot 插件市场安装

1. 在 MoviePilot 设置中，将插件源地址添加到环境变量 `PLUGIN_MARKET`：
   ```
   https://github.com/cqubioyj/MoviePilot-Plugins
   ```
2. 重启 MoviePilot
3. 在插件市场中找到"BrushFlow增强版"并安装

### 方法2：手动安装

1. 从 [GitHub 仓库](https://github.com/cqubioyj/MoviePilot-Plugins) 下载插件文件
2. 将插件文件复制到 MoviePilot 的 `plugins` 目录
3. 重启 MoviePilot
4. 在插件管理中启用"BrushFlow增强版"

## 配置说明

| 配置项 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| 启用插件 | 开关 | 是 | 启用/禁用插件 |
| BrushFlow服务器地址 | 文本 | 是 | BrushFlow API 地址 |
| API密钥 | 文本 | 否 | 如果 BrushFlow 需要认证 |
| 超时时间 | 数字 | 否 | 请求超时时间（秒），默认30 |

## 过滤功能

### 媒体过滤
- **类型过滤**：电影、电视剧、动漫
- **年份过滤**：按发行年份筛选
- **评分过滤**：按 IMDB/豆瓣评分筛选

### 资源过滤
- **质量过滤**：4K、1080p、720p、480p
- **来源过滤**：BluRay、Remux、WEB-DL、WEBRip、HDTV
- **编码过滤**：H265、H264
- **大小过滤**：自定义文件大小范围

## 使用方法

1. 在 MoviePilot 中配置好 BrushFlow 服务器地址
2. 启用插件
3. 在 MoviePilot 的搜索界面中，插件会自动应用配置的过滤规则
4. 搜索结果会根据设置的媒体和资源过滤条件进行筛选

## 技术规范

- **插件类型**：索引器插件
- **用户权限级别**：2（认证用户可见）
- **开发规范**：遵循 MoviePilot V1 插件规范
- **依赖**：requests（用于 HTTP 请求）

## 版本历史

- **v1.0.0**：初始版本，支持媒体过滤和资源过滤

## 开发者

**作者：** [cqubioyj](https://github.com/cqubioyj)  
**项目地址：** [https://github.com/cqubioyj/MoviePilot-Plugins](https://github.com/cqubioyj/MoviePilot-Plugins)

## 许可证

本项目遵循 MoviePilot 的开源许可证。
