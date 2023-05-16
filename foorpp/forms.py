from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    DecimalField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    widgets
)
from wtforms.validators import DataRequired, NumberRange, Length
from wtforms_alchemy import QuerySelectMultipleField


ALLERGEN_CHOICES = [
    "Celery",
    "Cereals containing gluten",
    "Crustaceans",
    "Eggs",
    "Fish",
    "Lupin",
    "Milk",
    "Molluscs",
    "Mustard",
    "Nuts",
    "Peanuts",
    "Sesame seeds",
    "Soya",
    "Sulphur dioxide"
]
DIETS_CHOICES = [
    "Vegan",
    "Vegetarian",
    "Dairy-free",
    "Gluten-free"
]
ORDERING_CHOICES = {
    "Ascending by price ",
    "Descending by price",
    "Ascending by name",
    "Descending by name"
}


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
    category = StringField("Category", validators=[DataRequired(),
                                                   Length(min=1, max=20)])
    submit = SubmitField("Save item")


class CategoryAddForm(FlaskForm):
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


class QuerySelectMultipleFieldWithCheckboxes(QuerySelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class SelectMultipleFieldWithCheckboxes(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


class FilterForm(FlaskForm):
    categories = QuerySelectMultipleFieldWithCheckboxes("Category")
    diets = SelectMultipleFieldWithCheckboxes("Diet", choices=DIETS_CHOICES)
    excluded_allergens = SelectMultipleFieldWithCheckboxes(
        "Excluded allergens", choices=ALLERGEN_CHOICES)
    ordering = SelectField("Order by", choices=ORDERING_CHOICES)
    submit = SubmitField("Show items")
