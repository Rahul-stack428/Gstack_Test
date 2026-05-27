from playwright.sync_api import Page
from pages.base_page import BasePage


class DashboardPage(BasePage):
    """Page object for the dashboard page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.platform_admin_link = page.get_by_text("Platform Admin")
    
    def navigate_to_platform_admin(self) -> None:
        """Navigate to Platform Admin section"""
        self.platform_admin_link.click()
        self.wait_for_load_state()
