from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DecimalField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField
)
from wtforms.validators import DataRequired, NumberRange, Length


class AdminLoginForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")


class MenuItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(),
                                             Length(min=1, max=40)])
    price = DecimalField("Price", places=2, validators=[DataRequired(),
                                                        NumberRange(min=0)])
    description = TextAreaField("Description")
    image = FileField("Photo",
                      validators=[FileAllowed(['png', 'jpg', 'jpeg'])])
    tags = TextAreaField("Tags")
    allergens = TextAreaField("Allergens")
    submit = SubmitField("Save item")


class CategoryForm(FlaskForm):
    name = StringField("Category name", validators=[DataRequired(),
                                                    Length(min=1, max=20)])
    submit = SubmitField("Add category")


class OrderStatusForm(FlaskForm):
    status = SelectField("Status", choices=[("unsubmitted", "Unsubmitted"),
                                            ("submitted", "Submitted"),
                                            ("prepared", "Prepared"),
                                            ("finished", "Finished"),
                                            ("cancelled", "Cancelled")])
    submit = SubmitField("Save")
