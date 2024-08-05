from typing import Any

from bs4 import BeautifulSoup

from .helpers import clean_text, split_made_attempted


def merge_team_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new team data stats"""
    data_dict = {f"{item['team_name']}_{item['games_played']}": item for item in existing_data}

    for new_item in new_data:
        key = f"{new_item['team_name']}_{new_item['games_played']}"
        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())


def parse_team_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse team stats data from an HTML table"""
    table_data: list[dict[str, Any]] = []
    rows = soup.find_all("tr")

    for row in rows:
        cols: list = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            team_name = clean_text(cols[1].get_text())
            games_played = clean_text(cols[2].get_text())
            row_data["team_name"] = team_name
            row_data["games_played"] = games_played
            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 3].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                        "field_goal_made_against",
                        "three_pointers_made_against",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
            table_data.append(row_data)

    return table_data


def parse_standings_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse standings data from an HTML table"""
    table_data: list[dict[str, Any]] = []

    # Find all rows in the table
    rows = soup.find_all("tr")

    for row in rows:
        row_data = {}

        # Extract the team name from the <th> element
        team_name_th = row.find("th", class_="team-name")
        if team_name_th:
            team_name_tag = team_name_th.find("a")
            if team_name_tag:
                team_name = clean_text(team_name_tag.get_text())
                row_data["team_name"] = team_name

        # Extract the column data from <td> elements
        cols = row.find_all("td")
        if cols:
            for col, column_name in zip(cols, columns):
                row_data[column_name] = clean_text(col.get_text())

            table_data.append(row_data)

    return table_data
