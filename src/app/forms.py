from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from utils import FIELDS, ORDER


class MovieSearchForm(FlaskForm):

    chosen_type = SelectField("Search: ", choices=FIELDS, validators=[DataRequired()])
    string_search = StringField("", validators=[DataRequired()])
    chosen_column_order = SelectField(
        " ordered by ", choices=ORDER, validators=[DataRequired()]
    )
