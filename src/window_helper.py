"""
窗口管理模块
负责查找和激活微信窗口
"""

import win32gui
import win32con
import time
from typing import Optional


class WindowHelper:
    """Windows 窗口助手"""

    @staticmethod
    def find_wechat_window() -> Optional[int]:
        """
        查找微信窗口句柄

        Returns:
            窗口句柄，如果未找到返回 None
        """
        def callback(hwnd, hwnds):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if "微信" in title:
                    hwnds.append(hwnd)
            return True

        hwnds = []
        win32gui.EnumWindows(callback, hwnds)
        return hwnds[0] if hwnds else None

    @staticmethod
    def activate_window(hwnd: int) -> bool:
        """
        激活指定窗口

        Args:
            hwnd: 窗口句柄

        Returns:
            是否成功激活
        """
        try:
            # 如果窗口最小化，先恢复
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

            # 前置窗口
            win32gui.SetForegroundWindow(hwnd)
            time.sleep(0.2)  # 等待窗口激活
            return True
        except Exception as e:
            print(f"激活窗口失败: {e}")
            return False

    @staticmethod
    def get_window_rect(hwnd: int) -> Optional[tuple]:
        """
        获取窗口位置和大小

        Returns:
            (left, top, right, bottom) 或 None
        """
        try:
            return win32gui.GetWindowRect(hwnd)
        except Exception:
            return None

    @staticmethod
    def list_all_windows():
        """列出所有可见窗口（调试用）"""
        def callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    windows.append((hwnd, title))
            return True

        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
