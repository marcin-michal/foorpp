from foorpp import bcrypt, db
from foorpp.models import AdminAccount, Category, MenuItem

db.drop_all()
db.create_all()

cat1 = Category(name="Pizza")
cat2 = Category(name="Burger")
cat3 = Category(name="Mexican")
cat4 = Category(name="Indian")

it1 = MenuItem(name = "Pizza", price = 6.99, category=cat1,
               description = "Very pizza yummy yum yum yum")
it1.allergens = "Eggs, Milk"
it1.tags = "pizza, yummy, vegetarian"

it2 = MenuItem(name = "Burger", price = 9.89, description = "Big borgur",
               category=cat2)
it2.allergens = "Crustaceans, Soybeans"
it2.tags = "yummy"

it3 = MenuItem(name = "Mystery", price = 2.58, description = "!!!sushiii")
it4 = MenuItem(name = "myster2", price = 54546543.32, category=cat1)
it4.tags = "pizza"

db.session.add_all([cat1, cat2, cat3, cat4])
db.session.add_all([it1, it2, it3, it4])
db.session.add(
    AdminAccount(password = bcrypt.generate_password_hash(password = "admin")
                 .decode("utf-8"))
)

db.session.commit()
