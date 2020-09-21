import time

import logging

import pandas as pd
import pyodbc
from pymongo.errors import OperationFailure

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from movies.dataloader.mongodb_loader import read_mongo
from movies.dataprocessing.data_preprocessing import clean_dataframe, split_list_into_df
from movies.db_config import DB_SETTINGS


def connect() -> pyodbc.Connection:

    server = "tcp:{}".format(DB_SETTINGS["SERVER"])
    database = DB_SETTINGS["DATABASE"]
    username = DB_SETTINGS["UID"]
    password = DB_SETTINGS["PWD"]
    port = str(DB_SETTINGS["PORT"])
    driver = DB_SETTINGS["DRIVER"]
    cnxn = pyodbc.connect(
        "DRIVER="
        + driver
        + ";SERVER="
        + server
        + ";PORT="
        + port
        + ";DATABASE="
        + database
        + ";UID="
        + username
        + ";PWD="
        + password
    )
    return cnxn


def run_once():

    try:
        df = read_mongo("movies", "movie_data")
    except OperationFailure:
        logging.info(
            """Something went wrong with the connection
             to MongoDB and the retrieving of data"""
        )

    description_df = (
        pd.concat(
            [split_list_into_df(df, "genres"), split_list_into_df(df, "plot_keywords")],
            axis=1,
            sort=False,
        )
        .reset_index()
        .rename(columns={"index": "idx"})
    )

    creation_df = (
        pd.concat(
            [
                split_list_into_df(df, "director"),
                split_list_into_df(df, "writer"),
                split_list_into_df(df, "creator"),
            ],
            axis=1,
            sort=False,
        )
        .reset_index()
        .rename(columns={"index": "idx"})
    )

    country_stars_df = (
        pd.concat(
            [split_list_into_df(df, "stars"), split_list_into_df(df, "country")],
            axis=1,
            sort=False,
        )
        .reset_index()
        .rename(columns={"index": "idx"})
    )

    movie_df = clean_dataframe(df, description_df.copy())

    try:
        cnxn = connect()
    except pyodbc.OperationalError:
        logging.info("Something went wrong with the connection to mssql.")

    engine = create_engine(
        "mssql+pyodbc://",
        poolclass=StaticPool,
        creator=lambda: cnxn,
        fast_executemany=True,
    )

    description_df.to_sql(
        name="description_df",
        con=engine,
        schema="dbo",
        index=False,
        if_exists="append",
        chunksize=1000,
    )

    creation_df.to_sql(
        name="creation_df",
        con=engine,
        schema="dbo",
        index=False,
        if_exists="append",
        chunksize=1000,
    )

    country_stars_df.to_sql(
        name="country_stars_df",
        con=engine,
        schema="dbo",
        index=False,
        if_exists="append",
        chunksize=1000,
    )

    movie_df.to_sql(
        name="movie_df",
        con=engine,
        schema="dbo",
        index=False,
        if_exists="append",
        chunksize=1000,
    )


if __name__ == "__main__":

    start_time = time.time()
    logging.info("Process started at %s", start_time)

    run_once()

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))
