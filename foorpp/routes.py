from flask import (
    abort,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from foorpp import app, db
from foorpp.forms import SearchForm
from foorpp.filters import filter_by_keyword
from foorpp.models import Category, MenuItem, CustomerSession
from sqlalchemy import func


@app.route("/", methods = ["GET", "POST"])
def index():
    if "id" in session:
        CustomerSession.query.filter(CustomerSession.id == session["id"]).first().end = func.now()
        session.pop("id", None)

    if request.method == "POST":
        if request.form.get("admin_login_btn"):
            return redirect(url_for("admin_login"))

        if request.form.get("get_started_btn"):
            new_session = CustomerSession()
            db.session.add(new_session)
            db.session.commit()

            session["id"] = new_session.id

            return redirect(url_for("categories"))

    return render_template("index.html")


@app.route("/categories", methods = ["GET", "POST"])
def categories():
    if "id" not in session:
        return redirect(url_for("index"))

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
    if "id" not in session:
        return redirect(url_for("index"))

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
    if "id" not in session:
        return redirect(url_for("index"))

    search = SearchForm()
    menu_item = MenuItem.query.filter(MenuItem.id == item_id).first()
    if menu_item is None:
        abort(404)

    return render_template("item.html", search = search, item = menu_item)


@app.errorhandler(404)
def page_not_found(_):
    search = SearchForm()
    return render_template("404.html", search = search)
