from playwright.sync_api import Page
from core.logger import logger

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self.logger = logger
    def navigate(self, url: str):
        self.logger.info(f"导航到: {url}")
        self.page.goto(url)