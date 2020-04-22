from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, RadioField
from wtforms import validators


class AddReviewForm(FlaskForm):
    stars = RadioField("Stars: ", choices=[
                       ("1", '1 Star'), ("2", '2 Star'), ("3", '3 Star'), ("4", '4 Star'), ("5", '5 Star')])
    comment = TextAreaField("Comment: ")
    submit = SubmitField("Add review")
