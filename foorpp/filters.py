from foorpp import db
from foorpp.models import ItemTag, MenuItem
from sqlalchemy import or_


def filtered_items(keyword):
    if not keyword:
        return MenuItem.query.all()

    return MenuItem.query.filter(or_(MenuItem.name.ilike(f"%{keyword}%"),
                                     MenuItem.description.ilike(f"%{keyword}%"))).all()
                                     ##ItemTag.tag.contains(keyword)).all()
            #.join(MenuItem.tags)
