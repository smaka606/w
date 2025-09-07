import asyncio
from playwright.async_api import async_playwright
import os

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        # Get the absolute path to the HTML file
        file_path = os.path.abspath('index.html')

        # Navigate to the local HTML file
        await page.goto(f'file://{file_path}')

        # Wait for the preloader to disappear
        await page.locator('#preloader').wait_for(state='hidden', timeout=20000)
        await page.wait_for_timeout(1000) # 1 second delay

        # 1. Verify the new footer is visible and take a screenshot in light mode
        await page.locator('.footer-v2').wait_for(state='visible')
        await page.screenshot(path="jules-scratch/verification/light_mode_verification.png")

        # 2. Click the dark mode toggle
        toggle_button = page.locator('#dark-mode-toggle')
        await toggle_button.click()

        # 3. Wait for the dark mode class to be applied to the body
        await page.wait_for_function("() => document.body.classList.contains('dark-mode')")

        # 4. Take a screenshot in dark mode
        await page.screenshot(path="jules-scratch/verification/dark_mode_verification.png")

        await browser.close()

if __name__ == '__main__':
    asyncio.run(main())
