from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm


class MovieSearchForm(FlaskForm):

    fields = [
        ("director", "Director"),
        ("movie_title", "Title"),
        ("genres", "Genre"),
        ("stars", "Actor"),
    ]
    choice = SelectField("Pick one:", choices=fields, validators=[DataRequired()])
    string_search = StringField("Search:", validators=[DataRequired()])
