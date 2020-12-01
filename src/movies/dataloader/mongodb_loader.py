import time

import pandas as pd
from pymongo import MongoClient
import logging

from pymongo.database import Database
from pymongo.errors import OperationFailure

from movies.dataprocessing.data_preprocessing import clean_dataframe


def _connect_mongo(
        host: str,
        port: int,
        username: str,
        password: str,
        database: str
) -> Database:

    if username and password:
        mongo_uri = "mongodb://%s:%s@%s:%s/%s" % (
            username,
            password,
            host,
            port,
            database,
        )
        cnxn = MongoClient(mongo_uri)
    else:
        cnxn = MongoClient(host, port)

    return cnxn[database]


def read_mongo(
    database,
    collection,
    query=None,
    host="localhost",
    port=27017,
    username=None,
    password=None,
    no_id=True,
) -> pd.DataFrame:

    if query is None:
        query = {}
    database = _connect_mongo(
        host=host, port=port, username=username, password=password, database=database
    )
    cursor = database[collection].find(query)
    df = pd.DataFrame(list(cursor))

    if no_id:
        del df["_id"]

    return df


def run_once(
    database,
    collection,
    host="localhost",
    port=27017,
    username=None,
    password=None,
) -> bool:

    try:
        df = read_mongo(database, collection)
    except OperationFailure:
        logging.info(
            """Something went wrong with the connection
             to MongoDB and the retrieving of data"""
        )
        return False

    database = _connect_mongo(
        host=host, port=port, username=username, password=password, database=database
    )

    cursor = database[collection]
    _ = cursor.delete_many({})

    movie_data = clean_dataframe(df).to_dict("records")
    cursor.insert_many(movie_data)

    return True


if __name__ == "__main__":

    start_time = time.time()
    logging.info("Process started at %s", start_time)

    run_once("movies", "movie_data")

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))
