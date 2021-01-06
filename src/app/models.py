from app import db


class Movies(db.Model):

    index = db.Column(db.Integer, primary_key=True)
    original_title = db.Column(db.String(150))
    duration = db.Column(db.Integer)
    release = db.Column(db.String(30))
    storyline = db.Column(db.Text)
    stars = db.Column(db.String(100))
    creator = db.Column(db.String(50))
    genres = db.Column(db.String(150))
    plot_keywords = db.Column(db.String(150))
    certificate = db.Column(db.String(10))
    movie_title = db.Column(db.String(150))
    title_year = db.Column(db.String(5))
    imdb_score = db.Column(db.String(4))
    number_ratings = db.Column(db.String(20))
    director = db.Column(db.String(50))
    writer = db.Column(db.String(50))
    episode_count = db.Column(db.String(15))
    country = db.Column(db.String(50))
    budget = db.Column(db.Integer)
    cum_worldwide_gross = db.Column(db.Integer)
    poster = db.Column(db.String(250))
    big_poster = db.Column(db.String(250))
    type = db.Column(db.String(20))

    def __repr__(self):
        return '<Movie {}>'.format(self.movie_title)
