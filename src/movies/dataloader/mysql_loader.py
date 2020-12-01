import time

import pyodbc

from movies.dataloader.mongodb_loader import read_mongo
from movies.dataprocessing.data_preprocessing import clean_dataframe

from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool

from movies.db_config import DB_SETTINGS

import logging


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
    except Exception as e:
        logging.info(
            "Something went wrong with the connection to MongoDB and the retrieving of data: {}".format(
                e
            )
        )
        return

    movie_df = clean_dataframe(df)

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
    logging.info("Process started at {}".format(start_time))

    run_once()

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))
