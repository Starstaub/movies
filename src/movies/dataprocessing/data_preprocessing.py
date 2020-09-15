import pandas as pd

from movies.dataprocessing.money_dataprocessing import convert_money_columns
from movies.dataprocessing.movie_dataprocessing import (
    define_types,
    clean_release_column,
    get_movie_kind,
)
from movies.dataprocessing.time_dataprocessing import format_time_to_minutes


def column_cleaning(df: pd.DataFrame) -> pd.DataFrame:

    df["title_year"] = [0 if x == "" else x for x in df["title_year"].values]
    df["title_year"] = df["title_year"].astype(int)

    df["number_ratings"] = df["number_ratings"].str.replace(",", "")
    df["number_ratings"] = df["number_ratings"].astype(int)

    df["episode_count"] = df["episode_count"].str.replace(" episodes", "")
    df["episode_count"] = [0 if x == "" else x for x in df["episode_count"].values]
    df["episode_count"] = df["episode_count"].astype(int)

    return df


def split_list_into_df(df: pd.DataFrame, column_to_split: str) -> pd.DataFrame:

    temp_df = df[column_to_split].apply(pd.Series)
    temp_df.columns = [
        x + "_" + str(y)
        for x, y in zip(
            [column_to_split] * len(temp_df.columns), range(1, len(temp_df.columns) + 1)
        )
    ]
    temp_df = temp_df.apply(lambda x: x.str.strip())

    return temp_df


def clean_dataframe(df: pd.DataFrame, description_df: pd.DataFrame) -> pd.DataFrame:

    df = format_time_to_minutes(df, "duration")
    df["type"] = df["release"].apply(define_types)
    df = clean_release_column(df, "release")
    df = convert_money_columns(df, "budget")
    df = convert_money_columns(df, "cum_worldwide_gross")
    df = column_cleaning(df)
    df = get_movie_kind(df, description_df)
    df.drop(
        columns=[
            "stars",
            "country",
            "director",
            "writer",
            "creator",
            "genres",
            "plot_keywords",
            "currency",
            "currency_value",
        ],
        inplace=True,
    )

    return df
