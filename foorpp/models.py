from flask import session
from foorpp import db
from functools import total_ordering
from sqlalchemy import func


menu_item_tags = db.Table("menu_item_tags",
                          db.Column("menu_item_id", db.Integer,
                                    db.ForeignKey("menu_item.id")),
                          db.Column("item_tag_id", db.Integer,
                                    db.ForeignKey("item_tag.id")))


menu_item_allergens = db.Table("menu_item_allergens",
                               db.Column("menu_item_id", db.Integer,
                                         db.ForeignKey("menu_item.id")),
                               db.Column("allergen_id", db.Integer,
                                         db.ForeignKey("allergen.id")))


order_menu_items = db.Table("order_menu_items",
                            db.Column("order_id", db.Integer,
                                      db.ForeignKey("order.id")),
                            db.Column("menu_item_id", db.Integer,
                                      db.ForeignKey("menu_item.id")))


class Category(db.Model):
    name = db.Column(db.String(20), nullable = False, primary_key = True)
    value = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Category('{self.category_name}', '{self.category_value}')"


@total_ordering
class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Double, nullable = False)
    description = db.Column(db.String(1000))
    image = db.Column(db.String(50), nullable = False, default = "static/images/default.jpg")
    tags = db.relationship("ItemTag", secondary = menu_item_tags,
                           backref = "menu_items")
    allergens = db.relationship("Allergen", secondary = menu_item_allergens,
                                backref = "menu_items")

    def __repr__(self):
        return f"MenuItem({self.id}, '{self.name}', '{self.price}')"

    def __eq__(self, other):
        return self.id == other.id

    def __lt__(self, other):
        return self.id < other.id


class ItemTag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String(50))

    def __repr__(self):
        return f"ItemTag('{self.tag}')"


class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    allergen = db.Column(db.String(30), nullable = False)

    def __repr__(self):
        return f"ItemTag('{self.allergen}')"


class CustomerSession(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    start = db.Column(db.DateTime, nullable = False, default = func.now())
    end = db.Column(db.DateTime)
    order = db.relationship("Order", backref = "customer_session",
                            uselist = False)

    def __repr__(self):
        return f"CustomerSession({self.id}, '{self.start}', '{self.end}')"


class Order(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    time = db.Column(db.DateTime)
    total_price = db.Column(db.Double, nullable = False, default = 0)
    item_count = db.Column(db.Integer, nullable = False, default = 0)
    status = db.Column(db.String(20), nullable = False,
                        default = "unsubmitted")
    session_id = db.Column(db.Integer, db.ForeignKey("customer_session.id"))
    items = db.relationship("MenuItem", secondary = "order_menu_items",
                            backref = "order", uselist=True)

    def __repr__(self):
        return f"Order({self.id}, {self.number}, {self.total_price},"\
               f"{self.items}, {self.item_count}, '{self.status}')"

    @classmethod
    def get_current_order(self):
        if session.get("order_id") is None:
            current_order = Order()
            db.session.add(current_order)
            db.session.commit()
            session["order_id"] = current_order.id
            return current_order

        return Order.query.get(session["order_id"])

    def add_item(self, item):
        self.total_price += item.price
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
