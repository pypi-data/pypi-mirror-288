import pandas as pd

from ...utils import convert_types
from ..data_fetching import fetching_standings_data
from ..team_settings import standings_type_mapping


async def get_standings_df(standings_url: str) -> pd.DataFrame:
    """function to handle stadnings data into a pandas DataFrame"""
    # Fetch standings data
    standings_data = await fetching_standings_data(standings_url)

    df = pd.DataFrame(standings_data)
    df = convert_types(df, standings_type_mapping)
    df = df.drop(columns=["ties"])

    return df
