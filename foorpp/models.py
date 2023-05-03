from decimal import Decimal
from flask import session
from foorpp import db
from functools import total_ordering
from sqlalchemy import func


order_menu_items = db.Table("order_menu_items",
                            db.Column("order_id", db.Integer,
                                      db.ForeignKey("order.id")),
                            db.Column("menu_item_id", db.Integer,
                                      db.ForeignKey("menu_item.id")))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)


    def __repr__(self):
        return f"Category('{self.category_name}')"


    @staticmethod
    def create(form):
        db.session.add(Category(name=form.name.data))
        db.session.commit()


@total_ordering
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(50), nullable=False,
                      default="images/default.png")
    tags = db.Column(db.String, default="")
    allergens = db.Column(db.String, default="")


    @staticmethod
    def create(form):
        db.session.add(MenuItem().update(form))
        db.session.commit()


    def update(self, form):
        self.name = form.name.data
        self.price = form.price.data
        self.description = form.description.data
        self.tags = form.tags.data
        self.allergens = form.allergens.data
        db.session.commit()

        return self


    def remove(self):
        MenuItem.query.filter(MenuItem.id == self.id).delete()
        db.session.commit()


    def __repr__(self):
        return f"MenuItem({self.id}, '{self.name}', '{self.price}')"


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
    items = db.relationship("MenuItem", secondary="order_menu_items",
                            backref="order", uselist=True)


    def __repr__(self):
        return f"Order({self.id}, {self.number}, {self.total_price},"\
               f"{self.items}, {self.item_count}, '{self.status}')"


    @staticmethod
    def get_current_order():
        if session.get("order_id") is None:
            current_order = Order()
            db.session.add(current_order)
            db.session.commit()
            session["order_id"] = current_order.id
            return current_order

        return Order.query.get(session["order_id"])


    def add_item(self, item):
        self.total_price += Decimal(item.price)
        self.item_count += 1
        self.items.append(item)
        db.session.commit()


    def remove_item(self, item):
        self.total_price -= item.price
        self.item_count -= 1
        self.item.remove(item)


    def empty_cart(self):
        self.total_price = 0
        self.item_count = 0
        self.items.clear()
        db.session.commit()


class AdminAccount(db.Model):
    password = db.Column(db.String(50), primary_key=True)
