import logging
import time
from typing import Dict, Any

from plugin.plugin import Plugin


class BrushFlowPlus(Plugin):
    def __init__(self):
        super().__init__()

    def get_config_define(self) -> Dict[str, Any]:
        return {
            "enable_brush": False,
            "brush_cron": "0 */12 * * *",
            "brush_sites": [],
            "brush_clients": [],
            "brush_sort": "added_on",
            "brush_max_page": 20,
            "brush_notify": True,
            "media_filter_enabled": False,
            "media_filter_rules": "",
            "resource_filter_enabled": False,
            "resource_filter_rules": ""
        }

    @Plugin.command(name="brushplus", description="增强版刷流任务", icon="brush.jpg", menu=True)
    def brush(self, **kwargs):
        self.log(f"BrushFlowPlus 开始执行...")
        config = self.get_config()
        if not config.get("enable_brush"):
            self.log("刷流功能未启用")
            return

        self.log(f'开始刷流，站点：{config.get("brush_sites")}，下载器：{config.get("brush_clients")}')

        # 模拟刷流逻辑
        time.sleep(5)

        self.log(f"刷流任务执行完成")

    def get_ui_schema(self):
        return {
            "type": "object",
            "properties": {
                "enable_brush": {
                    "type": "boolean",
                    "title": "启用刷流",
                    "description": "是否启用刷流功能"
                },
                "brush_cron": {
                    "type": "string",
                    "title": "执行周期",
                    "description": "使用CRON表达式，默认每12小时执行一次"
                },
                "brush_sites": {
                    "type": "array",
                    "title": "刷流站点",
                    "description": "选择要进行刷流的站点",
                    "items": {
                        "type": "string"
                    }
                },
                "brush_clients": {
                    "type": "array",
                    "title": "下载器",
                    "description": "选择用于刷流的下载器",
                    "items": {
                        "type": "string"
                    }
                },
                "brush_sort": {
                    "type": "string",
                    "title": "排序方式",
                    "description": "按种子的添加时间或完成时间排序",
                    "enum": ["added_on", "completed_on"],
                    "default": "added_on"
                },
                "brush_max_page": {
                    "type": "integer",
                    "title": "最大页数",
                    "description": "最大扫描的种子页数",
                    "default": 20
                },
                "brush_notify": {
                    "type": "boolean",
                    "title": "发送通知",
                    "description": "刷流完成后是否发送通知",
                    "default": True
                },
                "media_filter_enabled": {
                    "type": "boolean",
                    "title": "启用媒体过滤",
                    "description": "根据标题过滤媒体类型"
                },
                "media_filter_rules": {
                    "type": "string",
                    "title": "媒体过滤规则",
                    "description": "每行一个规则，支持正则表达式"
                },
                "resource_filter_enabled": {
                    "type": "boolean",
                    "title": "启用资源过滤",
                    "description": "根据副标题过滤资源类型"
                },
                "resource_filter_rules": {
                    "type": "string",
                    "title": "资源过滤规则",
                    "description": "每行一个规则，支持正则表达式"
                }
            }
        }
