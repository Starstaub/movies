import pandas as pd
from pymongo import MongoClient


def _connect_mongo(host, port, username, password, database):

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
):

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
