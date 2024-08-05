"""
USports Basketball Statistics Module

This module provides functions to fetch and process basketball statistics for men's and women's teams and players.

Dependencies:
    - pandas
    - BeautifulSoup (bs4)
    - requests
    - pytest
    - playwright (Chromium only)

Functions:
- usport_players_stats: Fetch player statistics.
- usport_teams_stats: Fetch team statistics.

These functions return pandas DataFrames with the requested statistics.

Examples:
>>> from usports_basketball import usport_players_stats, usport_teams_stats

# Fetch statistics for men's players
>>> men_player_stats_df = usport_players_stats('m')

# Fetch statistics for women's players playing in U Sports championship Final 8
>>> women_player_stats_df = usport_players_stats('w', 'championship')

# Fetch statistics for men's teams
>>> men_team_stats_df = usport_teams_stats('m')

# Fetch statistics for women's playoff teams
>>> women_team_stats_df = usport_teams_stats('w', 'playoffs')

Author:
    OJ Adeyemi

Date Created:
    August 6, 2024
"""

from .player_stats import usport_players_stats
from .team_stats import usport_teams_stats

__all__ = ["usport_players_stats", "usport_teams_stats"]
