import pandas as pd
import pyodbc

from movies.db_config import PORT, PWD, UID, DATABASE, SERVER, DRIVER


def connect() -> pyodbc.Connection:

    server = "tcp:{}".format(SERVER)
    database = DATABASE
    username = UID
    password = PWD
    port = str(PORT)
    driver = DRIVER
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


connect().execute("USE movies")

df = pd.read_sql("SELECT * FROM movie_data", connect())
print(df)
