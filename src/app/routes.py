import ast

from flask import render_template, flash, url_for, request
import pandas as pd
import numpy as np
from werkzeug.utils import redirect

from app.models import Movies
from dataloader.mongodb_loader import read_mongo
from dataprocessing.machinelearningmodels import get_predictions
from app.forms import MovieSearchForm

from app import app


def get_movie(chosen_type, string_search, chosen_column):

    return Movies.query.filter(
        getattr(Movies, chosen_type).contains(string_search)
    ).order_by(chosen_column)


def get_key(val, tuple_to_search):

    dictionary = dict(tuple_to_search)

    for key, value in dictionary.items():
        if val == value:
            return key


@app.route("/", methods=["GET", "POST"])
def index():

    form = MovieSearchForm()
    results = None

    if form.validate_on_submit():

        chosen_type = form.chosen_type.data
        string_search = form.string_search.data
        chosen_column = form.chosen_column_order.data

        results = get_movie(chosen_type, string_search.strip(), chosen_column)

        if results.first() is not None:
            return redirect(
                url_for(
                    "search",
                    chosen_type=chosen_type,
                    string_search=string_search,
                    chosen_column=chosen_column,
                )
            )

        flash("No results.")

    return render_template(
        "index.html", results=results, form=form, title="Home - MovieDB"
    )


@app.route("/search/")
def search():

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")

    form = MovieSearchForm(
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column_order=chosen_column,
    )

    results = get_movie(chosen_type, string_search.strip(), chosen_column)

    return render_template(
        "search.html",
        results=results,
        form=form,
        title="Results - MovieDB",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
    )


@app.route("/details/<string:id>")
def details(id):

    df = read_mongo("movies", "movie_data")
    results = df.iloc[int(id)]

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")

    return render_template(
        "details.html",
        results=results,
        title="Details - MovieDB",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
    )


@app.route("/recommendations/<string:id>")
def recommendations(id):

    df = read_mongo("movies", "movie_data")

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")

    indexes = get_predictions(df, int(id))[0]
    indexes = np.delete(indexes, np.where(indexes == int(id)))
    results = df.iloc[indexes]
    initial_movie = df.iloc[int(id)]

    return render_template(
        "recommendations.html",
        initial_movie=initial_movie,
        results=results,
        title="Recommendations - MovieDB",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
    )
