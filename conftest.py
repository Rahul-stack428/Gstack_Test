import pytest
import os
from playwright.sync_api import Playwright, Browser, Page
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    """Configure browser context with viewport"""
    return {
        **browser_context_args,
        "viewport": {"width": 1280, "height": 720},
    }


@pytest.fixture(scope="function")
def authenticated_page(browser: Browser) -> Page:
    """Fixture that provides an authenticated page"""
    context = browser.new_context()
    page = context.new_page()
    
    # Login
    page.goto("https://admin-test.granitestack.ai/admin/login")
    page.locator("input[name='email']").fill(os.getenv("USERNAME"))
    page.locator("input[name='password']").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    
    yield page
    
    context.close()


@pytest.fixture(scope="session")
def base_url():
    """Provide base URL from environment"""
    return os.getenv("BASE_URL", "https://admin-test.granitestack.ai")


@pytest.fixture(scope="session")
def test_credentials():
    """Provide test credentials from environment"""
    return {
        "username": os.getenv("USERNAME"),
        "password": os.getenv("PASSWORD")
    }
