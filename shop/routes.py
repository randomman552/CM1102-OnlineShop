#File to hold routes (we can split this into many separate files if it gets too big)
import os
import random
from flask import render_template, redirect, request, flash, url_for, session, Flask
from werkzeug.utils import secure_filename
from .forms import *
from .models import db, Product, Picture
from sqlalchemy import and_
from . import app
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash # security package.
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import time

@app.route("/")
def render_home():
    return render_template("layout.html")

@app.route("/products")
def render_products():
    def handle_views():
        """Handle setting of session variables for product display.\n
        This will return a redirect if the required GET variable is missing from the url."""
        #If it is set to grid, set the session variable and return
        if "view" in request.args:
            if request.args["view"] == "grid":
                session["product display"] = "grid"
            else:
                session["product display"] = "list"
            #If view is in the GET args, we do not need to rebuild the url to contain it.
            #So we can return
            return
                
        #If either of the previous checks fail, set "product display" to if it is not available
        if not("product display" in session):
            session["product display"] = "list"

        #Build a redirect to set the GET variable to list.
        temp = []

        #For each arg in the request, recreate the GET string for that arg
        for arg in request.args:
            temp.append(f"{arg}={request.args[arg]}")

        #Add our new arg to the list
        temp.append(f"view={session['product display']}")

        #Create the base url and add all the args to it
        url = f"{request.base_url}?"
        for arg in temp:
            url += f"{arg}&"

        #Remove the extra & from the string and return the redirect
        return redirect(url[:-1])
    def get_products():
        """This function gets the relevant products from the database and filters them according to user input."""
        products = []
        if "query" in request.args:
            #Fitler the results with the query, look at the description and name of products.
            products = Product.query.filter(Product.name.like(f"%{request.args['query']}%")).all()
            products += Product.query.filter(Product.description.like(f"%{request.args['query']}%")).all()
            #TODO: ADD CATEGORY FILTERING
            #Remove any duplicates
            already_present = []
            for product in products:
                if product.ID in already_present:
                    products.remove(product)
                else:
                    already_present.append(product.ID)
        else:
            products = Product.query.all()
        return products
    def get_pictures(products):
        """Get the relevant pictures from the database."""
        #Setup return list with slots for each product
        pictures_return = []
        #Generate lowest and highest ID variables, these are used to constrain the pictures we get from the database
        lowestID = products[0].ID
        highestID = products[0].ID

        #Initalise pictures_return and get highest and lowest ID.
        for i in range(len(products)):
            if products[i].ID < lowestID:
                lowestID = products[i].ID
            elif products[i].ID > highestID:
                highestID = products[i].ID
            pictures_return.append([])

        #Get pictures from the database
        pictures = Picture.query.filter(Picture.productID <= highestID).filter(Picture.productID >= lowestID).all()

        #Append the corresponding pictures to the correct list
        for i in range(len(products)):
            for picture in pictures:
                if picture.productID == products[i].ID:
                    pictures_return[i].append(picture)
        return pictures_return
    
    #Call handle_views, if it returns something, return it.
    retval = handle_views()
    if retval:
        return retval
    
    #Get products and pictures from the database
    products = get_products()
    pictures = get_pictures(products)

    return render_template("products/products.html", products=products, pictures=pictures, mode="edit")

@app.route("/products/new", methods=["GET", "POST"])
def render_new_product():
    #Give the new product a random name, which we can then use to get its ID from the database
    random_name = str(random.randint(0,500000000))
    new_product = Product(name=random_name)
    #Add product to database
    db.session.add(new_product)
    db.session.commit()
    #Extract the newly created product and redirect to the edit page for it
    new_product = Product.query.filter(Product.name.like(random_name)).first()
    #Change the product name from the random one
    new_product.name = "Product name"
    db.session.commit()
    return redirect(f"/products/{new_product.ID}")

@app.route("/products/<int:product_id>", methods=["GET"])
def render_view_product(product_id):
    product = Product.query.filter(Product.ID.like(product_id)).first()
    pictures = Picture.query.filter(Picture.productID.like(product_id)).all()
    return render_template("products/view_product.html", product=product, pictures=pictures, mode="edit")
    
    app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/luca/Desktop/Accounts/database.db' #URI of database
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model): #Table
    id = db.Column(db.Integer, primary_key=True)
     #allow only non existing emails, confirming with the db.
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
#check and see if user exists in database
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #emails are unique shouldn't get more than one result.
        if user:
            if check_password_hash(user.password, form.password.data): #check hash password instead of string password.
                login_user(user, remember=form.remember.data)
                return redirect(url_for('Account'))

        return '<h1>Invalid email or password</h1>' #If there is no match


    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256') #generate hash 80 characters long hence max 80 password fields.
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user) #Pass to db.
        db.session.commit()

        return '<h1>New user has been successfully created!</h1>'

    return render_template('signup.html', form=form)

@app.route('/password_change', methods=["GET", "POST"])
@login_required
def user_password_change():
    form = PasswordForm()

    if form.validate_on_submit():
        user = current_user
        user.password = generate_password_hash(form.password.data, method='sha256')
        db.session.add(user)
        db.session.commit()

        return redirect(url_for('Account'))

    return render_template('password_change.html', form=form)

@app.route('/delete_account', methods=["GET", "POST"])
@login_required
def delete():
    form = DeleteUserForm()

    if form.validate_on_submit():
        user = current_user
        db.session.delete(user)
        db.session.commit()

        logout_user()
        return redirect(url_for('login'))

    return render_template('delete_account.html', form=form)

@app.route('/Account')
@login_required #can not access directly
def Account():
    return render_template('Account.html', name=current_user.email)

@app.route('/logout')
@login_required
def logout(): #redirect to login when this route is reached.
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
