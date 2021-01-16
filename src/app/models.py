from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login


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
        return f"<Movie {self.movie_title}>"


class User(UserMixin, db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
