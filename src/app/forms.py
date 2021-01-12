from wtforms import StringField, SelectField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

from utils import FIELDS, COLUMNS, ORDER


class MovieSearchForm(FlaskForm):

    chosen_type = SelectField("Search: ", choices=FIELDS, validators=[DataRequired()])
    string_search = StringField("", validators=[DataRequired()])
    chosen_column_order = SelectField(
        " ordered by ", choices=COLUMNS, validators=[DataRequired()]
    )
    chosen_order = SelectField("", choices=ORDER, validators=[DataRequired()])
