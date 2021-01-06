from ast import literal_eval

from app.models import Movies
import pandas as pd


def get_movie(chosen_type, string_search, chosen_column):

    return Movies.query.filter(
        getattr(Movies, chosen_type).contains(string_search)
    ).order_by(chosen_column)


def clean_list_results(results):

    list_results = pd.DataFrame(
        {
            "stars": [results.stars],
            "director": [results.director],
            "plot_keywords": [results.plot_keywords],
            "writer": [results.writer],
            "creator": [results.creator],
            "genres": [results.genres],
            "country": [results.country],
        }
    )

    for col in list_results.columns:
        list_results[col] = list_results[col].apply(literal_eval)

    return list_results
