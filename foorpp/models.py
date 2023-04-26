from foorpp import db


menu_item_tags = db.Table("menu_item_tags",
                          db.Column("menu_item_id", db.Integer,
                                    db.ForeignKey("menu_item_id")),
                          db.Column("item_tag_id", db.Integer,
                                    db.ForeignKey("item_tag_id")))


menu_item_allergens = db.Table("menu_item_allergens",
                               db.Column("menu_item_id", db.Integer,
                                         db.ForeignKey("menu_item_id")),
                               db.Column("allergen_id", db.Integer,
                                         db.ForeignKey("allergen_id")))


class Category(db.Model):
    name = db.Column(db.String(20), nullable = False, primary_key = True)
    value = db.Column(db.String(20), nullable = False)

    def __repr__(self):
        return f"Category('{self.category_name}', '{self.category_value}')"


class MenuItem(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(30), nullable = False)
    price = db.Column(db.Double, nullable = False)
    description = db.Column(db.String(1000))
    tags = db.relationship("ItemTag", secondary = menu_item_tags,
                           backref = "menu_items")
    allergens = db.relationship("Allergen", secondary = menu_item_allergens,
                                backref = "menu_items")


class ItemTag(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    tag = db.Column(db.String(50))


class Allergen(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    allergen = db.Column(db.String(30), nullable = False)
