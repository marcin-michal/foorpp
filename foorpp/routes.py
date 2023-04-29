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
from foorpp.filters import filter_by_keyword
from foorpp.models import Category, CustomerSession, MenuItem, Order
from sqlalchemy import func


@app.route("/", methods = ["GET", "POST"])
def index():
    session.clear()
    if "id" in session:
        if session["id"] is not None:
            CustomerSession.query.get(session["id"]).end = func.now()
        session.clear()

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
    if session.get("id") is None:
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
    if session.get("id") is None:
        return redirect(url_for("index"))

    filter_arg = ""
    data = get_flashed_messages()
    if data:
        filter_arg = data[0]

    menu_items = filter_by_keyword(filter_arg.strip().lower())

    return render_template("menu.html", items = menu_items)


@app.post("/search")
def search():
    flash(request.form["searched"])
    return redirect("menu")


@app.route("/item/<item_id>")
def item(item_id):
    if session.get("id") is None:
        return redirect(url_for("index"))

    menu_item = MenuItem.query.get(item_id)
    if menu_item is None:
        abort(404)

    return render_template("item.html", item = menu_item)


@app.route("/cart", methods = ["GET", "POST"])
def cart():
    if session.get("id") is None:
        return redirect(url_for("index"))

    order = Order.get_current_order()

    return render_template("cart.html", order=order)


@app.post("/add_to_cart/<origin>/<item_id>")
def add_to_cart(origin, item_id):
    order = Order.get_current_order()
    order.add_item(MenuItem.query.get(item_id))
    db.session.commit()

    if (origin == "item"):
        return redirect(url_for("item", item_id = item_id))

    return redirect(url_for("menu"))


@app.post("/empty_cart")
def empty_cart():
    Order.query.get(session["order_id"]).empty_cart()
    return redirect(url_for("cart"))


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html")
