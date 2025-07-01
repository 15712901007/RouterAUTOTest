from playwright.sync_api import Page, expect
from pages.base_page import BasePage
from typing import Dict

class VlanPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.add_button = page.get_by_role("link", name="添加")
        self.save_button = page.get_by_role("button", name="保存")
        self.vlan_id_input = page.locator("input[name=\"vlan_id\"]")
        self.vlan_name_input = page.locator("input[name=\"vlan_name\"]")
        self.ip_addr_input = page.locator("input[name=\"ip_addr\"]")
        self.comment_input = page.locator("input[name=\"comment\"]")
        self.confirm_dialog_ok_button = page.locator(".el-message-box__btns .el-button--primary")
    def create_vlan(self, vlan_data: Dict):
        self.logger.info(f"开始创建VLAN, ID: {vlan_data['id']}, 名称: {vlan_data['name']}")
        self.add_button.click()
        self.vlan_id_input.fill(vlan_data.get("id", ""))
        self.vlan_name_input.fill(vlan_data.get("name", ""))
        self.ip_addr_input.fill(vlan_data.get("ip", ""))
        self.comment_input.fill(vlan_data.get("comment", ""))
        self.save_button.click()
        if self.confirm_dialog_ok_button.is_visible():
            self.confirm_dialog_ok_button.click()
    def is_vlan_exist_in_list(self, vlan_id: str, vlan_name: str) -> bool:
        self.logger.info(f"检查VLAN ID '{vlan_id}' 是否存在于列表中")
        row = self.page.locator(f"//tr[contains(., '{vlan_id}') and contains(., '{vlan_name}')]")
        try:
            expect(row).to_be_visible(timeout=5000)
            self.logger.info(f"成功找到VLAN ID '{vlan_id}'")
            return True
        except AssertionError:
            self.logger.warning(f"未在列表中找到VLAN ID '{vlan_id}'")
            return False
    def get_form_error_message(self) -> str:
        error_locator = self.page.locator(".el-form-item__error").first
        expect(error_locator).to_be_visible()
        return error_locator.text_content()