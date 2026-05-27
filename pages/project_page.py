from playwright.sync_api import Page
from pages.base_page import BasePage


class ProjectPage(BasePage):
    """Page object for project creation and management"""
    
    def __init__(self, page: Page):
        super().__init__(page)
    
    def select_organization(self, org_name: str) -> None:
        """Select an organization from dropdown"""
        self.page.locator("button").filter(has_text=org_name).click()
    
    def select_workspace(self, workspace_name: str) -> None:
        """Select a workspace"""
        self.page.get_by_role("button", name=workspace_name).click()
    
    def click_create_new_project(self) -> None:
        """Click the Create New Project button"""
        self.page.get_by_role("button", name="Create New Project Start").click()
    
    def fill_project_name(self, name: str) -> None:
        """Fill project name field"""
        self.page.locator("input[name='name']").fill(name)
    
    def fill_project_description(self, description: str) -> None:
        """Fill project description field"""
        self.page.locator("input[name='description']").fill(description)
    
    def click_build_from_scratch(self) -> None:
        """Click Build from Scratch button"""
        self.page.get_by_role("button", name="Build from Scratch").click()
