from playwright.sync_api import Playwright, expect, Page
from datetime import datetime
import pytest
import os
from dotenv import load_dotenv

load_dotenv()


def test_login_success(playwright: Playwright) -> None:
    """Test successful login with valid credentials"""
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    
    page.goto("https://admin-test.granitestack.ai/admin/login")
    page.locator("input[name=\"email\"]").fill(os.getenv("USERNAME"))
    page.locator("input[name=\"password\"]").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Sign In").click()
    
    # Verify login was successful
    expect(page.get_by_text("Platform Admin")).to_be_visible()
    
    context.close()
    browser.close()


def test_navigate_to_organization(playwright: Playwright) -> None:
    """Test navigation to organization selection"""
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    
    # Login first
    page.goto("https://admin-test.granitestack.ai/admin/login")
    page.locator("input[name=\"email\"]").fill(os.getenv("USERNAME"))
    page.locator("input[name=\"password\"]").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    
    # Navigate to organization
    page.get_by_text("Platform Admin").click()
    page.locator("button").filter(has_text="Rahul").click()
    
    context.close()
    browser.close()


def test_select_workspace(playwright: Playwright) -> None:
    """Test workspace selection"""
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    
    # Login and navigate
    page.goto("https://admin-test.granitestack.ai/admin/login")
    page.locator("input[name=\"email\"]").fill(os.getenv("USERNAME"))
    page.locator("input[name=\"password\"]").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Platform Admin").click()
    page.locator("button").filter(has_text="Rahul").click()
    page.get_by_role("button", name="G Gstack").click()
    
    context.close()
    browser.close()


def test_create_project(playwright: Playwright) -> None:
    """Test creating a new project"""
    browser = playwright.chromium.launch()
    context = browser.new_context()
    page = context.new_page()
    
    # Login and navigate to project creation
    page.goto("https://admin-test.granitestack.ai/admin/login")
    page.locator("input[name=\"email\"]").fill(os.getenv("USERNAME"))
    page.locator("input[name=\"password\"]").fill(os.getenv("PASSWORD"))
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    
    page.get_by_text("Platform Admin").click()
    page.locator("button").filter(has_text="Rahul").click()
    page.get_by_role("button", name="G Gstack").click()
    page.get_by_role("button", name="Create New Project Start").click()
    
    # Fill project details
    unique_name = "user_" + datetime.now().strftime("%Y%m%d%H%M%S")
    page.locator("input[name=\"name\"]").fill(unique_name)
    page.locator("input[name=\"description\"]").fill("Test")
    page.get_by_role("button", name="Build from Scratch").click()
    
    context.close()
    browser.close()