from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from ...utils import fetch_table_html, get_random_header, merge_team_data, parse_team_stats_table
from ..team_settings import stat_group_options, team_stats_columns_type_mapping


async def fetching_team_stats(stats_url: str):
    """function for handling fetching team stats from url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        headers = get_random_header()
        await page.set_extra_http_headers(headers)

        # Block unnecessary resources to speed up page load
        await page.route("**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}", lambda route: route.abort())

        try:
            await page.goto(stats_url, timeout=60 * 1000)
            all_data = []
            team_table_names = stat_group_options.keys()
            for index, _ in enumerate(team_table_names):
                table_html = await fetch_table_html(page, index)

                soup = BeautifulSoup(table_html, "html.parser")
                columns = team_stats_columns_type_mapping[index]
                column_names = list(columns.keys())
                table_data = parse_team_stats_table(soup, column_names)
                all_data = merge_team_data(all_data, table_data)

            return all_data
        except Exception as e:
            raise RuntimeError(f"Error fetching team stats: {e}") from e
        finally:
            await browser.close()
