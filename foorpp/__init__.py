from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "967e5507622ee781502896970aaccf8f1ddd553c06f73d9e5d518292d83a9c95"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
app.config['UPLOADED_PHOTOS_DEST'] = "static/images"

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

ALLERGENS = [
    "Cereals containing gluten",
    "Crustaceans",
    "Eggs",
    "Fish",
    "Peanuts",
    "Soybeans",
    "Milk",
    "Nuts",
    "Celery",
    "Mustard",
    "Sesame seeds",
    "Sulphur dioxide and sulphites",
    "Lupin",
    "Molluscs"
]

app.app_context().push()

from foorpp import routes

