import asyncio
import logging
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import json
import os
from typing import Dict, List, Any

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

if not all([USERNAME, PASSWORD, BASE_URL]):
    raise ValueError("Missing required environment variables: USERNAME, PASSWORD, BASE_URL")


def validate_dom_element(element: Dict[str, Any]) -> bool:
    """Validate a DOM element has required fields"""
    if not isinstance(element, dict):
        return False
    if "tag" not in element:
        return False
    return True


def validate_dom_data(dom_data: Dict[str, List[Dict[str, Any]]]) -> bool:
    """Validate the complete DOM data structure"""
    if not isinstance(dom_data, dict):
        logger.error("DOM data is not a dictionary")
        return False
    
    for page_name, elements in dom_data.items():
        if not isinstance(elements, list):
            logger.error(f"Elements for page {page_name} is not a list")
            return False
        
        for element in elements:
            if not validate_dom_element(element):
                logger.error(f"Invalid element found in page {page_name}")
                return False
    
    return True

PAGES = [
    {
        "name": "login",
        "url": "https://admin-test.granitestack.ai/admin/login"
    },
    {
        "name": "dashboard",
        "url": "https://admin-test.granitestack.ai/admin/dashboard/503/Demmo"
    },
    {
        "name": "organisation_listing",
        "url": "https://admin-test.granitestack.ai/admin/business-board"
    },
    {
        "name": "platform_listing",
        "url": "https://admin-test.granitestack.ai/admin/platforms"
    },
]

async def extract_elements(page):
    try:
        await page.wait_for_load_state("networkidle")
        return await page.evaluate("""() => {
        const results = [];

        document.querySelectorAll('input').forEach(el => {
            results.push({
                tag: 'input',
                id: el.id || null,
                name: el.name || null,
                type: el.type || null,
                placeholder: el.placeholder || null,
                className: el.className || null,
                'data-testid': el.getAttribute('data-testid')
            });
        });

        document.querySelectorAll('button').forEach(el => {
            results.push({
                tag: 'button',
                id: el.id || null,
                text: el.innerText.trim() || null,
                className: el.className || null,
                'data-testid': el.getAttribute('data-testid')
            });
        });

        document.querySelectorAll('a').forEach(el => {
            results.push({
                tag: 'link',
                id: el.id || null,
                text: el.innerText.trim() || null,
                href: el.href || null,
                className: el.className || null
            });
        });

        document.querySelectorAll('select').forEach(el => {
            results.push({
                tag: 'select',
                id: el.id || null,
                name: el.name || null,
                options: Array.from(el.options).map(o => o.text)
            });
        });

        document.querySelectorAll('table').forEach(el => {
            const headers = Array.from(
                el.querySelectorAll('th')
            ).map(th => th.innerText.trim());
            results.push({
                tag: 'table',
                id: el.id || null,
                headers: headers
            });
        });

        document.querySelectorAll(
            '[role="dialog"], .modal'
        ).forEach(el => {
            results.push({
                tag: 'modal',
                id: el.id || null,
                className: el.className || null
            });
        });

        document.querySelectorAll(
            'nav a, .sidebar a, .menu a'
        ).forEach(el => {
            results.push({
                tag: 'nav_link',
                text: el.innerText.trim() || null,
                href: el.href || null
            });
        });

            return results;
        }""")
    except Exception as e:
        logger.error(f"Error extracting elements: {e}")
        return []


async def main():
    all_dom = {}

    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=False)
            context = await browser.new_context()
            page = await context.new_page()

            # ── Login ──────────────────────────────────────
            logger.info("Logging in...")
            try:
                await page.goto(f"{BASE_URL}/login")
                await page.wait_for_load_state("networkidle")
            except Exception as e:
                logger.error(f"Failed to navigate to login page: {e}")
                raise

            # Extract login page before logging in
            logger.info("Extracting login page elements...")
            all_dom["login"] = await extract_elements(page)

            # Perform login
            try:
                await page.locator("input[name='email']").fill(USERNAME)
                await page.locator("input[name='password']").fill(PASSWORD)
                await page.get_by_role("button", name="Sign In").click()
                await page.wait_for_load_state("networkidle")
                await page.wait_for_timeout(2000)
                logger.info("Logged in successfully!")
            except Exception as e:
                logger.error(f"Login failed: {e}")
                raise

            # ── Other pages ────────────────────────────────
            for p_info in PAGES[1:]:
                logger.info(f"Extracting: {p_info['name']}...")
                try:
                    await page.goto(p_info["url"])
                    await page.wait_for_load_state("networkidle")
                    await page.wait_for_timeout(2000)
                    all_dom[p_info["name"]] = await extract_elements(page)
                    logger.info(f"Found {len(all_dom[p_info['name']])} elements")
                except Exception as e:
                    logger.error(f"Failed to extract {p_info['name']}: {e}")
                    all_dom[p_info["name"]] = []

            await browser.close()

    except Exception as e:
        logger.error(f"Fatal error in main: {e}")
        raise

    # ── Save to data folder ────────────────────────────
    try:
        # Validate data before saving
        if not validate_dom_data(all_dom):
            logger.error("DOM data validation failed, not saving")
            raise ValueError("Invalid DOM data structure")
        
        os.makedirs("data", exist_ok=True)
        with open("data/dom_elements.json", "w") as f:
            json.dump(all_dom, f, indent=2)
        logger.info("Done! Saved to data/dom_elements.json")
        logger.info("Summary:")
        for page_name, elements in all_dom.items():
            logger.info(f"  {page_name}: {len(elements)} elements found")
    except Exception as e:
        logger.error(f"Failed to save data: {e}")
        raise


asyncio.run(main())