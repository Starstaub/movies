import ast

from flask import Flask, render_template, flash, url_for, request
import pandas as pd
import numpy as np
from werkzeug.utils import redirect

from movies.dataloader.mongodb_loader import read_mongo
from movies.dataprocessing.machinelearningmodels import get_predictions
from movies.site.app.forms import MovieSearchForm

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = "niceapp"
WTF_CSRF_SECRET_KEY = "niceapp"


def get_movie(df, chosen_type, string_search, chosen_column):

    if chosen_type == "movie_title":
        return df[
            df[chosen_type].str.lower().str.contains(string_search.lower())
        ].sort_values(by=chosen_column)

    else:
        return df[
            df[chosen_type]
            .astype(str)
            .str.lower()
            .transform(ast.literal_eval)
            .map({string_search.lower()}.issubset)
        ].sort_values(by=chosen_column)


def get_key(val, tuple_to_search):

    dictionary = dict(tuple_to_search)

    for key, value in dictionary.items():
        if val == value:
            return key


@app.route("/", methods=["GET", "POST"])
def index():

    df = read_mongo("movies", "movie_data")
    form = MovieSearchForm()
    results = pd.DataFrame()

    if form.validate_on_submit():
        chosen_type = form.chosen_type.data
        string_search = form.string_search.data
        chosen_column = form.chosen_column_order.data

        results = get_movie(df, chosen_type, string_search.strip(), chosen_column)

        if not results.empty:
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

    df = read_mongo("movies", "movie_data")
    form = MovieSearchForm(
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column_order=chosen_column,
    )

    results = get_movie(df, chosen_type, string_search.strip(), chosen_column)

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
