from foorpp import db
from foorpp.models import MenuItem, Order


def add_to_cart(item_id):
    item = MenuItem.query.get(item_id)
    Order.get_current_order().add_item(item)
    db.session.commit()
