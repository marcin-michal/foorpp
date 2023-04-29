from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SECRET_KEY"] = "967e5507622ee781502896970aaccf8f1ddd553c06f73d9e5d518292d83a9c95"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///site.db"
db = SQLAlchemy(app)

app.app_context().push()

from foorpp import routes

