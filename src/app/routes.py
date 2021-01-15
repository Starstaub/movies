from datetime import datetime

from flask import render_template, flash, url_for, request
from flask_login import current_user, logout_user, login_user
from werkzeug.urls import url_parse
from werkzeug.utils import redirect

from app.models import Movies, User
from app.modules import get_movie, clean_list_results, clean_ml_food, clean_lists
from dataprocessing.machinelearningmodels import get_predictions
from app.forms import MovieSearchForm, LoginForm, RegistrationForm

from app import app, db
from utils import FIELDS


@app.route("/", methods=["GET", "POST"])
def index():

    form = MovieSearchForm()
    results = None

    if form.validate_on_submit():

        chosen_type = form.chosen_type.data
        string_search = form.string_search.data
        chosen_column = form.chosen_column_order.data
        chosen_order = form.chosen_order.data

        results = get_movie(chosen_type, string_search.strip(), chosen_column, chosen_order)

        if results.first() is not None:
            return redirect(
                url_for(
                    "search",
                    chosen_type=chosen_type,
                    string_search=string_search,
                    chosen_column=chosen_column,
                    chosen_order=chosen_order,
                )
            )

        types = dict(FIELDS)
        flash("No results for '{}' in category '{}'.".format(string_search.strip(), types[chosen_type]))

    return render_template(
        "index.html", results=results, form=form, title="Home"
    )


@app.route("/search/")
def search():

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")
    chosen_order = request.args.get("chosen_order")

    form = MovieSearchForm(
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column_order=chosen_column,
        chosen_order=chosen_order,
    )

    page = request.args.get("page", 1, type=int)
    data = get_movie(chosen_type, string_search.strip(), chosen_column, chosen_order)
    results = data.paginate(
        page, app.config["POSTS_PER_PAGE"], False
    )
    count = data.count()
    next_url = (
        url_for(
            "search",
            chosen_type=chosen_type,
            string_search=string_search,
            chosen_column=chosen_column,
            chosen_order=chosen_order,
            page=results.next_num,
        )
        if results.has_next
        else None
    )
    prev_url = (
        url_for(
            "search",
            chosen_type=chosen_type,
            string_search=string_search,
            chosen_column=chosen_column,
            chosen_order=chosen_order,
            page=results.prev_num,
        )
        if results.has_prev
        else None
    )

    return render_template(
        "search.html",
        results=results.items,
        form=form,
        count=count,
        next_url=next_url,
        prev_url=prev_url,
        page=results.page,
        pages=results.pages,
        title="Results",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
        chosen_order=chosen_order,
    )


@app.route("/details/<string:id>")
def details(id):

    results = Movies.query.filter(Movies.index == int(id)).first()

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")
    chosen_order = request.args.get("chosen_order")
    page = request.args.get("page", 1, type=int)

    list_results = clean_list_results(results)

    return render_template(
        "details.html",
        results=results,
        list_results=list_results,
        title="Details",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
        chosen_order=chosen_order,
        page=page,
    )


@app.route("/recommendations/<string:id>")
def recommendations(id):

    results = Movies.query.with_entities(
        Movies.index, Movies.genres, Movies.certificate, Movies.imdb_score
    ).all()
    df = clean_ml_food(results)

    chosen_type = request.args.get("chosen_type")
    string_search = request.args.get("string_search")
    chosen_column = request.args.get("chosen_column")
    chosen_order = request.args.get("chosen_order")
    page = request.args.get("page", 1, type=int)

    indexes = get_predictions(df, int(id))[0]
    indexes = [str(i) for i in indexes if i != int(id)]

    results = Movies.query.filter(Movies.index.in_(indexes)).all()
    results = [next(s for s in results if s.index == int(idx)) for idx in indexes]
    initial_movie = Movies.query.filter(Movies.index == int(id)).first()

    list_initial_movie = clean_lists(initial_movie)

    return render_template(
        "recommendations.html",
        initial_movie=initial_movie,
        results=results,
        list_initial_movie=list_initial_movie,
        title="Recommendations",
        chosen_type=chosen_type,
        string_search=string_search,
        chosen_column=chosen_column,
        chosen_order=chosen_order,
        page=page,
    )


@app.route("/login", methods=["GET", "POST"])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password.")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
            flash(f"Welcome back {user.username}!")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    flash("You have been successfully logged out. Until next time!")
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():

    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for('login'))
    return render_template("register.html", title="Create your account", form=form)


@app.before_request
def before_request():

    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
