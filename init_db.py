from foorpp import bcrypt, db
from foorpp.models import AdminAccount, Category, MenuItem

db.drop_all()
db.create_all()

db.session.add(
    AdminAccount(password = bcrypt.generate_password_hash(password = "admin")
                 .decode("utf-8"))
)

db.session.commit()
