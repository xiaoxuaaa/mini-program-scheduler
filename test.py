"""
测试脚本 - 验证各个模块功能
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.clicker import Clicker
from src.window_helper import WindowHelper

print("=" * 60)
print("模块功能测试")
print("=" * 60)

# 测试 1: 配置管理
print("\n[测试 1] 配置管理模块")
config = ConfigManager()
print("✓ 配置管理器初始化成功")

# 添加测试任务
result = config.add_task(
    name="测试任务",
    time="15:00",
    clicks=[[100, 200], [300, 400]],
    description="这是一个测试任务"
)
print(f"✓ 添加任务: {'成功' if result else '失败'}")

# 读取任务
tasks = config.load_tasks()
print(f"✓ 当前任务数: {len(tasks)}")

# 测试 2: 鼠标控制
print("\n[测试 2] 鼠标控制模块")
clicker = Clicker()
print("✓ 鼠标控制器初始化成功")

pos = clicker.get_current_position()
print(f"✓ 当前鼠标位置: {pos}")

screen = clicker.get_screen_size()
print(f"✓ 屏幕尺寸: {screen[0]} x {screen[1]}")

# 测试 3: 窗口管理
print("\n[测试 3] 窗口管理模块")
window_helper = WindowHelper()
print("✓ 窗口助手初始化成功")

# 查找微信窗口
hwnd = window_helper.find_wechat_window()
if hwnd:
    print(f"✓ 找到微信窗口 (句柄: {hwnd})")
else:
    print("⚠ 未找到微信窗口 (请确保微信正在运行)")

# 列出所有窗口（前 5 个）
print("\n当前打开的窗口（前 5 个）:")
windows = window_helper.list_all_windows()
for i, (hwnd, title) in enumerate(windows[:5], 1):
    print(f"  {i}. {title} (句柄: {hwnd})")

print("\n" + "=" * 60)
print("所有测试完成！")
print("=" * 60)

# 清理测试数据
print("\n清理测试任务...")
config.remove_task(1)
print("✓ 测试任务已清理")
