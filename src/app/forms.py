from flask_login import current_user
from wtforms import StringField, SelectField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, Length
from flask_wtf import FlaskForm

from app.models import User
from utils import FIELDS, COLUMNS, ORDER


class MovieSearchForm(FlaskForm):

    chosen_type = SelectField("Search: ", choices=FIELDS, validators=[DataRequired()])
    string_search = StringField("", validators=[DataRequired()])
    chosen_column_order = SelectField(
        " ordered by ", choices=COLUMNS, validators=[DataRequired()]
    )
    chosen_order = SelectField("", choices=ORDER, validators=[DataRequired()])


class LoginForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")


class RegistrationForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired()])
    password2 = PasswordField("Repeat Password", validators=[DataRequired(), EqualTo("password")])
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(f"'{username.data}' is already used. Please choose a different username.")

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(f"'{email.data}' is already used. Please choose a different e-mail.")


class EditProfileForm(FlaskForm):

    username = StringField("Username", validators=[DataRequired()])
    about_me = TextAreaField("About me", validators=[Length(min=0, max=140)])
    submit = SubmitField("Submit")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None and current_user.username != username.data:
            raise ValidationError(f"'{username.data}' is already used.")
