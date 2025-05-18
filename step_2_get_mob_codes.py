# script 2
import asyncio
import re
from playwright.async_api import (
    async_playwright,
    TimeoutError as PlaywrightTimeoutError,
)
from datetime import datetime


async def scrape_all_friend_codes(iframe):
    all_codes = set()

    # Get total pages from form IDs (more reliable than paginator text)
    form_ids = await iframe.locator(
        'form[id^="support_allies_paginated_form_"]'
    ).evaluate_all("nodes => nodes.map(n => n.id)")
    page_numbers = [
        int(re.search(r"support_allies_paginated_form_(\d+)", fid).group(1))
        for fid in form_ids
    ]
    max_page = max(page_numbers, default=1)
    print(f"Detected {max_page} pages of allies.")

    # Get current month and year for comparison
    now = datetime.now()
    current_month = now.month
    current_year = now.year % 100  # Match the YY format in the HTML (e.g., 25 for 2025)

    current_page = 1
    while True:
        print(f"Scraping page {current_page}...")

        await iframe.locator("#support_ally_container").wait_for(timeout=5000)

        ally_elements = await iframe.locator(
            '#support_ally_container div[id^="ally_"][id$="_row"]'
        ).all()

        for element in ally_elements:
            element_id = await element.get_attribute("id")
            if not element_id:
                continue

            match = re.search(r"ally_(\d+)_row", element_id)
            if not match:
                continue

            user_id = match.group(1)

            # Check "Last Active" date
            last_active_span = element.locator('span[title="Last Active"]')
            if await last_active_span.count():
                last_active_text = await last_active_span.inner_text()
                try:
                    last_active_date = datetime.strptime(last_active_text, "%m.%d.%y")
                    if (
                        last_active_date.month != current_month
                        or last_active_date.year % 100 != current_year
                    ):
                        print(
                            f"User {user_id} last active on {last_active_text}. Stopping scrape."
                        )
                        break  # Exit the inner loop
                except ValueError:
                    print(
                        f"Could not parse last active date for {user_id}: '{last_active_text}'"
                    )
                    continue

                all_codes.add(user_id)

        else:
            # Continue to next page if we didn’t break the inner loop
            if current_page >= max_page:
                break

            next_button = iframe.locator("a.paginator", has_text="Next")
            if not await next_button.count():
                print("Next button not found. Ending pagination.")
                break

            await next_button.click()
            await asyncio.sleep(1)
            current_page += 1
            continue

        # We hit an old user, stop scraping
        break

    return all_codes


async def run():
    async with async_playwright() as p:
        context = await p.chromium.launch_persistent_context(
            user_data_dir="auth_data",  # directory where cookies/storage will be saved
            headless=False,
        )
        page = await context.new_page()
        url = f"https://www.kanoplay.com/la_cosa_nostra/?game_server=server_2"

        try:
            await page.goto(url)
            await page.wait_for_selector("#portal_canvas_iframe", timeout=5000)
            await page.wait_for_selector("#portal_canvas_iframe", timeout=5000)
            iframe_element = await page.query_selector("#portal_canvas_iframe")
            iframe = await iframe_element.content_frame()

            mob_button = iframe.locator(
                'div.alliances-main-menu a[href*="alliances?game_server=server_2"]'
            )
            await mob_button.wait_for(timeout=5000)
            await mob_button.click()
            print("Clicked MOB button.")

            familia_button = iframe.locator(
                'a[href*="alliances/allies_view?game_server=server_2"] span.submenu-button'
            )
            await familia_button.wait_for(timeout=5000)
            await familia_button.click()
            print("Clicked FAMILIA button.")

            # Wait a bit to ensure content loads
            await asyncio.sleep(1)

            paginator_div = iframe.locator('div[style*="text-align:center"]')
            html_content = await paginator_div.first.inner_html()
            print("Paginator div HTML:\n", html_content)

            # Call the refactored pagination scraping function
            all_codes = await scrape_all_friend_codes(iframe)

            # Save all friend codes to a file
            with open("mob_codes.txt", "w") as f:
                for code in sorted(all_codes):
                    f.write(code + "\n")

            print(f"Scraped a total of {len(all_codes)} friend codes.")

        except PlaywrightTimeoutError as e:
            print(f"Timeout or other error: {e}")

        await context.close()


asyncio.run(run())
