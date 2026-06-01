from playwright.sync_api import Page, Locator
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Page object for the login page"""
    
    def __init__(self, page: Page):
        super().__init__(page)
        self.email_input = page.locator("input[name='email']")
        self.password_input = page.locator("input[name='password']")
        self.sign_in_button = page.get_by_role("button", name="Sign In")
        self.platform_admin = page.get_by_text("Platform Admin")
    
    def login(self, email: str, password: str) -> None:
        """Perform login with credentials"""
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.sign_in_button.click()
        self.platform_admin.click()
        self.wait_for_load_state()
