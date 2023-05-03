from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DecimalField,
    PasswordField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import DataRequired, Length


class AdminLoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class MenuItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),
                                             Length(min=1, max=40)])
    price = DecimalField("Price", places=2, validators=[DataRequired()])
    description = TextAreaField("Description")
    image = FileField("Photo",
                      validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    tags = TextAreaField("Tags")
    allergens = TextAreaField("Allergens")
    submit = SubmitField("Save item")
