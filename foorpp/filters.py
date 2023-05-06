from foorpp.models import MenuItem
from sqlalchemy import not_, or_


def filtered_items(categories, keyword, diets, excluded_allergens):
    query = filter_by_category(categories)
    query = query.intersect(filter_by_keyword(keyword))
    query = query.intersect(filter_by_diet(diets))
    query = query.intersect(filter_by_allergens(excluded_allergens))

    return query.all()


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
    for category in seeked_categories:
        query = query.union(
            MenuItem.query.filter(MenuItem.category_id == category)
        )

    return query


def filter_by_diet(seeked_diets):
    if seeked_diets is None or not seeked_diets:
        return MenuItem.query

    query = MenuItem.query.filter(False)
    for diet in seeked_diets:
        query = query.union(
            MenuItem.query.filter(MenuItem.tags.ilike(f"%{diet}%"))
        )

    return query


def filter_by_allergens(excluded_allergens):
    if excluded_allergens is None or not excluded_allergens:
        return MenuItem.query

    return MenuItem.query.filter(
        not_(or_(*[MenuItem.allergens.ilike(f"%{allergen}%")
                   for allergen in excluded_allergens])))
