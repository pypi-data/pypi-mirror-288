"""
Utilities Package

This package provides utility functions for processing player and team statistics data.

Modules:
- helpers: General functions to assist with data processing.
  - clean_text: Remove extra spaces and newlines from text.
  - convert_types: Convert DataFrame columns to specified types.
  - fetch_table_html: Retrieve HTML content of a table.
  - split_made_attempted: Split a string into made and attempted values.

- player_data_parsing: Functions for handling player data.
  - parse_player_stats_table: Extract player stats from an HTML table.
  - merge_player_data: Combine and update player data records.

- team_data_parsing: Functions for handling team data.
  - parse_standings_table: Extract standings data from an HTML table.
  - parse_team_stats_table: Extract team stats from an HTML table.
  - merge_team_data: Combine and update team data records.

- headers: Provides HTTP header configurations.
  - get_random_header: Retrieve a random HTTP header from predefined options.

- logging_config: Setup and configure logging.
  - setup_logging: Configure logging with customizable settings.
"""

from .headers import get_random_header
from .helpers import clean_text, convert_types, fetch_table_html, split_made_attempted
from .logging_config import setup_logging
from .player_data_parsing import merge_player_data, parse_player_stats_table
from .team_data_parsing import merge_team_data, parse_standings_table, parse_team_stats_table

__all__ = [
    "clean_text",
    "convert_types",
    "fetch_table_html",
    "get_random_header",
    "merge_player_data",
    "merge_team_data",
    "parse_player_stats_table",
    "parse_standings_table",
    "parse_team_stats_table",
    "setup_logging",
    "split_made_attempted",
]
