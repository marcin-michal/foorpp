from foorpp import db
from foorpp.models import ItemTag, MenuItem
from numpy import unique
from sqlalchemy import or_


def filter_by_keyword(keyword):
    if not keyword:
        return MenuItem.query.all()

    found_substring =  MenuItem.query.filter(
        or_(MenuItem.name.ilike(f"%{keyword}%"),
        MenuItem.description.ilike(f"%{keyword}%"))).all()
    found_tag = []

    for tag in ItemTag.query.filter(ItemTag.tag.ilike(f"%{keyword}%")).all():
        found_tag += tag.menu_items

    return unique(found_tag + found_substring)
