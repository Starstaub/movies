from flask import Flask, render_template, request, flash
import pandas as pd
import numpy as np
from movies.dataloader.mongodb_loader import read_mongo
from movies.site.app.forms import MovieSearchForm

app = Flask(__name__, template_folder='templates')

app.config['SECRET_KEY'] = "niceapp"
WTF_CSRF_SECRET_KEY = "niceapp"


@app.route('/', methods=['GET', 'POST'])
def index():
    df = read_mongo("movies", "movie_data")
    df = df.replace(np.NaN, "")
    form = MovieSearchForm()
    results = pd.DataFrame()
    if form.validate_on_submit():
        choice = form.choice.data
        string_search = form.string_search.data
        if choice == "movie_title":
            results = df[df[choice].str.contains(string_search)]
            if results.empty:
                flash("No results.")
        if choice == "director" or choice == "genres" or choice == "stars":
            results = df[df[choice].map({string_search}.issubset)]
            if results.empty:
                flash("No results.")
    return render_template("index.html", results=results, form=form)

