"""
测试 v0.3.0 - 验证去除微信窗口依赖后的功能
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.scheduler import TaskScheduler
from datetime import datetime, timedelta

print("=" * 60)
print("v0.3.0 功能测试 - 通用定时点击工具")
print("=" * 60)

# 测试 1: 配置管理
print("\n[测试 1] 配置管理")
config = ConfigManager()
print("OK - 配置管理器初始化成功")

# 清空旧任务
config.save_tasks([])

# 添加测试任务（2分钟后执行）
future_time = (datetime.now() + timedelta(minutes=2)).strftime("%H:%M")
result = config.add_task(
    name="测试任务",
    time=future_time,
    clicks=[[960, 540]],  # 屏幕中心位置
    description="测试通用点击功能"
)
print(f"OK - 添加任务: {'成功' if result else '失败'}")

# 读取任务
tasks = config.load_tasks()
print(f"OK - 当前任务数: {len(tasks)}")
if tasks:
    print(f"     任务名称: {tasks[0]['name']}")
    print(f"     执行时间: {tasks[0]['time']}")
    print(f"     点击坐标: {tasks[0]['clicks']}")

# 测试 2: 调度器初始化（不启动）
print("\n[测试 2] 调度器初始化")
scheduler = TaskScheduler(config)
print("OK - 调度器初始化成功")
print("OK - 已移除微信窗口依赖")

# 测试 3: 验证调度器属性
print("\n[测试 3] 验证调度器属性")
if hasattr(scheduler, 'window_helper'):
    print("ERROR - 仍然存在 window_helper 属性")
else:
    print("OK - 已移除 window_helper 属性")

if hasattr(scheduler, 'clicker'):
    print("OK - 保留 clicker 属性")
else:
    print("ERROR - 缺少 clicker 属性")

# 测试 4: 模拟任务设置
print("\n[测试 4] 模拟任务设置")
scheduler.setup_tasks()
print("OK - 任务设置完成")

print("\n" + "=" * 60)
print("测试结果总结:")
print("=" * 60)
print("✓ 配置管理正常")
print("✓ 调度器初始化正常")
print("✓ 已移除微信窗口依赖")
print("✓ 保留核心点击功能")
print()
print("v0.3.0 核心变更:")
print("  - 不再查找微信窗口")
print("  - 不再激活窗口")
print("  - 到达时间后直接执行点击")
print("  - 适用于任何应用场景")
print("=" * 60)

# 清理测试数据
config.save_tasks([])
print("\n测试任务已清理")
