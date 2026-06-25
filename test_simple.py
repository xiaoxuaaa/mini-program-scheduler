"""
简化测试脚本 - 避免特殊字符
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.clicker import Clicker
from src.window_helper import WindowHelper

print("=" * 60)
print("Module Function Test")
print("=" * 60)

# Test 1: Config Manager
print("\n[Test 1] Config Manager")
config = ConfigManager()
print("OK - Config manager initialized")

# Add test task
result = config.add_task(
    name="Test Task",
    time="15:00",
    clicks=[[100, 200], [300, 400]],
    description="This is a test task"
)
print(f"OK - Add task: {'Success' if result else 'Failed'}")

# Load tasks
tasks = config.load_tasks()
print(f"OK - Current tasks: {len(tasks)}")
if tasks:
    print(f"     Task name: {tasks[0]['name']}")
    print(f"     Task time: {tasks[0]['time']}")
    print(f"     Clicks: {len(tasks[0]['clicks'])}")

# Test 2: Mouse Control
print("\n[Test 2] Mouse Control")
clicker = Clicker()
print("OK - Clicker initialized")

pos = clicker.get_current_position()
print(f"OK - Current mouse position: {pos}")

screen = clicker.get_screen_size()
print(f"OK - Screen size: {screen[0]} x {screen[1]}")

# Test 3: Window Management
print("\n[Test 3] Window Management")
window_helper = WindowHelper()
print("OK - Window helper initialized")

# Find WeChat window
hwnd = window_helper.find_wechat_window()
if hwnd:
    print(f"OK - Found WeChat window (handle: {hwnd})")
else:
    print("WARNING - WeChat window not found (make sure WeChat is running)")

# List all windows (first 5)
print("\nCurrent open windows (first 5):")
windows = window_helper.list_all_windows()
for i, (hwnd, title) in enumerate(windows[:5], 1):
    print(f"  {i}. {title}")

print("\n" + "=" * 60)
print("All tests completed!")
print("=" * 60)

# Cleanup test data
print("\nCleaning up test task...")
config.remove_task(1)
print("OK - Test task cleaned up")
