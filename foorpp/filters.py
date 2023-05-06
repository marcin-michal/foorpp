from foorpp.models import Category, MenuItem
from sqlalchemy import and_, or_


def filtered_items(categories, keyword):
    query_category = filter_by_category(categories)
    query_keyword = filter_by_keyword(keyword)

    return query_category.intersect(query_keyword).all()


def filter_by_keyword(keyword):
    if keyword is None:
        return MenuItem.query

    return MenuItem.query.filter(
        or_(MenuItem.name.ilike(f"%{keyword}%"),
            MenuItem.description.ilike(f"%{keyword}%"),
            MenuItem.tags.ilike(f"%{keyword}%")))


def filter_by_category(seeked_categories):
    if seeked_categories is None or not seeked_categories:
        return MenuItem.query

    query = MenuItem.query.filter(False)
    for seeked_category in seeked_categories:
        query = query.union(
            MenuItem.query.filter(MenuItem.category_id == seeked_category)
        )

    return query
