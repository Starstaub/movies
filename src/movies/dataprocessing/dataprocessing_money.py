import pandas as pd

from utils import CURRENCY_VALUES


def determine_currencies(df: pd.DataFrame, money_column: str) -> pd.DataFrame:

    df["currency"] = df[money_column].str.extract(r'([a-zA-Z\$]+)')

    df["currency_value"] = df["currency"].map(CURRENCY_VALUES).astype(float)

    return df


def convert_money_columns(df: pd.DataFrame, money_column: str) -> pd.DataFrame:

    df[money_column] = df[money_column].str.replace(",", "")
    df = determine_currencies(df, money_column)

    df[money_column] = df[money_column].str.extract(r'(\d+)').astype(float)
    df[money_column] = df[money_column] * df["currency_value"]

    return df
