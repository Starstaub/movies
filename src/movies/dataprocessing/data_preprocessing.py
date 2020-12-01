import pandas as pd
import numpy as np

from movies.dataprocessing.money_dataprocessing import convert_money_columns
from movies.dataprocessing.movie_dataprocessing import (
    define_types,
    clean_release_column,
)
from movies.dataprocessing.time_dataprocessing import format_time_to_minutes


def column_cleaning(df: pd.DataFrame) -> pd.DataFrame:

    df["title_year"] = ["a" if x == "" else x for x in df["title_year"].values]
    df["title_year"] = pd.to_numeric(
        df["title_year"], downcast="signed", errors="coerce"
    )

    df["number_ratings"] = df["number_ratings"].str.replace(",", "")
    df["number_ratings"] = ["a" if x == "" else x for x in df["number_ratings"].values]
    df["number_ratings"] = pd.to_numeric(df["number_ratings"], errors="coerce")

    df["episode_count"] = df["episode_count"].str.replace(" episodes", "")
    df["episode_count"] = ["a" if x == "" else x for x in df["episode_count"].values]
    df["episode_count"] = pd.to_numeric(
        df["episode_count"], downcast="signed", errors="coerce"
    )

    df["duration"] = df["duration"].replace(0, np.NaN)

    return df


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


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:

    df = format_time_to_minutes(df, "duration")
    df["type"] = df["release"].apply(define_types)
    df = clean_release_column(df, "release")
    df = convert_money_columns(df, "budget")
    df = convert_money_columns(df, "cum_worldwide_gross")
    df = remove_doubles(df, "writer")
    df = column_cleaning(df)
    df = clean_lists(df, "genres")
    df["certificate"] = (
        df["certificate"]
        .str.replace("Not rated", "Not Rated")
        .str.replace("Unrated", "Not Rated")
        .str.replace("Tous Public", "Tous publics")
    )
    df.replace(r"^\s*$", np.NaN, regex=True, inplace=True)
    df = df.dropna(subset=['imdb_score'])
    df.drop(
        columns=["currency", "currency_value"], inplace=True,
    )

    return df
