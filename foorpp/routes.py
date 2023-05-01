from flask import (
    abort,
    flash,
    redirect,
    render_template,
    request,
    session,
    url_for
)
from foorpp import app, bcrypt, db
from foorpp.filters import filter_by_keyword
from foorpp.forms import AdminLoginForm
from foorpp.models import (
    AdminAccount,
    Category,
    CustomerSession,
    MenuItem,
    Order
)
from foorpp.utils import add_to_cart
from sqlalchemy import func


@app.route("/", methods = ["GET", "POST"])
def index():
    session.clear()

    if request.method == "POST":
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
        session["keyword"] = request.form.get("searched")
        return redirect(url_for("menu"))

    return render_template("categories.html",
                           categories = Category.query.all())


@app.route("/menu", methods = ["GET", "POST"])
def menu():
    if session.get("id") is None:
        return redirect(url_for("index"))

    keyword = session.get("keyword")
    menu_items = filter_by_keyword(keyword if keyword is None
                                   else keyword.strip().lower())

    if request.method == "POST":
        add_to_cart(request.form["item_id"])

    return render_template("menu.html", items = menu_items)


@app.post("/search")
def search():
    session["keyword"] = request.form["searched"]
    return redirect("menu")


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item(item_id):
    if session.get("id") is None:
        return redirect(url_for("index"))

    menu_item = MenuItem.query.get(item_id)
    if menu_item is None:
        abort(404)

    if request.method == "POST":
        add_to_cart(item_id)

    return render_template("item.html", item = menu_item)


@app.route("/cart", methods = ["GET", "POST"])
def cart():
    if session.get("id") is None:
        return redirect(url_for("index"))

    order = Order.get_current_order()

    return render_template("cart.html", order=order)


@app.post("/empty_cart")
def empty_cart():
    Order.query.get(session["order_id"]).empty_cart()
    return redirect(url_for("cart"))


@app.route("/order/<order_id>", methods = ["GET", "POST"])
def finalized_order(order_id):
    Order.query.get(order_id).status = "submitted"
    db.session.commit()

    if request.method == "POST" and "finish" in request.form:
        CustomerSession.query.get(session["id"]).end = func.now()
        return redirect(url_for("index"))

    return render_template("finalized_order.html",
                           order_num = int(order_id) % 100)


@app.route("/admin_login", methods = ["GET", "POST"])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        admin_account = AdminAccount.query.first()

        if admin_login and bcrypt.check_password_hash(admin_account.password,
                                                      form.password.data):
            session["id"] = "admin"
            return redirect(url_for("admin"))

        flash("Incorrect admin password!")

    return render_template("admin_login.html", form = form, )


@app.get("/admin")
def admin():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    return render_template("admin.html")


@app.route("/orders")
def orders():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    return "hahahaha"


@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html")
