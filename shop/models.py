#File to hold database models
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from datetime import datetime
import json

from . import app

def import_config():
    """Import the username and password from the config.json file in static."""
    config = dict()
    with open("shop/static/config.json", "r") as file:
        config = json.load(file)
    return config

def save_config(config):
    """Save config to a file."""
    with open("shop/static/config.json", "w") as file:
        json.dump(config, file, indent=4)

config = import_config()

# Create the connect string for this database, if ssl options are specified in the file, add those to the uri.
db_connect_string = "mysql+pymysql://{user}:{password}@{host}:3306/{schema}".format(
    user=config["username"], password=config["password"], host=config["host"], schema=config["database"])
if "ssl_key" in config and "ssl_cert" in config:
    db_connect_string += "?ssl_key={ssl_key}&ssl_cert={ssl_cert}".format(
        ssl_key=config["ssl_key"], ssl_cert=config["ssl_cert"])

# Add connection uri to the app config
app.config["SQLALCHEMY_DATABASE_URI"] = db_connect_string
db = SQLAlchemy(app)

#UNCOMMENT THIS LINE TO CLEAR THE DATABASE
db.drop_all()

#User class
class User(UserMixin, db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    password_hash = Column(Text)
    creation_date = Column(DateTime, nullable=False, default=datetime.now())
    
    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_id(self):
        return self.userID

#Products class
class Product(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    __desc = Column(Text, nullable=False)
    
    #Description stores a json encoded dict, this allows me to store some layout information in the product table.
    @property
    def description(self):
        return json.loads(self.desc)

    @description.setter
    def set_description(self, dict_object):
        self.desc = json.dumps(dict_object)

#Pictures class (one to many)
class Picture(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    productID = Column(Integer, ForeignKey("user.ID"), nullable=False)
    URL = Column(Text, nullable=False)

#Wishlist class (many to many)
class Wishlist(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    userID = Column(Integer, ForeignKey("user.ID"), nullable=False)
    productID = Column(Integer, ForeignKey("product.ID"), nullable=False)

#Category class
class Category(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(30), primary_key=True, unique=True, nullable=False)

#Product to category class (many to many)
class ProductCategory(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    categoryID = Column(Integer, ForeignKey("category.ID"), nullable=False)
    productID = Column(Integer, ForeignKey(Product.ID), nullable=False)
db.create_all()
