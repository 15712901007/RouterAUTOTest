import pytest
import allure
import yaml
from pathlib import Path
from pages.vlan_page import VlanPage

data_file = Path(__file__).parent.parent / 'data' / 'vlan_data.yml'
with open(data_file, 'r', encoding='utf-8') as f:
    vlan_data = yaml.safe_load(f)

@allure.feature("VLAN管理")
class TestVLAN:
    @allure.story("创建VLAN")
    @pytest.mark.parametrize("data", vlan_data['create_success'], ids=[d['case_name'] for d in vlan_data['create_success']])
    def test_create_vlan_success(self, vlan_page: VlanPage, data: dict):
        allure.dynamic.title(f"成功创建VLAN - {data['case_name']}")
        with allure.step("1. 执行创建VLAN操作"):
            vlan_page.create_vlan(data)
        with allure.step("2. 验证VLAN是否成功出现在列表中"):
            assert vlan_page.is_vlan_exist_in_list(data['id'], data['name']), f"VLAN {data['id']} 创建后未在列表中找到"