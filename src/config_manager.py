"""
配置管理模块
负责任务配置的读取、保存和管理
"""

import json
import os
from typing import List, Dict, Optional
from datetime import datetime


class ConfigManager:
    """配置管理器"""

    def __init__(self, config_path: str = "config/tasks.json"):
        self.config_path = config_path
        self._ensure_config_dir()

    def _ensure_config_dir(self):
        """确保配置目录存在"""
        config_dir = os.path.dirname(self.config_path)
        if config_dir and not os.path.exists(config_dir):
            os.makedirs(config_dir)

    def load_tasks(self) -> List[Dict]:
        """加载所有任务"""
        if not os.path.exists(self.config_path):
            return []

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return []

    def save_tasks(self, tasks: List[Dict]) -> bool:
        """保存所有任务"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(tasks, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False

    def add_task(self, name: str, time: str = None, clicks: List[tuple] = None,
                 description: str = "", enabled: bool = True, timeline: List[Dict] = None,
                 task_type: str = "simple") -> bool:
        """
        添加新任务（支持简单任务和多时间点任务）

        Args:
            name: 任务名称
            time: 执行时间 (HH:MM 格式) - 简单任务使用
            clicks: 点击坐标列表 [(x1, y1), (x2, y2), ...] - 简单任务使用
            description: 任务描述
            enabled: 是否启用
            timeline: 时间轴列表 - 多时间点任务使用
            task_type: 任务类型 ("simple" 或 "multi_time")
        """
        tasks = self.load_tasks()

        task = {
            "id": self._generate_task_id(tasks),
            "name": name,
            "type": task_type,
            "description": description,
            "enabled": enabled,
            "created_at": datetime.now().isoformat(),
            "last_run": None
        }

        # 简单任务
        if task_type == "simple":
            task["time"] = time
            task["clicks"] = clicks if clicks else []
        # 多时间点任务
        elif task_type == "multi_time":
            task["timeline"] = timeline if timeline else []

        tasks.append(task)
        return self.save_tasks(tasks)

    def remove_task(self, task_id: int) -> bool:
        """删除任务"""
        tasks = self.load_tasks()
        tasks = [t for t in tasks if t.get("id") != task_id]
        return self.save_tasks(tasks)

    def update_task(self, task_id: int, **kwargs) -> bool:
        """更新任务"""
        tasks = self.load_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                task.update(kwargs)
                return self.save_tasks(tasks)
        return False

    def get_task(self, task_id: int) -> Optional[Dict]:
        """获取单个任务"""
        tasks = self.load_tasks()
        for task in tasks:
            if task.get("id") == task_id:
                return task
        return None

    def get_enabled_tasks(self) -> List[Dict]:
        """获取所有启用的任务"""
        tasks = self.load_tasks()
        return [t for t in tasks if t.get("enabled", True)]

    def _generate_task_id(self, tasks: List[Dict]) -> int:
        """生成新的任务ID"""
        if not tasks:
            return 1
        return max(t.get("id", 0) for t in tasks) + 1
