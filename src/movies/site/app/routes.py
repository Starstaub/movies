import ast

from flask import Flask, render_template, flash
import pandas as pd
import numpy as np

from movies.dataloader.mongodb_loader import read_mongo
from movies.dataprocessing.machinelearningmodels import get_predictions
from movies.site.app.forms import MovieSearchForm

app = Flask(__name__, template_folder="templates")

app.config["SECRET_KEY"] = "niceapp"
WTF_CSRF_SECRET_KEY = "niceapp"


@app.route("/", methods=["GET", "POST"])
def index():
    df = read_mongo("movies", "movie_data")
    df = df.replace(np.NaN, "")
    form = MovieSearchForm()
    results = pd.DataFrame()
    if form.validate_on_submit():
        chosen_type = form.chosen_type.data
        string_search = form.string_search.data
        chosen_column = form.chosen_column_order.data
        if chosen_type == "movie_title":
            results = df[
                df[chosen_type].str.lower().str.contains(string_search.lower())
            ].sort_values(by=chosen_column)
            if results.empty:
                flash("No results.")
        if (
            chosen_type == "director"
            or chosen_type == "genres"
            or chosen_type == "stars"
        ):
            results = df[
                df[chosen_type]
                .astype(str)
                .str.lower()
                .transform(ast.literal_eval)
                .map({string_search.lower()}.issubset)
            ].sort_values(by=chosen_column)
            if results.empty:
                flash("No results.")

    return render_template("index.html", results=results, form=form, title="Home - MovieDB")


@app.route("/details/<id>")
def details(id):
    df = read_mongo("movies", "movie_data")
    results = df.iloc[int(id)]

    return render_template("details.html", results=results, title="Details - MovieDB")


@app.route("/recommendations/<id>")
def recommendations(id):
    df = read_mongo("movies", "movie_data")
    indexes = get_predictions(df, int(id))[0]
    indexes = np.delete(indexes, np.where(indexes == int(id)))
    results = df.iloc[indexes]
    initial_movie = df.iloc[int(id)]

    return render_template(
        "recommendations.html", initial_movie=initial_movie, results=results, title="Recommendations - MovieDB"
    )
