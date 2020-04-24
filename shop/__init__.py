#Any code we want to run before creating any routes or models should be put in here
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

UPLOAD_FOLDER = 'static/products/temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
db = SQLAlchemy(app)

from . import models
from . import routes

from flask_admin import Admin
from shop.views import AdminView
from flask_admin.contrib.sqla import ModelView
from shop.models import Picture
from shop.models import Product
admin = Admin(app, name='Admin panel', template_mode='bootstrap3')
admin.add_view(ModelView(Product, db.session))