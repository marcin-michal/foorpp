from foorpp import bcrypt, db
from foorpp.models import AdminAccount, Allergen, Category, ItemTag, MenuItem

db.drop_all()
db.create_all()

# Init categories
db.session.add(Category(name="pizza", value="Pizza"))
db.session.add(Category(name="burger", value="Burger"))
db.session.add(Category(name="sushi", value="Sushi"))
db.session.add(Category(name="mexican", value="Mexican"))

# Init allergens
al01 = Allergen(allergen = "Cereals containing gluten")
al02 = Allergen(allergen = "Crustaceans")
al03 = Allergen(allergen = "Eggs")
al04 = Allergen(allergen = "Fish")
al05 = Allergen(allergen = "Peanuts")
al06 = Allergen(allergen = "Soybeans")
al07 = Allergen(allergen = "Milk")
al08 = Allergen(allergen = "Nuts")
al09 = Allergen(allergen = "Celery")
al10 = Allergen(allergen = "Mustard")
al11 = Allergen(allergen = "Sesame seeds")
al12 = Allergen(allergen = "Sulphur dioxide and sulphites")
al13 = Allergen(allergen = "Lupin")
al14 = Allergen(allergen = "Molluscs")

tag1 = ItemTag(tag = "pizza")
tag2 = ItemTag(tag = "yummy")
tag3 = ItemTag(tag = "vegetarian")

it1 = MenuItem(name = "Pizza", price = 6.99,
               description = "Very pizza yummy yum yum yum")
it1.allergens.append(al03)
it1.allergens.append(al07)
it1.tags.append(tag1)
it1.tags.append(tag2)
it1.tags.append(tag3)

it2 = MenuItem(name = "Burger", price = 9.89, description = "Big borgur")
it2.allergens.append(al02)
it2.allergens.append(al06)
it2.tags.append(tag2)

it3 = MenuItem(name = "Mystery", price = 2.58, description = "!!!sushiii")
it4 = MenuItem(name = "myster2", price = 54546543.32)
it4.tags.append(tag1)

db.session.add_all([al01, al02, al03, al04, al05, al06, al07, al08, al09, al10,
                    al11, al12, al13,  al14])
db.session.add_all([tag1, tag2, tag3])
db.session.add_all([it1, it2, it3, it4])
db.session.add(
    AdminAccount(password = bcrypt.generate_password_hash(password = "admin")
                 .decode("utf-8"))
)

db.session.commit()
