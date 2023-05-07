from foorpp import db
from foorpp.models import Category, MenuItem, Order


def add_to_cart(item_id):
    item = MenuItem.query.get(item_id)
    Order.get_current_order().add_item(item)
    db.session.commit()


def selected_categories(category_ids):
    if category_ids is None:
        return []

    categories = []

    for id in category_ids:
        categories.append(Category.query.get(id))

    return categories


def clear_filters(session):
    session["categories"] = None
    session["keyword"] = None
    session["excluded_allergens"] = None
    session["diets"] = None
    session["ordering"] = None
