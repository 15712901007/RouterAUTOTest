# pages/login_page.py

from playwright.sync_api import Page, expect
from pages.base_page import BasePage

class LoginPage(BasePage):
    """登录页面对象"""
    def __init__(self, page: Page):
        super().__init__(page)
        # 元素定位器
        self.username_input = page.get_by_role("textbox", name="用户名")
        self.password_input = page.get_by_role("textbox", name="密码")
        self.login_button = page.get_by_role("button", name="登录")
        
        # 【关键修改】根据成功的录制脚本，我们使用“网络设置”链接作为登录成功的标志。
        # 这个定位器与你的录制脚本完全一致，是最可靠的。
        self.success_login_indicator = page.locator("a").filter(has_text="网络设置")

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.logger.info(f"使用用户名 '{username}' 登录")
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()
        
        # 【关键修改】等待这个新的、更可靠的标志出现。
        self.logger.info("等待'网络设置'链接出现，以确认登录成功...")
        expect(self.success_login_indicator).to_be_visible(timeout=10000)
        
        self.logger.info("登录成功，'网络设置'链接已可见。")