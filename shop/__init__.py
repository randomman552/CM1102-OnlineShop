# Any code we want to run before creating any routes or models should be put in here
from flask import Flask, redirect, flash
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

# Setup the flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

from . import routes
from . import models

from flask_admin import Admin
from shop.views import AdminView
from flask_admin.contrib.sqla import ModelView
from shop.models import Picture
from shop.models import Product
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(Product, models.db.session))

#User loader
@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)

#TODO: Make it redirect you to the previous page you were on instead of login?
#Redirect for when user is unauthorised
@login_manager.unauthorized_handler
def unauthorized():
    flash("You must be logged in to view that page.")
    return redirect("/login")