from foorpp import db

class Category(db.Model):
    name = db.Column(db.String(20), nullable=False, primary_key=True)
    value = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Category('{self.category_name}', '{self.category_value}')"
