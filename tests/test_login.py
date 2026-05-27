import os
import pytest
from dotenv import load_dotenv
from playwright.sync_api import Playwright, Page

load_dotenv()


def do_login(page: Page):
    """Helper function to perform login"""
    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    # Fill email
    page.locator(
        "input[name='email']"
    ).fill(os.getenv("USERNAME"))
    page.wait_for_timeout(500)

    # Fill password
    page.locator(
        "input[name='password']"
    ).fill(os.getenv("PASSWORD"))
    page.wait_for_timeout(500)

    # Wait for button to become enabled
    page.locator(
        "button[type='submit']"
    ).wait_for(state="enabled", timeout=10000)

    # Click Sign In
    page.locator("button[type='submit']").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)


# ─── Page Load Tests ───────────────────────────────────

def test_login_page_loads(playwright: Playwright):
    """Test login page loads successfully"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")

    assert "login" in page.url
    browser.close()


def test_email_field_visible(playwright: Playwright):
    """Test email field is visible"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")

    assert page.locator(
        "input[name='email']"
    ).is_visible()
    browser.close()


def test_password_field_visible(playwright: Playwright):
    """Test password field is visible"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")

    assert page.locator(
        "input[name='password']"
    ).is_visible()
    browser.close()


def test_password_field_masked(playwright: Playwright):
    """Test password field is masked"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")

    input_type = page.locator(
        "input[name='password']"
    ).get_attribute("type")
    assert input_type == "password"
    browser.close()


def test_sign_in_button_disabled_initially(
    playwright: Playwright
):
    """Test Sign In button is disabled when page loads"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")

    button = page.locator("button[type='submit']")
    assert not button.is_enabled(), \
        "Button should be disabled initially"
    browser.close()


# ─── Valid Login Tests ──────────────────────────────────

def test_login_success(playwright: Playwright):
    """Test successful login with valid credentials"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    do_login(page)

    assert "login" not in page.url, \
        "Should redirect away from login page"
    browser.close()


def test_valid_login_redirects_to_dashboard(
    playwright: Playwright
):
    """Test valid login redirects to dashboard"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    do_login(page)

    assert "dashboard" in page.url or \
           "admin" in page.url, \
        "Should redirect to dashboard"
    browser.close()


# ─── Invalid Login Tests ────────────────────────────────

def test_invalid_password(playwright: Playwright):
    """Test login with wrong password stays on login"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    page.locator(
        "input[name='email']"
    ).fill(os.getenv("USERNAME"))
    page.wait_for_timeout(500)

    page.locator(
        "input[name='password']"
    ).fill("WrongPassword123!")
    page.wait_for_timeout(500)

    page.locator(
        "button[type='submit']"
    ).wait_for(state="enabled", timeout=10000)
    page.locator("button[type='submit']").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    assert "login" in page.url, \
        "Should stay on login page"
    browser.close()


def test_invalid_email(playwright: Playwright):
    """Test login with wrong email stays on login"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai/admin/login"
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    page.locator(
        "input[name='email']"
    ).fill("wrong@email.com")
    page.wait_for_timeout(500)

    page.locator(
        "input[name='password']"
    ).fill("SomePassword123!")
    page.wait_for_timeout(500)

    page.locator(
        "button[type='submit']"
    ).wait_for(state="enabled", timeout=10000)
    page.locator("button[type='submit']").click()
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    assert "login" in page.url, \
        "Should stay on login page"
    browser.close()


# ─── Security Tests ─────────────────────────────────────

def test_direct_dashboard_without_login(
    playwright: Playwright
):
    """Test dashboard not accessible without login"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai"
        "/admin/dashboard/503/Demmo"
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    assert "login" in page.url, \
        "Should redirect to login if not logged in"
    browser.close()


def test_direct_organisation_without_login(
    playwright: Playwright
):
    """Test organisation page not accessible without login"""
    browser = playwright.chromium.launch()
    page = browser.new_context().new_page()

    page.goto(
        "https://admin-test.granitestack.ai"
        "/admin/business-board"
    )
    page.wait_for_load_state("networkidle")
    page.wait_for_timeout(2000)

    assert "login" in page.url, \
        "Should redirect to login if not logged in"
    browser.close()