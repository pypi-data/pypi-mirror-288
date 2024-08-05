from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from ...utils import fetch_table_html, get_random_header, merge_player_data, parse_player_stats_table
from ..player_settings import player_stats_columns_type_mapping


async def fetching_player_stats(url: str):
    """Function for handling fetching data from players stat url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()
        headers = get_random_header()
        await page.set_extra_http_headers(headers)

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(url, timeout=50000)
            all_data = []
            for index in range(0, 3):
                table_html = await fetch_table_html(page, index + 3)

                soup = BeautifulSoup(table_html, "html.parser")
                columns = player_stats_columns_type_mapping[index]
                column_names = list(columns.keys())
                table_data = parse_player_stats_table(soup, column_names)
                all_data = merge_player_data(all_data, table_data)
            return all_data

        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}") from e
        finally:
            await browser.close()
