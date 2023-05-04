from foorpp.models import Category, MenuItem
from sqlalchemy import or_


def filter_by_keyword(keyword):
    if keyword is None:
        return MenuItem.query.all()

    return MenuItem.query.filter(
        or_(MenuItem.name.ilike(f"%{keyword}%"),
            MenuItem.description.ilike(f"%{keyword}%"),
            MenuItem.tags.ilike(f"%{keyword}%"))).all()


def filter_by_category(category_name):
    if category_name == "Show me everything!":
        return MenuItem.query.all()

    return Category.query \
        .filter(Category.name.ilike(f"%{category_name}%")).first().menu_items
