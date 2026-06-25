"""
任务调度模块
负责定时任务的调度和执行
"""

import schedule
import time
import threading
from datetime import datetime
from typing import Callable, List, Dict
from .config_manager import ConfigManager
from .clicker import Clicker


class TaskScheduler:
    """任务调度器"""

    def __init__(self, config_manager: ConfigManager):
        self.config_manager = config_manager
        self.clicker = Clicker()
        self.running = False
        self.thread = None

    def setup_tasks(self):
        """设置所有启用的定时任务"""
        schedule.clear()  # 清除旧任务

        tasks = self.config_manager.get_enabled_tasks()
        if not tasks:
            print("没有启用的任务")
            return

        for task in tasks:
            task_type = task.get("type", "simple")

            # 简单任务（旧版兼容）
            if task_type == "simple":
                task_time = task.get("time")
                if not task_time:
                    continue

                def create_job(t):
                    return lambda: self._execute_simple_task(t)

                schedule.every().day.at(task_time).do(create_job(task))
                print(f"已设置任务: {task['name']} - {task_time}")

            # 多时间点任务
            elif task_type == "multi_time":
                timeline = task.get("timeline", [])
                if not timeline:
                    print(f"警告: 任务 '{task['name']}' 没有时间轴配置")
                    continue

                for time_point in timeline:
                    time_str = time_point.get("time")
                    if not time_str:
                        continue

                    def create_multi_job(t, tp):
                        return lambda: self._execute_timeline_point(t, tp)

                    schedule.every().day.at(time_str).do(create_multi_job(task, time_point))
                    point_name = time_point.get("name", "未命名步骤")
                    print(f"已设置任务: {task['name']} - {point_name} ({time_str})")

    def _execute_task(self, task: Dict):
        """
        执行单个简单任务（旧版兼容）

        Args:
            task: 任务配置字典
        """
        print(f"\n{'='*50}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行任务")
        print(f"任务名称: {task['name']}")
        print(f"任务描述: {task.get('description', '无')}")
        print(f"{'='*50}")

        # 获取点击坐标列表
        clicks = task.get("clicks", [])
        if not clicks:
            print("⚠️  警告: 没有配置点击坐标")
            return

        # 等待0.5秒确保准备就绪
        print("准备执行点击操作...")
        time.sleep(0.5)

        # 执行点击序列
        success = self.clicker.click_sequence(clicks)

        # 更新任务执行记录
        if success:
            print("✓ 任务执行成功")
            self.config_manager.update_task(
                task["id"],
                last_run=datetime.now().isoformat()
            )
        else:
            print("❌ 任务执行失败")

        print(f"{'='*50}\n")

    def _execute_simple_task(self, task: Dict):
        """执行简单任务（_execute_task 的别名，保持兼容）"""
        self._execute_task(task)

    def _execute_timeline_point(self, task: Dict, time_point: Dict):
        """
        执行多时间点任务的某个时间点

        Args:
            task: 任务配置字典
            time_point: 时间点配置
        """
        print(f"\n{'='*50}")
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 开始执行任务")
        print(f"任务名称: {task['name']}")
        print(f"步骤名称: {time_point.get('name', '未命名步骤')}")
        print(f"任务描述: {task.get('description', '无')}")
        print(f"{'='*50}")

        # 是否先回到桌面
        if time_point.get("show_desktop", False):
            print("正在回到桌面...")
            self.clicker.show_desktop()
            time.sleep(1)  # 等待桌面显示

        # 获取自定义间隔，默认使用 clicker 的间隔
        interval = time_point.get("interval", self.clicker.click_interval)

        # 临时修改 clicker 的间隔
        original_interval = self.clicker.click_interval
        self.clicker.click_interval = interval

        print(f"准备执行操作（间隔 {interval} 秒）...")
        time.sleep(0.5)

        # 优先使用新格式的 actions
        actions = time_point.get("actions")

        if actions:
            # 新格式：执行操作序列
            success = self.clicker.execute_actions(actions, interval)
        else:
            # 旧格式：执行点击序列（向后兼容）
            clicks = time_point.get("clicks", [])
            if not clicks:
                print("⚠️  警告: 没有配置操作或点击坐标")
                self.clicker.click_interval = original_interval
                return

            success = self.clicker.click_sequence(clicks)

        # 恢复原间隔
        self.clicker.click_interval = original_interval

        # 更新任务执行记录
        if success:
            print("✓ 任务步骤执行成功")
            self.config_manager.update_task(
                task["id"],
                last_run=datetime.now().isoformat()
            )
        else:
            print("❌ 任务步骤执行失败")

        print(f"{'='*50}\n")

    def start(self):
        """启动调度器（后台运行）"""
        if self.running:
            print("调度器已经在运行中")
            return False

        self.running = True
        self.setup_tasks()

        print("\n调度器已启动（后台运行）")
        print(f"当前时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

        # 显示下次执行时间
        jobs = schedule.get_jobs()
        if jobs:
            print("\n待执行任务:")
            for job in jobs:
                print(f"  - 下次执行: {job.next_run}")

        print("\n提示: 选择菜单 7 可以停止调度器")
        print("调度器将在后台持续运行...\n")

        # 在后台线程中运行
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        return True

    def _run_scheduler(self):
        """后台运行调度器"""
        while self.running:
            schedule.run_pending()
            time.sleep(0.3)  # 每0.3秒检查一次，提高精度

    def stop(self):
        """停止调度器"""
        if not self.running:
            print("调度器未运行")
            return False

        self.running = False
        schedule.clear()

        if self.thread:
            self.thread.join(timeout=2)

        print("调度器已停止")
        return True

    def is_running(self):
        """检查调度器是否在运行"""
        return self.running

    def get_status(self):
        """获取调度器状态"""
        if not self.running:
            return "调度器未运行"

        jobs = schedule.get_jobs()
        if not jobs:
            return "调度器运行中，但没有待执行任务"

        status = f"调度器运行中，共 {len(jobs)} 个任务待执行:\n"
        for job in jobs:
            status += f"  - 下次执行: {job.next_run}\n"

        return status.strip()
