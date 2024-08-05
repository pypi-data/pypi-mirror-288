from typing import Any

from bs4 import BeautifulSoup

from .helpers import clean_text, split_made_attempted


def parse_player_stats_table(soup: BeautifulSoup, columns: list[str]) -> list[dict[str, Any]]:
    """Parse player stats data from an HTML table."""
    table_data: list[dict[str, Any]] = []
    rows = soup.find_all("tr")

    for row in rows:
        cols: list = row.find_all("td")
        if len(cols) > 1:
            row_data = {}
            player_name = clean_text(cols[1].get_text())
            school = clean_text(cols[2].get_text())
            games_played = clean_text(cols[3].get_text())
            games_started = clean_text(cols[4].get_text())
            row_data["player_name"] = player_name
            row_data["school"] = school
            row_data["games_played"] = games_played
            row_data["games_started"] = games_started
            for j, col in enumerate(columns):
                if j < len(cols) - 1:
                    value = cols[j + 5].get_text().strip()
                    if col in [
                        "field_goal_made",
                        "three_pointers_made",
                        "free_throws_made",
                    ]:
                        made, attempted = split_made_attempted(value)
                        row_data[col] = made
                        row_data[col.replace("made", "attempted")] = attempted
                    else:
                        row_data[col] = value
        table_data.append(row_data)

    return table_data


def merge_player_data(existing_data: list[dict[str, Any]], new_data: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Merge existing and new player data stats."""
    data_dict = {f"{item['player_name']}_{item['school']}_{item['games_played']}": item for item in existing_data}

    for new_item in new_data:
        key = f"{new_item['player_name']}_{new_item['school']}_{new_item['games_played']}"
        if key in data_dict:
            data_dict[key].update(new_item)
        else:
            data_dict[key] = new_item

    return list(data_dict.values())
