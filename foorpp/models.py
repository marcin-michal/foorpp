from decimal import Decimal
from flask import session, url_for
from foorpp import app, db
from functools import total_ordering
from sqlalchemy import func
from werkzeug.utils import secure_filename
import os
import uuid


DEFAULT_IMAGE = "images/default.jpg"


order_items = db.Table("order_items",
                       db.Column("order_id", db.Integer, db.ForeignKey("order.id")),
                       db.Column("item_id", db.Integer, db.ForeignKey("menu_item.id")),
                       db.Column("count", db.Integer, default=1))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    menu_items = db.relationship("MenuItem", backref="category")

    def __repr__(self):
        return self.name


    @staticmethod
    def create(name):
        category = Category(name=name)

        db.session.add(category)
        db.session.commit()

        return category


    @staticmethod
    def get_category_by_name(name):
        category = Category.query.get(name)

        if category is None:
            category = Category.create(name)

        return category


    def add_item(self, item):
        self.menu_items.append(item)


    def remove_item(self, item):
        self.menu_items.remove(item)

        if len(self.menu_items) == 0:
            db.session.delete(self)


@total_ordering
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(50), nullable=False,
                      default=DEFAULT_IMAGE)
    tags = db.Column(db.String, default="")
    allergens = db.Column(db.String, default="")
    category_id = db.Column(db.Integer, db.ForeignKey("category.id"))


    @staticmethod
    def create(form, image):
        db.session.add(MenuItem().update(form, image))
        db.session.commit()


    def update(self, form, image):
        self.name = form.name.data
        self.price = form.price.data
        self.description = form.description.data
        if self.category_id != form.category.data:
            if (self.category_id is not None):
                Category.query.get(self.category_id).remove_item(self)

            category = Category.get_category_by_name(form.category.data)
            category.add_item(self)

        self.tags = form.tags.data
        self.allergens = form.allergens.data

        if image.filename != "":
            filename = f"{str(uuid.uuid1())}_{secure_filename(image.filename)}"
            self.image = "images/" + filename
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(image_path)

        db.session.commit()

        return self


    def remove(self):
        if self.image != DEFAULT_IMAGE:
            os.remove("foorpp/" + url_for("static", filename=self.image))

        MenuItem.query.filter(MenuItem.id == self.id).delete()
        db.session.commit()


    def __repr__(self):
        return f"MenuItem({self.id}, '{self.name}', '{self.price}'," \
               f"{self.category_id})"


    def __eq__(self, other):
        return self.id == other.id


    def __lt__(self, other):
        return self.id < other.id


class CustomerSession(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start = db.Column(db.DateTime, nullable=False, default=func.now())
    end = db.Column(db.DateTime)
    order = db.relationship("Order", backref="customer_session",
                            uselist=False)


    def __repr__(self):
        return f"CustomerSession({self.id}, '{self.start}', '{self.end}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime)
    total_price = db.Column(db.Numeric(10, 2), nullable=False, default=0)
    item_count = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), nullable=False, default = "unsubmitted")
    session_id = db.Column(db.Integer, db.ForeignKey("customer_session.id"))
    items = db.relationship("MenuItem", secondary="order_items",
                            backref="orders")


    def __repr__(self):
        return f"Order({self.id}, {self.total_price},"\
               f"{self.items}, {self.item_count}, '{self.status}')"


    def add_item(self, item):
        self.total_price += Decimal(item.price)
        self.item_count += 1

        order_item = db.session.query(order_items).filter(
            order_items.c.order_id==self.id,
            order_items.c.item_id==item.id
        ).first()

        if order_item is None:
            self.items.append(item)
        else:
            db.session.query(order_items).filter(
                order_items.c.order_id==self.id,
                order_items.c.item_id==item.id
            ).update({"count": order_items.c.count + 1})

        db.session.commit()


    def decrease_item(self, item, count):
        self.total_price -= item.price * count
        self.item_count -= count
        db.session.query(order_items).filter(
            order_items.c.order_id==self.id,
            order_items.c.item_id==item.id
        ).update({"count": order_items.c.count - count})

        db.session.commit()

        order_item = db.session.query(order_items).filter(
            order_items.c.order_id==self.id,
            order_items.c.item_id==item.id
        ).first()

        if order_item.count == 0:
            self.items.remove(item)

        db.session.commit()


    def empty_cart(self):
        self.total_price = 0
        self.item_count = 0
        self.items.clear()
        db.session.commit()


    def get_item_counts(self):
        item_counts = {}

        for order_item in db.session.query(order_items).filter(
            order_items.c.order_id==self.id,
        ).all():
            item_counts[order_item.item_id] = order_item.count

        return item_counts


    @staticmethod
    def get_current_order():
        if session.get("order_id") is None:
            current_order = Order(session_id=session["id"])
            db.session.add(current_order)
            db.session.commit()
            session["order_id"] = current_order.id
            return current_order

        return Order.query.get(session["order_id"])


class AdminAccount(db.Model):
    password = db.Column(db.String(50), primary_key=True)
