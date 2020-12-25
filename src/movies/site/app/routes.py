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
    data = MovieSearchForm()
    results = pd.DataFrame()
    if data.validate_on_submit():
        choice = data.choice.data
        string_search = data.string_search.data
        if choice == "movie_title":
            results = df[df[choice].str.contains(string_search)]
            if results.empty:
                flash("No results.")
        if choice == "director" or choice == "genres" or choice == "stars":
            results = df[df[choice].map({string_search}.issubset)]
            if results.empty:
                flash("No results.")

    return render_template("index.html", results=results, data=data)


@app.route("/details/<id>")
def details(id):
    df = read_mongo("movies", "movie_data")
    results = df.iloc[int(id)]

    return render_template("details.html", results=results)


@app.route("/recommendations/<id>")
def recommendations(id):
    df = read_mongo("movies", "movie_data")
    indexes = get_predictions(df, int(id))[0]
    indexes = np.delete(indexes, np.where(indexes == int(id)))
    results = df.iloc[indexes]
    initial_movie = df.iloc[int(id)]

    return render_template(
        "recommendations.html", initial_movie=initial_movie, results=results
    )
