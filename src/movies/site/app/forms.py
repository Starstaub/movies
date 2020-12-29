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
    order = [
        ("index", "Default"),
        ("title_year", "Year"),
        ("movie_title", "Title"),
        ("imdb_score", "IMDB Score")
    ]

    chosen_type = SelectField("Search:", choices=fields, validators=[DataRequired()])
    string_search = StringField("", validators=[DataRequired()])
    chosen_column_order = SelectField("ordered by", choices=order, validators=[DataRequired()])
