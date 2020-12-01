from flask import Flask, render_template

from movies.dataloader.mongodb_loader import read_mongo

app = Flask(__name__, template_folder='templates')


@app.route('/')
@app.route('/index')
def index():

    df = read_mongo("movies", "movie_data")
    data = df.head(10)
    return render_template("index.html", data=data)

