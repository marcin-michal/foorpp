from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    search = StringField("Search", validators = [DataRequired(), Length(max=50)])
    submit = SubmitField("Search")
