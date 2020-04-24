from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, SubmitField, SelectField
from wtforms.validators import DataRequired, Length, Email, NumberRange

class ShippingForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please fill in your first name'), Length(min=2, max=15, message='Last name must be at least 2 characters long')])
    lastname = StringField('Last Name', validators=[DataRequired(message='Please fill in your last name'), Length(min=2, max=15, message='Last name must be at least 2 characters long')])
    email = StringField('Email', validators=[DataRequired(message='Please fill in your email address'), Email(message='Invalid email address')])
    phone = IntegerField('Phone', validators=[DataRequired(message='Please choose an 11 digit phone number')])
    address1 = TextAreaField('Address 1', validators=[DataRequired(message='Please fill in the first line of your address'), Length(min=3, max=30, message='Please type an address between 3 and 30 characters long')])
    address2 = TextAreaField('Address 2 ', validators=[DataRequired(message='Please fill in the second line of your address'), Length(min=3, max=30, message='Please type an address between 3 and 30 characters long')])
    postcode = StringField('Postcode ', validators=[DataRequired(message='Please fill in your postcode'), Length(min=6, max=9, message='Your postcode must be between 6 and 8 characters long')])
    submit1 = SubmitField('Proceed to Billing')

class BillingForm(FlaskForm):
   cardholdername = StringField('Card holders name', validators=[DataRequired(message='Please fill in the card holders name'), Length(min=4, max=20)])
   cardnumber = IntegerField('Card Number', validators=[DataRequired(message='Type your 16 digit card number'), NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber2 = IntegerField('Card Number', validators=[DataRequired(message='Type your 16 digit card number'), NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber3 = IntegerField('Card Number', validators=[DataRequired(message='Type your 16 digit card number'), NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   cardnumber4 = IntegerField('Card Number', validators=[DataRequired(message='Type your 16 digit card number'), NumberRange(min=0, max=9999, message='Type your 16 digit card number')])
   expirydate = SelectField('Expiry Date', choices=[('2020' , '2020'), ('2021' , '2021'), ('2022' , '2022'), ('2023' , '2023'), ('2024' , '2024'), ('2025' , '2025'), ('2026' , '2026'), ('2027' , '2027'), ('2028' , '2028'), ('2029' , '2029'), ('2030' , '2030'), ('2031' , '2031'), ('2032' , '2032'), ('2033' , '2033'), ('2034' , '2034'), ('2035' , '2035')])
   expirymonth = SelectField('Expiry month', choices=[('01' , '01'), ('02' , '02'), ('03' , '03'), ('04' , '04'), ('05' , '05'), ('06' , '06'), ('07' , '07'), ('08' , '08'), ('09' , '09'), ('10' , '10'), ('11' , '11'), ('12' , '12')])
   cvv = IntegerField('CVV', validators=[DataRequired(message='These are the three digits on the back'), NumberRange(min=0, max=999, message='These are the three digits on the back')])
   submit2 = SubmitField('Proceed to Review')

class ReviewForm(FlaskForm):
    submit3 = SubmitField('Pay now')
    editshipping = SubmitField('Edit Shipping')
    editbilling = SubmitField('Edit Billing')
