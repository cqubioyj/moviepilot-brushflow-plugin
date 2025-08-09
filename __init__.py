import re
from typing import List, Dict, Any, Optional, Tuple
from urllib.parse import quote

from app.core.config import settings
from app.log import logger
from app.plugins import _PluginBase
from app.schemas.types import MediaType


class BrushFlowPlus(_PluginBase):
    # 插件名称
    plugin_name = "BrushFlow增强版"
    # 插件描述
    plugin_desc = "支持 MoviePilot 媒体过滤和资源过滤的 BrushFlow 搜索插件"
    # 插件图标
    plugin_icon = ""
    # 插件版本
    plugin_version = "1.0.0"
    # 插件作者
    plugin_author = "cqubioyj"
    # 作者主页
    author_url = "https://github.com/cqubioyj"
    # 插件配置项ID前缀
    plugin_config_prefix = "brushflowplus_"
    # 加载顺序
    plugin_order = 1
    # 可使用的用户级别
    auth_level = 2

    # 私有属性
    _enabled = False
    _brushflow_url = ""
    _api_key = ""
    _timeout = 30

    def init_plugin(self, config: dict = None):
        """
        初始化插件
        """
        if config:
            self._enabled = config.get("enabled", False)
            self._brushflow_url = config.get("brushflow_url", "")
            self._api_key = config.get("api_key", "")
            self._timeout = config.get("timeout", 30)

        logger.info(f"BrushFlow增强版插件初始化完成：{'启用' if self._enabled else '禁用'}")

    def get_state(self) -> bool:
        """
        获取插件状态
        """
        return self._enabled

    @staticmethod
    def get_command() -> List[Dict[str, Any]]:
        """
        定义远程控制命令
        """
        return []

    def get_api(self) -> List[Dict[str, Any]]:
        """
        获取插件API
        """
        return []

    def get_form(self) -> Tuple[List[dict], Dict[str, Any]]:
        """
        拼装插件配置页面，需要返回两块数据：1、页面配置；2、数据结构
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
                                            'model': 'brushflow_url',
                                            'label': 'BrushFlow服务器地址',
                                            'placeholder': 'http://localhost:8080'
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
                                            'placeholder': '可选，如果BrushFlow需要认证'
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
                                            'model': 'timeout',
                                            'label': '超时时间（秒）',
                                            'type': 'number',
                                            'placeholder': '30'
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
                                            'text': '本插件为 BrushFlow 搜索增强版，支持 MoviePilot 的媒体过滤和资源过滤功能。'
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
            "brushflow_url": "",
            "api_key": "",
            "timeout": 30
        }

    def get_page(self) -> List[dict]:
        """
        拼装插件详情页面，需要返回页面配置，同时接收地址栏参数
        """
        return []

    def apply_media_filter(self, results: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """
        应用媒体过滤
        """
        if not filters:
            return results
            
        filtered_results = results
        
        # 类型过滤
        media_type = filters.get("type")
        if media_type and media_type != MediaType.UNKNOWN:
            filtered_results = [r for r in filtered_results if r.get("type") == media_type]
        
        # 年份过滤
        year = filters.get("year")
        if year:
            filtered_results = [r for r in filtered_results if r.get("year") == year]
        
        # 评分过滤
        vote_average = filters.get("vote_average")
        if vote_average:
            filtered_results = [r for r in filtered_results if r.get("vote_average", 0) >= vote_average]
        
        return filtered_results

    def apply_resource_filter(self, results: List[Dict], filters: Dict[str, Any]) -> List[Dict]:
        """
        应用资源过滤
        """
        if not filters:
            return results
            
        filtered_results = []
        
        for result in results:
            torrent_info = result.get("torrent_info", {})
            title = torrent_info.get("title", "")
            
            # 质量过滤
            quality = filters.get("quality")
            if quality:
                quality_patterns = {
                    "4K": r"4K|2160p|UHD",
                    "1080p": r"1080p|1080i|FHD", 
                    "720p": r"720p|HD",
                    "480p": r"480p|SD"
                }
                pattern = quality_patterns.get(quality)
                if pattern and not re.search(pattern, title, re.IGNORECASE):
                    continue
            
            # 来源过滤
            source = filters.get("source")
            if source:
                source_patterns = {
                    "BluRay": r"BluRay|Blu-ray",
                    "Remux": r"Remux",
                    "WEB-DL": r"WEB-DL|WEB\.DL",
                    "WEBRip": r"WEB-Rip|WEBRip",
                    "HDTV": r"HDTV"
                }
                pattern = source_patterns.get(source)
                if pattern and not re.search(pattern, title, re.IGNORECASE):
                    continue
            
            # 编码过滤
            codec = filters.get("codec")
            if codec:
                codec_patterns = {
                    "H265": r"H\.?265|x265|HEVC",
                    "H264": r"H\.?264|x264|AVC"
                }
                pattern = codec_patterns.get(codec)
                if pattern and not re.search(pattern, title, re.IGNORECASE):
                    continue
            
            # 文件大小过滤
            size_range = filters.get("size")
            if size_range:
                size = torrent_info.get("size", 0)
                min_size = size_range.get("min", 0)
                max_size = size_range.get("max", float('inf'))
                if not (min_size <= size <= max_size):
                    continue
            
            filtered_results.append(result)
        
        return filtered_results

    def search(self, keyword: str, 
               media_type: MediaType = None,
               media_filters: Dict[str, Any] = None,
               resource_filters: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """
        搜索方法，支持媒体过滤和资源过滤
        """
        if not self._enabled:
            logger.warning("BrushFlow增强版插件未启用")
            return []
            
        if not self._brushflow_url:
            logger.error("BrushFlow服务器地址未配置")
            return []
        
        try:
            # 构建搜索请求
            search_url = f"{self._brushflow_url.rstrip('/')}/api/search"
            params = {
                "q": keyword,
                "type": media_type.value if media_type else "all"
            }
            
            headers = {}
            if self._api_key:
                headers["Authorization"] = f"Bearer {self._api_key}"
            
            logger.info(f"开始搜索：{keyword}")
            
            # 调用 BrushFlow API (这里需要根据实际 BrushFlow API 调整)
            import requests
            response = requests.get(
                search_url,
                params=params,
                headers=headers,
                timeout=self._timeout
            )
            response.raise_for_status()
            
            # 解析结果
            data = response.json()
            results = data.get("results", [])
            
            logger.info(f"搜索到 {len(results)} 个结果")
            
            # 应用媒体过滤
            if media_filters:
                results = self.apply_media_filter(results, media_filters)
                logger.info(f"媒体过滤后剩余 {len(results)} 个结果")
            
            # 应用资源过滤
            if resource_filters:
                results = self.apply_resource_filter(results, resource_filters)
                logger.info(f"资源过滤后剩余 {len(results)} 个结果")
            
            return results
            
        except Exception as e:
            logger.error(f"BrushFlow搜索失败：{str(e)}")
            return []

    def stop_service(self):
        """
        退出插件
        """
        logger.info("BrushFlow增强版插件服务停止")