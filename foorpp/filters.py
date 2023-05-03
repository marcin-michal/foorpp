from foorpp.models import MenuItem
from sqlalchemy import or_


def filter_by_keyword(keyword):
    if keyword is None:
        return MenuItem.query.all()

    # found_substring = \
    return MenuItem.query.filter(
        or_(MenuItem.name.ilike(f"%{keyword}%"),
            MenuItem.description.ilike(f"%{keyword}%"),
            MenuItem.tags.ilike(f"%{keyword}%"))).all()
    # found_tag = []

    # for tag in ItemTag.query.filter(ItemTag.tag.ilike(f"%{keyword}%")).all():
    #     found_tag += tag.menu_items

    # return unique(found_tag + found_substring)
