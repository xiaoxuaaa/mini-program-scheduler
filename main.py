"""
微信小程序定时助手 - 主程序
"""

import sys
import os
from datetime import datetime
from colorama import init, Fore, Style

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.config_manager import ConfigManager
from src.scheduler import TaskScheduler
from src.clicker import Clicker

# 初始化 colorama（Windows 彩色输出支持）
init(autoreset=True)

# 全局调度器实例
scheduler = None


def print_banner():
    """打印欢迎横幅"""
    print(Fore.CYAN + "=" * 60)
    print(Fore.CYAN + "         定时点击助手 v0.7.2")
    print(Fore.CYAN + "=" * 60)
    print()


def print_menu():
    """打印主菜单"""
    print(Fore.YELLOW + "\n请选择操作:")
    print("  1. 添加任务")
    print("  2. 查看所有任务")
    print("  3. 删除任务")
    print("  4. 启用/禁用任务")
    print("  5. 获取鼠标坐标（辅助工具）")
    print("  6. 启动调度器")
    print("  7. 停止调度器")
    print("  8. 查看调度器状态")
    print("  0. 退出")
    print()


def add_task(config_manager: ConfigManager):
    """添加新任务的交互流程"""
    print(Fore.GREEN + "\n=== 添加新任务 ===\n")

    name = input("任务名称: ").strip()
    if not name:
        print(Fore.RED + "任务名称不能为空")
        return

    description = input("任务描述（可选）: ").strip()

    time_str = input("执行时间（格式 HH:MM，如 14:30）: ").strip()
    # 简单验证时间格式
    try:
        datetime.strptime(time_str, "%H:%M")
    except ValueError:
        print(Fore.RED + "时间格式错误，请使用 HH:MM 格式")
        return

    # 输入点击坐标
    print("\n输入点击坐标（可多个）")
    print("选项:")
    print("  1. 手动输入坐标（格式: x,y）")
    print("  2. 使用工具获取坐标（自动获取）")
    print("  输入 'done' 完成坐标输入")

    clicks = []
    clicker = Clicker()

    while True:
        coord_input = input(f"\n坐标 {len(clicks) + 1} (输入1/2或坐标或done): ").strip()

        if coord_input.lower() == 'done':
            break

        # 选项 2: 自动获取坐标
        elif coord_input == '2':
            import time
            print(Fore.YELLOW + "\n  >> 移动鼠标到目标位置，3秒倒计时后自动获取...")
            for i in range(3, 0, -1):
                print(f"     {i}...")
                time.sleep(1)

            x, y = clicker.get_current_position()
            clicks.append([x, y])
            print(Fore.GREEN + f"  ✓ 已自动获取坐标 ({x}, {y})")

        # 选项 1 或直接输入坐标
        elif coord_input == '1':
            manual_input = input(f"  请输入坐标 (x,y): ").strip()
            try:
                x, y = map(int, manual_input.split(','))
                clicks.append([x, y])
                print(Fore.GREEN + f"  ✓ 已添加坐标 ({x}, {y})")
            except ValueError:
                print(Fore.RED + "  ✗ 格式错误，请使用 x,y 格式")

        # 直接输入坐标（兼容旧方式）
        else:
            try:
                x, y = map(int, coord_input.split(','))
                clicks.append([x, y])
                print(Fore.GREEN + f"  ✓ 已添加坐标 ({x}, {y})")
            except ValueError:
                print(Fore.RED + "  ✗ 无效输入，请输入 1/2 或坐标格式 x,y")

    if not clicks:
        print(Fore.RED + "至少需要一个点击坐标")
        return

    # 保存任务
    if config_manager.add_task(name, time_str, clicks, description):
        print(Fore.GREEN + f"\n✓ 任务添加成功！")
        print(f"  名称: {name}")
        print(f"  时间: {time_str}")
        print(f"  点击数: {len(clicks)}")
    else:
        print(Fore.RED + "\n✗ 任务添加失败")


def list_tasks(config_manager: ConfigManager):
    """列出所有任务"""
    tasks = config_manager.load_tasks()

    if not tasks:
        print(Fore.YELLOW + "\n暂无任务")
        return

    print(Fore.GREEN + f"\n=== 任务列表（共 {len(tasks)} 个）===\n")

    for task in tasks:
        status = Fore.GREEN + "✓ 启用" if task.get("enabled") else Fore.RED + "✗ 禁用"
        print(f"ID: {task['id']} | {status}")
        print(f"  名称: {task['name']}")
        print(f"  时间: {task['time']}")
        print(f"  描述: {task.get('description', '无')}")
        print(f"  点击数: {len(task.get('clicks', []))}")

        if task.get('last_run'):
            print(f"  上次运行: {task['last_run']}")

        print()


def delete_task(config_manager: ConfigManager):
    """删除任务"""
    list_tasks(config_manager)

    try:
        task_id = int(input("\n请输入要删除的任务 ID: ").strip())

        confirm = input(f"确认删除任务 {task_id}? (y/n): ").strip().lower()
        if confirm == 'y':
            if config_manager.remove_task(task_id):
                print(Fore.GREEN + "✓ 任务已删除")
            else:
                print(Fore.RED + "✗ 删除失败，任务不存在")
    except ValueError:
        print(Fore.RED + "无效的 ID")


def toggle_task(config_manager: ConfigManager):
    """启用/禁用任务"""
    list_tasks(config_manager)

    try:
        task_id = int(input("\n请输入要切换状态的任务 ID: ").strip())
        task = config_manager.get_task(task_id)

        if not task:
            print(Fore.RED + "✗ 任务不存在")
            return

        new_status = not task.get("enabled", True)
        if config_manager.update_task(task_id, enabled=new_status):
            status_text = "启用" if new_status else "禁用"
            print(Fore.GREEN + f"✓ 任务已{status_text}")
        else:
            print(Fore.RED + "✗ 操作失败")
    except ValueError:
        print(Fore.RED + "无效的 ID")


def get_mouse_position():
    """获取鼠标坐标的辅助工具"""
    print(Fore.GREEN + "\n=== 鼠标坐标获取工具 ===")
    print("移动鼠标到目标位置，然后回到此窗口按回车")
    print("提示: 你有 3 秒的时间移动鼠标")
    print()

    import time
    clicker = Clicker()

    while True:
        input("按回车开始（3秒倒计时）...")

        for i in range(3, 0, -1):
            print(f"{i}...")
            time.sleep(1)

        x, y = clicker.get_current_position()
        print(Fore.CYAN + f"\n当前坐标: ({x}, {y})")
        print(f"复制此坐标: {x},{y}")

        again = input("\n继续获取? (y/n): ").strip().lower()
        if again != 'y':
            break


def start_scheduler(config_manager: ConfigManager):
    """启动调度器"""
    global scheduler

    if scheduler and scheduler.is_running():
        print(Fore.YELLOW + "\n调度器已经在运行中")
        print("如需重新启动，请先停止调度器（菜单选项 7）")
        return

    scheduler = TaskScheduler(config_manager)
    if scheduler.start():
        print(Fore.GREEN + "\n✓ 调度器已在后台启动")
    else:
        print(Fore.RED + "\n✗ 调度器启动失败")


def stop_scheduler():
    """停止调度器"""
    global scheduler

    if not scheduler or not scheduler.is_running():
        print(Fore.YELLOW + "\n调度器未运行")
        return

    if scheduler.stop():
        print(Fore.GREEN + "\n✓ 调度器已停止")
    else:
        print(Fore.RED + "\n✗ 停止调度器失败")


def show_scheduler_status():
    """显示调度器状态"""
    global scheduler

    print(Fore.GREEN + "\n=== 调度器状态 ===\n")

    if not scheduler:
        print("调度器未初始化")
        return

    status = scheduler.get_status()
    print(status)


def main():
    """主函数"""
    print_banner()

    config_manager = ConfigManager()

    while True:
        print_menu()
        choice = input("请选择: ").strip()

        if choice == "1":
            add_task(config_manager)
        elif choice == "2":
            list_tasks(config_manager)
        elif choice == "3":
            delete_task(config_manager)
        elif choice == "4":
            toggle_task(config_manager)
        elif choice == "5":
            get_mouse_position()
        elif choice == "6":
            start_scheduler(config_manager)
        elif choice == "7":
            stop_scheduler()
        elif choice == "8":
            show_scheduler_status()
        elif choice == "0":
            # 退出前停止调度器
            global scheduler
            if scheduler and scheduler.is_running():
                print(Fore.YELLOW + "\n正在停止调度器...")
                scheduler.stop()
            print(Fore.CYAN + "\n再见！")
            break
        else:
            print(Fore.RED + "无效的选择")


if __name__ == "__main__":
    main()
