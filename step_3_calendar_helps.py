# script 3
import asyncio
from playwright.async_api import async_playwright
import datetime


def month():
    current_month = datetime.datetime.now().month
    return f"{current_month:02d}"


def year():
    current_year = datetime.datetime.now().year
    return str(current_year)[-2:]


async def visit_urls():
    async with async_playwright() as p:

        with open("mob_codes.txt", "r") as file:
            lines = file.readlines()

        codes = [line[:-1] for line in lines]

        codes = list((set(codes)))
        print(len(codes))
        y = year()
        m = month()
        context = await p.chromium.launch_persistent_context(
            user_data_dir="auth_data",  # directory where cookies/storage will be saved
            headless=False,
        )
        page = await context.new_page()

        for i, code in enumerate(codes):
            url = f"https://www.kanoplay.com/la_cosa_nostra/minigame/help_friend/{y}{m}/{code}?game_server=server_2"
            print(f"{i}, visiting: {url}")

            # Set up a one-time listener for any response
            got_response = asyncio.Event()

            def on_response(response):
                if not got_response.is_set():
                    got_response.set()

            page.on("response", on_response)

            await page.goto(url, wait_until="domcontentloaded")

            try:
                await asyncio.wait_for(got_response.wait(), timeout=5)
                print(f"Got a response for: {url}")
            except asyncio.TimeoutError:
                print(f"No response received for: {url} within timeout.")

            await asyncio.sleep(1)

            # Use remove_listener instead of .off()
            page.remove_listener("response", on_response)
        await asyncio.sleep(180)
        await context.close()


asyncio.run(visit_urls())
