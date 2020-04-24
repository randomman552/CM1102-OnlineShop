from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, RadioField, PasswordField, BooleanField
from wtforms.validators import Length, DataRequired, InputRequired, Email, Length


class AddReviewForm(FlaskForm):
    stars = RadioField("Stars: ", choices=[
                       ("1", '1 Star'), ("2", '2 Star'), ("3", '3 Star'), ("4", '4 Star'), ("5", '5 Star')])
    comment = TextAreaField("Comment: ", validators=[
                            validators.length(max=140, message="Your comment must be a maximum of 140 characers long.")])
    submit = SubmitField("Add review")

class LoginForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)]) #setting minimum and maximum lengths.
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me') #remember me checkbox

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])

class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])


class DeleteUserForm(FlaskForm):
    delete = SubmitField('Delete')
