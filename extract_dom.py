import asyncio
from playwright.async_api import async_playwright
from dotenv import load_dotenv
import json
import os

load_dotenv()

USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
BASE_URL = os.getenv("BASE_URL")

PAGES = [
    {"name": "login",                "url": f"{BASE_URL}/login"},
    {"name": "dashboard",            "url": f"{BASE_URL}/dashboard"},
    {"name": "organisation_listing", "url": f"{BASE_URL}/organisations"},
    {"name": "platform_listing",     "url": f"{BASE_URL}/platforms"},
]

async def extract_elements(page):
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


async def main():
    all_dom = {}

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        # ── Login ──────────────────────────────────────
        print("Logging in...")
        await page.goto(f"{BASE_URL}/login")
        await page.wait_for_load_state("networkidle")

        # Extract login page before logging in
        print("Extracting login page elements...")
        all_dom["login"] = await extract_elements(page)

        # Perform login
        # Perform login
        await page.locator("input[name='email']").fill(USERNAME)
        await page.locator("input[name='password']").fill(PASSWORD)
        await page.get_by_role("button", name="Sign In").click()
        await page.wait_for_load_state("networkidle")
        await page.wait_for_timeout(2000)
        print("Logged in successfully!")

        # ── Other pages ────────────────────────────────
        for p_info in PAGES[1:]:
            print(f"Extracting: {p_info['name']}...")
            await page.goto(p_info["url"])
            await page.wait_for_load_state("networkidle")
            await page.wait_for_timeout(2000)
            all_dom[p_info["name"]] = await extract_elements(page)
            print(f"Found {len(all_dom[p_info['name']])} elements")

        await browser.close()

    # ── Save to data folder ────────────────────────────
    os.makedirs("data", exist_ok=True)
    with open("data/dom_elements.json", "w") as f:
        json.dump(all_dom, f, indent=2)

    print("\nDone! Saved to data/dom_elements.json")
    print("\nSummary:")
    for page_name, elements in all_dom.items():
        print(f"  {page_name}: {len(elements)} elements found")


asyncio.run(main())