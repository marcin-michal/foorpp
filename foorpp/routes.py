from flask import (
    abort,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for
)
from foorpp import app
from foorpp.forms import SearchForm
from foorpp.filters import filter_by_keyword
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
    menu_items = filter_by_keyword(filter_arg.strip().lower())

    return render_template("menu.html", search = search, filter_arg = filter_arg,
                           items = menu_items)


@app.route("/item/<item_id>")
def item(item_id):
    search = SearchForm()
    menu_item = MenuItem.query.filter(MenuItem.id == item_id).first()
    if menu_item is None:
        abort(404)

    return render_template("item.html", search = search, item = menu_item)


@app.errorhandler(404)
def page_not_found(e):
    search = SearchForm()
    return render_template("404.html", search = search)
