import pandas as pd

from dataprocessing.money_dataprocessing import convert_money_columns
from dataprocessing.movie_dataprocessing import (
    define_types,
    clean_release_column,
)
from dataprocessing.time_dataprocessing import format_time_to_minutes


def clean_lists(df: pd.DataFrame, column: str) -> pd.DataFrame:

    for list_to_clean in df[column]:
        for idx in range(len(list_to_clean)):
            if column == "country":
                list_to_clean[idx] = list_to_clean[idx].strip()
            else:
                list_to_clean[idx] = list_to_clean[idx].strip().title()
    return df


def remove_doubles(df: pd.DataFrame, column: str) -> pd.DataFrame:

    df[column] = df[column].apply(lambda row: list(set(row)))

    return df


def clean_list_columns(df: pd.DataFrame) -> pd.DataFrame:

    col_list = [
        "stars",
        "genres",
        "plot_keywords",
        "director",
        "writer",
        "country",
        "creator",
    ]
    for col in col_list:
        df[col] = df[col].apply(
            lambda value: value if isinstance(value, list) else list()
        )
    return df


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = format_time_to_minutes(df, "duration")
    df["type"] = df["release"].apply(define_types)
    df = clean_release_column(df, "release")
    df = convert_money_columns(df, "budget")
    df = convert_money_columns(df, "cum_worldwide_gross")
    df = remove_doubles(df, "writer")
    df = clean_lists(df, "genres")
    df = clean_list_columns(df)
    df["certificate"] = (
        df["certificate"]
        .str.replace("Not rated", "Not Rated")
        .str.replace("Unrated", "Not Rated")
        .str.replace("Tous Public", "Tous publics")
    )
    df = df[df["imdb_score"] != ""].copy()
    df.drop(
        columns=["currency", "currency_value"], inplace=True,
    )

    return df
