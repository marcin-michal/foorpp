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
from foorpp.filters import filtered_items
from foorpp.forms import (
    AdminLoginForm,
    CategoryAddForm,
    FilterForm,
    MenuItemForm,
    OrderStatusForm
)
from foorpp.models import (
    AdminAccount,
    Category,
    CustomerSession,
    MenuItem,
    Order,
    order_items
)
from foorpp.utils import add_to_cart, clear_filters, selected_categories
from sqlalchemy import func


@app.route("/", methods=["GET", "POST"])
def index():
    session.clear()

    if request.method == "POST":
        new_session = CustomerSession()
        db.session.add(new_session)
        db.session.commit()

        session["id"] = new_session.id

        return redirect(url_for("categories"))

    return render_template("index.html")


@app.route("/categories", methods=["GET", "POST"])
def categories():
    if session.get("id") is None:
        return redirect(url_for("index"))

    clear_filters(session)

    if request.method == "POST":
        category = request.form.get("category")
        session["categories"] = [] if category == "Show me everything!" \
            else [Category.query.filter(Category.name == category).first().id]
        session["keyword"] = None

        return redirect(url_for("menu"))

    return render_template("categories.html", id=session["id"],
                           categories=Category.query.all(), back_page="index")


@app.route("/menu", methods=["GET", "POST"])
def menu():
    if session.get("id") is None:
        return redirect(url_for("index"))

    back_page = "admin" if session["id"] == "admin" else "categories"
    menu_items = filtered_items(
        session.get("categories"),
        session.get("keyword"),
        session.get("diets"),
        session.get("excluded_allergens"),
        session.get("ordering")
    )

    if request.method == "POST":
        add_to_cart(request.form["item_id"])

    return render_template("menu.html", items=menu_items, id=session["id"],
                           back_page=back_page)


@app.post("/search")
def search():
    clear_filters(session)
    session["keyword"] = request.form["searched"]

    return redirect(url_for("menu"))


@app.route("/item/<item_id>", methods=["GET", "POST"])
def item(item_id):
    if session.get("id") is None:
        return redirect(url_for("index"))

    menu_item = MenuItem.query.get(item_id)
    if menu_item is None:
        abort(404)

    form = MenuItemForm(obj=menu_item)
    if form.validate_on_submit():
        menu.item = menu_item.update(form, request.files.get("image"))
        return redirect(url_for("menu"))
    elif "add_to_cart" in request.form:
        add_to_cart(item_id)
    elif "remove_item" in request.form:
        menu_item.remove()
        return redirect(url_for("menu"))

    return render_template("item.html", item=menu_item, form=form,
                           id=session["id"], back_page="menu")


@app.route("/cart", methods=["GET", "POST"])
def cart():
    if session.get("id") is None:
        return redirect(url_for("index"))

    current_order = Order.get_current_order()

    if request.method == "POST" and "edit_item" in request.form:
        data = request.form["edit_item"]
        operation = data[0]
        current_item = MenuItem.query.get(data[1:])

        if operation == "i":
            current_order.add_item(current_item)
        elif operation == "d":
            current_order.decrease_item(current_item, 1)
        elif operation == "r":
            count = db.session.query(order_items).filter(
                order_items.c.order_id==current_order.id,
                order_items.c.item_id==current_item.id
            ).first().count

            current_order.decrease_item(current_item, count)

    item_counts = current_order.get_item_counts()

    return render_template("cart.html", order=current_order, back_page="menu",
                           id=session["id"], item_counts=item_counts)


@app.post("/empty_cart")
def empty_cart():
    Order.query.get(session["order_id"]).empty_cart()
    return redirect(url_for("cart"))


@app.route("/order/<order_id>", methods=["GET", "POST"])
def finalized_order(order_id):
    if session.get("id") is None:
        return redirect(url_for("index"))

    current_order = Order.query.get(order_id)
    current_order.status = "submitted"
    current_order.time = func.now()
    db.session.commit()

    if request.method == "POST" and "finish" in request.form:
        CustomerSession.query.get(session["id"]).end = func.now()
        return redirect(url_for("index"))

    return render_template("finalized_order.html",
                           order_num=int(order_id) % 100)


@app.route("/admin-login", methods=["GET", "POST"])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        admin_account = AdminAccount.query.first()

        if admin_login and bcrypt.check_password_hash(admin_account.password,
                                                      form.password.data):
            session["id"] = "admin"

            return redirect(url_for("admin"))

        flash("Incorrect admin password!")

    return render_template("admin_login.html", form=form)


@app.get("/admin")
def admin():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    return render_template("admin.html")


@app.route("/orders")
def orders():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    orders = Order.query.all()

    return render_template("orders.html", id=session["id"], orders=orders,
                           back_page="admin")


@app.route("/add-menu-item", methods=["GET", "POST"])
def add_menu_item():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    form = MenuItemForm()
    if form.validate_on_submit():
        MenuItem().create(form, request.files.get("image"))
        return redirect(url_for("menu"))

    return render_template("add_menu_item.html", form=form, back_page="menu",
                           id=session["id"])


@app.route("/category-manager", methods=["GET", "POST"])
def category_manager():
    if session.get("id") != "admin":
        return redirect(url_for("index"))

    form = CategoryAddForm()
    if form.validate_on_submit():
        Category.create(form.name.data)
    elif "remove_category" in request.form:
        Category.query.filter(Category.id == request.form["remove_category"]).delete()
        db.session.commit()

    categories = Category.query.all()

    return render_template("category_manager.html", categories=categories,
                           form=form, back_page="admin", id=session["id"])


@app.route("/order-manager/<order_id>", methods=["GET", "POST"])
def order_manager(order_id):
    if session["id"] != "admin":
        return redirect(url_for("index"))

    current_order = Order.query.get(order_id)
    if current_order is None:
        abort(404)

    form = OrderStatusForm()
    if form.validate():
        current_order.status = form.status.data
        db.session.commit()
        return redirect(url_for("order_manager", order_id=order_id))

    return render_template("order.html", back_page="orders", id=session["id"],
                           order=current_order, form=form)


@app.route("/filter-items", methods=["GET", "POST"])
def filter_items():
    if session.get("id") is None:
        return redirect(url_for("index"))

    form = FilterForm(data={
        "categories": selected_categories(session.get("categories")),
        "diets": [] if session.get("diets") is None else session.get("diets"),
        "allergens": [] if session.get("excluded_allergens") is None
            else session.get("excluded_allergens"),
        "ordering": session.get("ordering")
    })
    form.categories.query = Category.query.all()

    if form.validate_on_submit():
        session["categories"] = [cat.id for cat in form.categories.data]
        session["diets"] = form.diets.data
        session["excluded_allergens"] = form.excluded_allergens.data
        session["ordering"] = form.ordering.data

        return redirect(url_for("menu"))

    return render_template("filter_items.html", form=form, back_page="menu")

@app.route("/clear-filters/<back_page>")
def clear_filters_button(back_page):
    if session.get("id") is None:
        return redirect(url_for("index"))

    clear_filters(session)
    return redirect(url_for(back_page))

@app.errorhandler(404)
def page_not_found(_):
    return render_template("404.html", back_page="index")
