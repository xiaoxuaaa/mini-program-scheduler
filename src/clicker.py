"""
鼠标点击和键盘操作模块
负责执行自动化点击和键盘操作
"""

import pyautogui
import time
import pyperclip
from typing import List, Tuple, Dict, Any, Union
import platform


class Clicker:
    """自动点击和键盘操作器"""

    def __init__(self, click_interval: float = 0.5):
        """
        初始化点击器

        Args:
            click_interval: 操作之间的间隔时间（秒）
        """
        self.click_interval = click_interval
        # 设置 PyAutoGUI 的安全设置
        pyautogui.PAUSE = 0.1
        pyautogui.FAILSAFE = True  # 鼠标移到屏幕左上角可以中止

    def click_at(self, x: int, y: int, clicks: int = 1) -> bool:
        """
        在指定坐标点击

        Args:
            x: X 坐标
            y: Y 坐标
            clicks: 点击次数

        Returns:
            是否成功执行
        """
        try:
            pyautogui.click(x, y, clicks=clicks)
            return True
        except Exception as e:
            print(f"点击失败 ({x}, {y}): {e}")
            return False

    def click_sequence(self, coordinates: List) -> bool:
        """
        执行一系列点击操作（旧版格式，保持兼容）

        Args:
            coordinates: 坐标列表 [(x1, y1), (x2, y2), ...] 或 [(x1, y1, clicks), ...]
                        第三个参数为点击次数，默认为 1

        Returns:
            是否全部成功
        """
        if not coordinates:
            print("警告: 没有点击坐标")
            return False

        print(f"开始执行点击序列，共 {len(coordinates)} 个点击")
        success = True

        for i, coord in enumerate(coordinates, 1):
            # 支持 (x, y) 或 (x, y, clicks) 格式
            if len(coord) >= 3:
                x, y, clicks = coord[0], coord[1], coord[2]
                click_type = "双击" if clicks == 2 else f"{clicks}次点击"
                print(f"  [{i}/{len(coordinates)}] {click_type}坐标 ({x}, {y})")
            else:
                x, y = coord[0], coord[1]
                clicks = 1
                print(f"  [{i}/{len(coordinates)}] 点击坐标 ({x}, {y})")

            if not self.click_at(x, y, clicks=clicks):
                success = False

            # 点击之间的间隔
            if i < len(coordinates):
                time.sleep(self.click_interval)

        return success

    @staticmethod
    def convert_clicks_to_actions(clicks: List) -> List[Dict[str, Any]]:
        """
        将旧格式的点击坐标转换为新格式的操作列表
        用于向后兼容

        Args:
            clicks: 坐标列表 [(x1, y1), (x2, y2), ...] 或 [(x1, y1, clicks), ...]

        Returns:
            操作列表
        """
        actions = []

        for i, coord in enumerate(clicks, 1):
            if len(coord) >= 3:
                x, y, click_count = coord[0], coord[1], coord[2]
            else:
                x, y, click_count = coord[0], coord[1], 1

            actions.append({
                "type": "click",
                "x": x,
                "y": y,
                "clicks": click_count,
                "label": f"点击 {i}"
            })

        return actions

    def get_current_position(self) -> Tuple[int, int]:
        """获取当前鼠标位置"""
        return pyautogui.position()

    @staticmethod
    def get_screen_size() -> Tuple[int, int]:
        """获取屏幕尺寸"""
        return pyautogui.size()

    def execute_action(self, action: Dict[str, Any]) -> bool:
        """
        执行单个操作（点击、输入、按键、粘贴、等待、调整间隔等）

        Args:
            action: 操作配置字典，格式：
                {
                    "type": "click" | "type" | "hotkey" | "wait" | "paste" | "change_interval",
                    "label": "操作描述",
                    ... 其他参数
                }

        Returns:
            是否成功执行
        """
        action_type = action.get("type")
        label = action.get("label", "未命名操作")

        try:
            if action_type == "click":
                # 点击操作
                x = action.get("x")
                y = action.get("y")
                clicks = action.get("clicks", 1)

                if x is None or y is None:
                    print(f"❌ 点击操作缺少坐标: {label}")
                    return False

                click_type = "双击" if clicks == 2 else f"{clicks}次点击"
                print(f"  → {label}: {click_type} ({x}, {y})")
                pyautogui.click(x, y, clicks=clicks)
                return True

            elif action_type == "type":
                # 输入文本
                text = action.get("text", "")
                interval = action.get("interval", 0.05)  # 字符间隔

                print(f"  → {label}: 输入文本 (长度: {len(text)})")
                pyautogui.write(text, interval=interval)
                return True

            elif action_type == "paste":
                # 粘贴文本（支持中文）
                text = action.get("text", "")

                if not text:
                    print(f"❌ 粘贴操作缺少文本: {label}")
                    return False

                print(f"  → {label}: 粘贴文本 (长度: {len(text)})")

                # 保存当前剪贴板内容
                try:
                    original_clipboard = pyperclip.paste()
                except:
                    original_clipboard = None

                # 复制到剪贴板
                pyperclip.copy(text)
                time.sleep(0.1)  # 等待剪贴板更新

                # 粘贴
                pyautogui.hotkey('ctrl', 'v')
                time.sleep(0.1)  # 等待粘贴完成

                # 恢复原剪贴板内容（可选）
                if original_clipboard is not None:
                    try:
                        pyperclip.copy(original_clipboard)
                    except:
                        pass

                return True

            elif action_type == "hotkey":
                # 按键/快捷键
                keys = action.get("keys", [])

                if not keys:
                    print(f"❌ 快捷键操作缺少按键: {label}")
                    return False

                keys_str = "+".join(str(k) for k in keys)
                print(f"  → {label}: 按键 {keys_str}")
                pyautogui.hotkey(*keys)
                return True

            elif action_type == "wait":
                # 等待
                seconds = action.get("seconds", 1)
                print(f"  → {label}: 等待 {seconds} 秒")
                time.sleep(seconds)
                return True

            elif action_type == "change_interval":
                # 调整间隔（这个操作本身不执行任何动作，只是标记）
                new_interval = action.get("interval", 0.5)
                print(f"  → {label}: 调整操作间隔为 {new_interval} 秒")
                return True

            else:
                print(f"❌ 未知的操作类型: {action_type}")
                return False

        except Exception as e:
            print(f"❌ 执行操作失败 [{label}]: {e}")
            return False

    def execute_actions(self, actions: List[Dict[str, Any]], interval: float = None) -> bool:
        """
        执行一系列操作（新版格式）

        Args:
            actions: 操作列表
            interval: 操作之间的初始间隔时间（秒），None 则使用默认间隔

        Returns:
            是否全部成功
        """
        if not actions:
            print("警告: 没有操作")
            return False

        if interval is None:
            interval = self.click_interval

        print(f"开始执行操作序列，共 {len(actions)} 个操作")
        success = True
        current_interval = interval  # 当前间隔，可以动态改变

        for i, action in enumerate(actions, 1):
            print(f"[{i}/{len(actions)}]", end=" ")

            # 检查是否是调整间隔操作
            if action.get("type") == "change_interval":
                new_interval = action.get("interval", 0.5)
                current_interval = new_interval
                print(f"  ⚡ 调整操作间隔为 {new_interval} 秒")
                continue  # 跳过等待，直接执行下一个操作

            if not self.execute_action(action):
                success = False

            # 操作之间的间隔（最后一个操作后不等待）
            if i < len(actions):
                time.sleep(current_interval)

        return success

    @staticmethod
    def show_desktop() -> bool:
        """
        显示桌面（最小化所有窗口）

        Windows: Win+D
        Mac: Fn+F11 或 Command+F3

        Returns:
            是否成功执行
        """
        try:
            system = platform.system()

            if system == "Windows":
                # Windows: 按 Win+D
                pyautogui.hotkey('win', 'd')
            elif system == "Darwin":  # macOS
                # Mac: 按 Fn+F11
                pyautogui.hotkey('fn', 'f11')
            else:
                print(f"不支持的操作系统: {system}")
                return False

            print("已回到桌面")
            return True

        except Exception as e:
            print(f"回到桌面失败: {e}")
            return False
