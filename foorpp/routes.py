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

    if request.method == "POST":
        if "searched" in request.form:
            filter_arg = request.form["searched"]
        else:
            filter_arg = ""

        flash(filter_arg)
        return redirect(url_for("menu"))

    return render_template("categories.html",
                           categories = Category.query.all())


@app.route("/admin_login")
def admin_login():
    return render_template("admin_login.html")


@app.route("/menu", methods = ["GET", "POST"])
def menu():
    if "id" not in session:
        return redirect(url_for("index"))

    filter_arg = ""
    data = get_flashed_messages()
    if data:
        filter_arg = data[0]

    search = SearchForm()
    menu_items = filter_by_keyword(filter_arg.strip().lower())

    return render_template("menu.html", items = menu_items)


@app.route("/search", methods = ["POST"])
def search():
    flash(request.form["searched"])
    return redirect("menu")


@app.route("/item/<item_id>")
def item(item_id):
    if "id" not in session:
        return redirect(url_for("index"))

    menu_item = MenuItem.query.filter(MenuItem.id == item_id).first()
    if menu_item is None:
        abort(404)

    return render_template("item.html", item = menu_item)


@app.route("/cart")
def cart():
    if "id" not in session:
        return redirect(url_for("index"))

    return render_template("cart.html")


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html")
