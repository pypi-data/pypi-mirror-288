from typing import Any

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

from ...utils import get_random_header, merge_team_data, parse_standings_table
from ..team_settings import standings_type_mapping


async def fetching_standings_data(standings_url: str) -> list[dict[str, Any]]:
    """function for handling fetch standings data from standings url"""
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True, timeout=10000)
        page = await browser.new_page()

        headers = get_random_header()
        await page.set_extra_http_headers(headers)
        # Block unnecessary resources
        await page.route(
            "**/*.{png,jpg,jpeg,gif,webp,css,woff2,woff,js}",
            lambda route: route.abort(),
        )

        await page.goto(standings_url, timeout=10000, wait_until="networkidle")

        await page.wait_for_selector("tbody", timeout=10000)
        tables = await page.query_selector_all("tbody")

        tables_length = len(tables)

        all_standings = []
        for i in range(0, tables_length):
            table = await tables[i].inner_html()

            standings_html = table.replace("\n", "").replace("\t", "")

            soup = BeautifulSoup(standings_html, "html.parser")

            column_names = list(standings_type_mapping.keys())[1:]
            standings_data = parse_standings_table(soup, column_names)
            all_standings = merge_team_data(all_standings, standings_data)

        await browser.close()

        return all_standings
