from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, PasswordField, BooleanField, MultipleFileField, SubmitField
from wtforms.validators import Length, DataRequired


class ProductFilterForm(FlaskForm):
    "Form for product filtering, is placed in products.html page."
    # TODO: Implement product filtering
    pass
