import pandas as pd

from utils import TYPE_DATA


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
