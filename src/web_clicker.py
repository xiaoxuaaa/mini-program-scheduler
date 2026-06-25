"""
网页自动化模块
使用 Selenium 进行网页元素定位和点击
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
from typing import Optional, Dict, Any


class WebClicker:
    """网页自动化点击器"""

    def __init__(self):
        """初始化"""
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None

    def start_browser(self, url: str, headless: bool = False) -> bool:
        """
        启动浏览器并打开网页

        Args:
            url: 目标网页地址
            headless: 是否无头模式（不显示浏览器窗口）

        Returns:
            是否成功启动
        """
        try:
            options = Options()
            if headless:
                options.add_argument('--headless')
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')

            # 自动下载和管理 ChromeDriver
            service = Service(ChromeDriverManager().install())
            self.driver = webdriver.Chrome(service=service, options=options)
            self.wait = WebDriverWait(self.driver, 10)

            # 打开网页
            self.driver.get(url)
            print(f"✅ 浏览器已打开：{url}")
            return True

        except Exception as e:
            print(f"❌ 启动浏览器失败: {e}")
            return False

    def inject_selector_script(self) -> bool:
        """
        注入选择器脚本，允许用户点击页面元素

        Returns:
            是否成功注入
        """
        try:
            script = """
            // 生成元素的 XPath
            function getXPath(element) {
                if (element.id !== '') {
                    return '//*[@id="' + element.id + '"]';
                }
                if (element === document.body) {
                    return '//' + element.tagName.toLowerCase();
                }

                var ix = 0;
                var siblings = element.parentNode.childNodes;
                for (var i = 0; i < siblings.length; i++) {
                    var sibling = siblings[i];
                    if (sibling === element) {
                        var tagName = element.tagName.toLowerCase();
                        var parent = getXPath(element.parentNode);
                        return parent + '/' + tagName + '[' + (ix + 1) + ']';
                    }
                    if (sibling.nodeType === 1 && sibling.tagName === element.tagName) {
                        ix++;
                    }
                }
            }

            // 生成优化的 XPath（使用属性）
            function getOptimizedXPath(element) {
                // 优先使用 class 和其他属性
                var path = '';
                var current = element;

                while (current && current !== document.body) {
                    var tagName = current.tagName.toLowerCase();
                    var selector = tagName;

                    // 添加重要属性
                    if (current.className) {
                        var classes = current.className.split(' ').filter(c => c);
                        if (classes.length > 0) {
                            selector += '[@class="' + classes.join(' ') + '"]';
                        }
                    }

                    // 添加其他属性
                    ['hnum', 'wnum', 'id'].forEach(function(attr) {
                        if (current.hasAttribute(attr)) {
                            selector += '[@' + attr + '="' + current.getAttribute(attr) + '"]';
                        }
                    });

                    path = '/' + selector + path;
                    current = current.parentNode;
                }

                return '//' + element.tagName.toLowerCase() + path.substring(path.lastIndexOf('/'));
            }

            // 添加点击监听
            window.selectedElement = null;
            document.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();

                // 清除之前的高亮
                if (window.selectedElement) {
                    window.selectedElement.style.border = '';
                    window.selectedElement.style.boxShadow = '';
                }

                // 高亮当前元素
                e.target.style.border = '3px solid #FF0000';
                e.target.style.boxShadow = '0 0 10px rgba(255, 0, 0, 0.5)';
                window.selectedElement = e.target;

                // 生成选择器信息
                var xpath = getOptimizedXPath(e.target);
                var simpleXPath = getXPath(e.target);
                var cssSelector = '';

                // 尝试生成 CSS Selector
                if (e.target.id) {
                    cssSelector = '#' + e.target.id;
                } else if (e.target.className) {
                    cssSelector = e.target.tagName.toLowerCase() + '.' +
                                  e.target.className.split(' ').join('.');
                }

                // 存储选择器信息
                window.selectorInfo = {
                    xpath: xpath,
                    simpleXPath: simpleXPath,
                    cssSelector: cssSelector,
                    tagName: e.target.tagName,
                    text: e.target.innerText.substring(0, 50),
                    className: e.target.className,
                    id: e.target.id,
                    outerHTML: e.target.outerHTML.substring(0, 200)
                };

                console.log('选中元素:', window.selectorInfo);
            }, true);

            // 添加提示信息
            var hint = document.createElement('div');
            hint.id = 'selector-hint';
            hint.style.cssText = 'position: fixed; top: 10px; left: 50%; transform: translateX(-50%); ' +
                                 'background: #C4612F; color: white; padding: 15px 30px; ' +
                                 'border-radius: 999px; z-index: 999999; font-size: 16px; ' +
                                 'box-shadow: 0 4px 12px rgba(196, 97, 47, 0.3); font-weight: 500;';
            hint.textContent = '👆 请点击要抢的按钮';
            document.body.appendChild(hint);

            console.log('✅ 选择器脚本已注入');
            """

            self.driver.execute_script(script)
            print("✅ 选择器脚本已注入，等待用户点击...")
            return True

        except Exception as e:
            print(f"❌ 注入脚本失败: {e}")
            return False

    def get_selected_element(self) -> Optional[Dict[str, Any]]:
        """
        获取用户选中的元素信息

        Returns:
            选择器信息字典，如果未选择则返回 None
        """
        try:
            selector_info = self.driver.execute_script("return window.selectorInfo;")
            return selector_info
        except Exception as e:
            print(f"❌ 获取选择器失败: {e}")
            return None

    def click_element(self, selector: str, selector_type: str = "xpath") -> bool:
        """
        点击指定元素

        Args:
            selector: 选择器字符串
            selector_type: 选择器类型 ("xpath" 或 "css")

        Returns:
            是否成功点击
        """
        try:
            if selector_type == "xpath":
                element = self.wait.until(
                    EC.element_to_be_clickable((By.XPATH, selector))
                )
            else:
                element = self.wait.until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                )

            element.click()
            print(f"✅ 点击成功: {selector}")
            return True

        except Exception as e:
            print(f"❌ 点击失败: {e}")
            return False

    def test_selector(self, selector: str, selector_type: str = "xpath") -> bool:
        """
        测试选择器是否有效

        Args:
            selector: 选择器字符串
            selector_type: 选择器类型

        Returns:
            是否能找到元素
        """
        try:
            if selector_type == "xpath":
                elements = self.driver.find_elements(By.XPATH, selector)
            else:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)

            if len(elements) > 0:
                print(f"✅ 找到 {len(elements)} 个匹配元素")
                # 高亮第一个元素
                self.driver.execute_script(
                    "arguments[0].style.border = '3px solid #00FF00';",
                    elements[0]
                )
                return True
            else:
                print("❌ 未找到匹配元素")
                return False

        except Exception as e:
            print(f"❌ 测试失败: {e}")
            return False

    def close(self):
        """关闭浏览器"""
        if self.driver:
            self.driver.quit()
            self.driver = None
            print("✅ 浏览器已关闭")

    def __del__(self):
        """析构函数，确保浏览器被关闭"""
        self.close()
