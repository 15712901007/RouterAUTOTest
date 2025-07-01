from playwright.sync_api import Page
from pages.base_page import BasePage

class NavigationPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.network_settings_menu = page.locator("a").filter(has_text="网络设置")
        self.vlan_settings_link = page.get_by_role("link", name="VLAN设置")
    def go_to_vlan_settings(self):
        self.logger.info("导航到 VLAN 设置页面")
        self.network_settings_menu.click()
        self.vlan_settings_link.click()