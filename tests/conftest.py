import pytest
import allure
import configparser
from pathlib import Path
from playwright.sync_api import Page, Playwright
from pages.login_page import LoginPage
from pages.navigation_page import NavigationPage
from pages.vlan_page import VlanPage

config = configparser.ConfigParser()
config.read(Path(__file__).parent.parent / 'config.ini', encoding='utf-8')
router_config = config['Router']

@pytest.fixture(scope="session")
def logged_in_page(playwright: Playwright) -> Page:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    login_page = LoginPage(page)
    login_page.navigate(router_config['base_url'])
    login_page.login(router_config['username'], router_config['password'])
    yield page
    context.close()
    browser.close()

@pytest.fixture
def vlan_page(logged_in_page: Page) -> VlanPage:
    nav_page = NavigationPage(logged_in_page)
    nav_page.go_to_vlan_settings()
    return VlanPage(logged_in_page)

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == 'call' and report.failed:
        page_fixture = item.funcargs.get('logged_in_page')
        if page_fixture:
            try:
                allure.attach(
                    page_fixture.content(),
                    name="失败时的页面源码",
                    attachment_type=allure.attachment_type.HTML
                )
            except Exception as e:
                print(f"附加页面源码失败: {e}")