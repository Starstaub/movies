from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired


class MovieSearchForm(Form):

    fields = [('director', 'Director'),
               ('movie_title', 'Title'),
               ('genres', 'Genre'),
              ('stars', 'Actor')
              ]
    choice = SelectField('', choices=fields, validators=[DataRequired()])
    string_search = StringField('', validators=[DataRequired()])
