import pandas as pd
import numpy as np

from movies.utils import TYPE_DATA


def define_types(value: str) -> str:

    val = "Other"

    for key in TYPE_DATA:
        if key in value:
            val = TYPE_DATA[key]
            break

    return val


def clean_release_column(df: pd.DataFrame, column: str) -> pd.DataFrame:

    df[column] = (
        df[column]
        .str.replace("TV Mini-Series ", "")
        .str.replace("TV Series ", "")
        .str.replace("TV Movie ", "")
        .str.replace("Video game released ", "")
        .str.replace("Episode aired ", "")
        .str.replace("Video ", "")
    )
    df[column] = [
        x.replace("(", "").replace(")", "") if x.startswith("(") else x
        for x in df[column].values
    ]

    return df


def get_movie_kind(main_df: pd.DataFrame, genre_df: pd.DataFrame) -> pd.DataFrame:

    cols = [x for x in genre_df.columns if "genres" in x]

    conditions = [
        (genre_df[cols] == "Short").any(axis="columns"),
        (genre_df[cols] == "Documentary").any(axis="columns"),
        (genre_df[cols] == "Animation").any(axis="columns"),
    ]

    choices = ["Short movie", "Documentary", "Animated movie"]

    main_df["kind"] = np.select(conditions, choices, default="Other")

    return main_df
