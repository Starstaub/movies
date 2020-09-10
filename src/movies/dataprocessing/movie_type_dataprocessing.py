from movies.utils import TYPE_DATA

import pandas as pd


def define_types(value):

    val = "Others"

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
    )
    df[column] = [
        x.replace("(", "").replace(")", "") if x.startswith("(") else x
        for x in df[column].values
    ]

    return df
