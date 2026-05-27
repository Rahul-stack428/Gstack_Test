from playwright.sync_api import Page, Locator


class BasePage:
    """Base page class with common functionality"""
    
    def __init__(self, page: Page):
        self.page = page
    
    def navigate(self, url: str) -> None:
        """Navigate to a URL"""
        self.page.goto(url)
    
    def click_element(self, locator: Locator) -> None:
        """Click on an element"""
        locator.click()
    
    def fill_text(self, locator: Locator, text: str) -> None:
        """Fill text into an input field"""
        locator.fill(text)
    
    def wait_for_load_state(self, state: str = "networkidle") -> None:
        """Wait for page load state"""
        self.page.wait_for_load_state(state)
