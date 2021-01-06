import os
import logging
import time

from sqlalchemy import create_engine

from dataloader.mongodb_loader import read_mongo

basedir = os.path.abspath(os.path.dirname(__file__))


def run_once() -> bool:

    try:
        df = read_mongo("movies", "movie_data")
        print(df.columns)
    except Exception as e:
        logging.info(
            "Something went wrong with the connection to MongoDB and the retrieving of data: {}".format(
                e
            )
        )
        return False

    engine = create_engine(
        "sqlite:///" + "/Users/mary/git/movies/src/app.db", echo=False
    )

    df[["stars", "director", "creator", "writer", "plot_keywords", "genres", "country"]] = df[["stars", "director", "creator", "writer", "plot_keywords", "genres", "country"]].astype(str)

    df.to_sql(
        name="movies",
        con=engine,
        if_exists="replace",
        chunksize=1000,
    )

    return True


if __name__ == "__main__":

    start_time = time.time()
    logging.info("Process started at {}".format(start_time))

    run_once()

    print("--- %s minute(s) ---" % ((time.time() - start_time) / 60))