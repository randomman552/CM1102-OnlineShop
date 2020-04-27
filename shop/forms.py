from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField, RadioField, PasswordField, BooleanField, SelectField
from wtforms import validators

class ShippingForm(FlaskForm):
    firstname = StringField('First Name', validators=[validators.DataRequired(message='Please fill in your first name'), validators.Length(min=2, max=15, message='Last name must be at least 2 characters long')])
    lastname = StringField('Last Name', validators=[validators.DataRequired(message='Please fill in your last name'), validators.Length(min=2, max=15, message='Last name must be at least 2 characters long')])
    email = StringField('Email', validators=[validators.DataRequired(message='Please fill in your email address'), validators.Email(message='Invalid email address')])
    phone = IntegerField('Phone', validators=[validators.DataRequired(message='Please type an 11 digit phone number')])
    address1 = TextAreaField('Address 1', validators=[validators.DataRequired(message='Please fill in the first line of your address'), validators.Length(min=3, max=30, message='Please type an address between 3 and 30 characters long')])
    address2 = TextAreaField('Address 2 ', validators=[validators.DataRequired(message='Please fill in the second line of your address'), validators.Length(min=3, max=30, message='Please type an address between 3 and 30 characters long')])
    postcode = StringField('Postcode ', validators=[validators.DataRequired(message='Please fill in your postcode'), validators.Length(min=6, max=9, message='Your postcode must be between 6 and 8 characters long')])
    submit1 = SubmitField('Proceed to Billing')

class BillingForm(FlaskForm):
   cardholdername = StringField('Card holders name', validators=[validators.DataRequired(message='Please fill in the card holders name'), validators.Length(min=4, max=20)])
   cardnumber = IntegerField('Card Number', validators=[validators.DataRequired(message='Type your 16 digit card number'), validators.NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber2 = IntegerField('Card Number', validators=[validators.DataRequired(message='Type your 16 digit card number'), validators.NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber3 = IntegerField('Card Number', validators=[validators.DataRequired(message='Type your 16 digit card number'), validators.NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber4 = IntegerField('Card Number', validators=[validators.DataRequired(message='Type your 16 digit card number'), validators.NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   expirydate = SelectField('Expiry Date', choices=[('2020' , '2020'), ('2021' , '2021'), ('2022' , '2022'), ('2023' , '2023'), ('2024' , '2024'), ('2025' , '2025'), ('2026' , '2026'), ('2027' , '2027'), ('2028' , '2028'), ('2029' , '2029'), ('2030' , '2030'), ('2031' , '2031'), ('2032' , '2032'), ('2033' , '2033'), ('2034' , '2034'), ('2035' , '2035')])
   expirymonth = SelectField('Expiry month', choices=[('01' , '01'), ('02' , '02'), ('03' , '03'), ('04' , '04'), ('05' , '05'), ('06' , '06'), ('07' , '07'), ('08' , '08'), ('09' , '09'), ('10' , '10'), ('11' , '11'), ('12' , '12')])
   cvv = IntegerField('CVV', validators=[validators.DataRequired(message='These are the three digits on the back'), validators.NumberRange(min=0, max=999, message='These are the three digits on the back')])
   submit2 = SubmitField('Proceed to Review')

class ReviewForm(FlaskForm):
    submit3 = SubmitField('Pay now')
    editshipping = SubmitField('Edit Shipping')
    editbilling = SubmitField('Edit Billing')
    
class AddReviewForm(FlaskForm):
    stars = RadioField("Stars: ", choices=[
                       ("1", '1 Star'), ("2", '2 Star'), ("3", '3 Star'), ("4", '4 Star'), ("5", '5 Star')])
    comment = TextAreaField("Comment: ", validators=[
                            validators.length(max=140, message="Your comment must be a maximum of 140 characers long.")])
    submit = SubmitField("Add review")

class LoginForm(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email(message='Invalid email'), validators.Length(max=50)]) #setting minimum and maximum lengths.
    password = PasswordField('password', validators=[validators.InputRequired(), validators.Length(min=8, max=80)])
    remember = BooleanField('remember me') #remember me checkbox

class RegisterForm(FlaskForm):
    email = StringField('email', validators=[validators.InputRequired(), validators.Email(message='Invalid email'), validators.Length(max=50)])
    password = PasswordField('password', validators=[validators.InputRequired(), validators.Length(min=8, max=80)])

class PasswordForm(FlaskForm):
    password = PasswordField('password', validators=[validators.InputRequired(), validators.Length(min=8, max=80)])


class DeleteUserForm(FlaskForm):
    delete = SubmitField('Delete')
