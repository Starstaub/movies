from datetime import datetime
import pandas as pd


def format_time_to_minutes(df: pd.DataFrame, time_column: str) -> pd.DataFrame:

    df[time_column] = [
        x + " 0min" if "min" not in x else x for x in df[time_column].values
    ]
    df[time_column] = ["0h " + x if "h" not in x else x for x in df[time_column].values]
    df[time_column] = [
        datetime.strptime(x, "%Hh %Mmin") for x in df[time_column].values
    ]
    df[time_column] = df[time_column].dt.hour * 60 + df[time_column].dt.minute

    return df
