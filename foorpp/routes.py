from flask import flash, get_flashed_messages, redirect, render_template, request, url_for
from foorpp import app
from foorpp.forms import SearchForm
from foorpp.filters import filtered_items
from foorpp.models import Category, MenuItem


@app.route("/", methods = ["GET", "POST"])
def index():
    if request.method == "POST":
        if request.form.get("admin_login_btn"):
            return redirect(url_for("admin_login"))

        if request.form.get("get_started_btn"):
            return redirect(url_for("categories"))

    return render_template("index.html")


@app.route("/categories", methods = ["GET", "POST"])
def categories():
    search = SearchForm()

    if request.method == "POST":
        if search.validate_on_submit():
            filter_arg = search.data["search"]
        elif "category_button" in request.form:
            filter_arg = request.form["category_button"]
        else:
            filter_arg = ""

        flash({"filter_arg": filter_arg})
        return redirect(url_for("menu"))

    return render_template("categories.html", search = search,
                           categories = Category.query.all())


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html", )


@app.route("/menu/", methods = ["GET", "POST"])
def menu():
    filter_arg = ""
    data = get_flashed_messages()
    if data:
        filter_arg = data[0]["filter_arg"]

    search = SearchForm()
    menu_items = filtered_items(filter_arg.strip().lower())

    return render_template("menu.html", search = search, filter_arg = filter_arg,
                           items = menu_items)


# @app.before_first_request
# def create_tables():
#     db.create_all()
#     # db.session.add(Category(name="pizza", value="Pizza"))
#     # db.session.add(Category(name="burger", value="Burger"))
#     # db.session.add(Category(name="sushi", value="Sushi"))
#     # db.session.commit()
