"""
多时间点任务示例脚本
用于演示如何创建和使用多时间点任务
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager

def create_wechat_booking_task():
    """
    创建微信小程序抢课任务示例

    场景：
    - 20:57 进入小程序（回到桌面 → 点击微信 → 进入小程序 → 进入约课页面）
    - 21:00 刷新并抢课（点击刷新 → 点击课程 → 确认）
    """

    config_manager = ConfigManager()

    # 多时间点任务配置
    timeline = [
        {
            "time": "20:57",
            "name": "进入小程序",
            "show_desktop": True,  # 先回到桌面
            "clicks": [
                [100, 600],   # 点击任务栏微信图标（请替换为实际坐标）
                [500, 300],   # 点击小程序入口
                [600, 400],   # 点击约课小程序
                [700, 500]    # 进入约课页面
            ],
            "interval": 2.0  # 每次点击间隔 2 秒
        },
        {
            "time": "21:00",
            "name": "刷新并抢课",
            "show_desktop": False,  # 不回桌面，直接操作
            "clicks": [
                [800, 300],   # 点击刷新按钮
                [850, 400],   # 点击目标课程
                [900, 500]    # 点击确认按钮
            ],
            "interval": 0.3  # 抢课要快，0.3 秒间隔
        }
    ]

    # 创建任务
    success = config_manager.add_task(
        name="小程序抢课",
        description="每晚 20:57 进入，21:00 抢课",
        timeline=timeline,
        task_type="multi_time",
        enabled=True
    )

    if success:
        print("✓ 多时间点任务创建成功！")
        print("\n任务详情：")
        print("  名称: 小程序抢课")
        print("  类型: 多时间点任务")
        print(f"  时间点数量: {len(timeline)}")
        print("\n时间轴：")
        for i, point in enumerate(timeline, 1):
            print(f"  {i}. {point['time']} - {point['name']} ({len(point['clicks'])} 个点击)")
        print("\n下一步：")
        print("  1. 启动 Web 服务: python app.py")
        print("  2. 访问 http://localhost:5000")
        print("  3. 点击'启动调度器'")
        print("  4. 等待任务自动执行")
    else:
        print("✗ 任务创建失败")

def create_simple_example():
    """创建简单的两时间点测试任务"""

    config_manager = ConfigManager()

    timeline = [
        {
            "time": "09:00",
            "name": "第一步",
            "show_desktop": True,
            "clicks": [[100, 100], [200, 200]],
            "interval": 1.0
        },
        {
            "time": "09:01",
            "name": "第二步",
            "show_desktop": False,
            "clicks": [[300, 300]],
            "interval": 0.5
        }
    ]

    success = config_manager.add_task(
        name="测试任务",
        description="多时间点测试",
        timeline=timeline,
        task_type="multi_time"
    )

    if success:
        print("✓ 测试任务创建成功")
    else:
        print("✗ 测试任务创建失败")

if __name__ == "__main__":
    print("=" * 60)
    print("         多时间点任务创建工具")
    print("=" * 60)
    print()
    print("请选择操作：")
    print("  1. 创建小程序抢课任务（示例）")
    print("  2. 创建简单测试任务")
    print("  0. 退出")
    print()

    choice = input("请选择: ").strip()

    if choice == "1":
        create_wechat_booking_task()
    elif choice == "2":
        create_simple_example()
    elif choice == "0":
        print("再见！")
    else:
        print("无效的选择")
