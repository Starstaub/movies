from flask import Flask, render_template

from movies.dataloader.mongodb_loader import read_mongo
from movies.dataprocessing.machinelearningmodels import get_predictions

app = Flask(__name__, template_folder='templates')


@app.route('/')
@app.route('/index')
def index():

    df = read_mongo("movies", "movie_data")
    # df = df.dropna(subset=['imdb_score'])
    array = get_predictions(df, 125)[0]
    data = df.iloc[array].reset_index(drop=True)

    return render_template("index.html", data=data)

