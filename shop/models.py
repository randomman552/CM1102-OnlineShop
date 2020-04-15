# File to hold database models
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, func
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
db_connect_string = f"mysql+pymysql://{config['username']}:{config['password']}@{config['host']}:3306/{config['database']}"
if "ssl_key" in config and "ssl_cert" in config:
    db_connect_string += f"?ssl_key={config['ssl_key']}&ssl_cert={config['ssl_cert']}"

# Add connection uri to the app config
app.config["SQLALCHEMY_DATABASE_URI"] = db_connect_string
db = SQLAlchemy(app)


# User class
class User(UserMixin, db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    email = Column(String(256), unique=True, nullable=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    password_hash = Column(Text)

    @property
    def password(self):
        raise AttributeError('Password is not readable.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

# Products class


class Product(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)
    # Price is stored as an integer so no precision is lost to floating point accuracy
    _price = Column(Integer, nullable=False, default=0)
    description = Column(Text, nullable=False, default="This is a description")
    _information = Column(Text)
    public = Column(Boolean, default=False)

    # Description stores a json encoded dict, this allows me to store some layout information in the product table.
    @property
    def information(self):
        return json.loads(self._information)

    @information.setter
    def set_information(self, dict_object):
        self._information = json.dumps(dict_object)

    @property
    def price(self) -> str:
        price = str(round(self._price / 100, 2))
        while len(price.split(".")[1]) < 2:
            price += "0"
        return f"£ {price}"

    @price.setter
    def set_price(self, number: float):
        self._price = round(number * 10)

# Review class


class Review(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    userID = Column(Integer, ForeignKey(User.ID))
    productID = Column(Integer, ForeignKey(Product.ID))
    rating = Column(Integer, nullable=False)
    content = Column(Text)

# Pictures class (one to many)


class Picture(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    productID = Column(Integer, ForeignKey(Product.ID), nullable=False)
    URL = Column(Text, nullable=False)

# Wishlist class (many to many)


class Wishlist(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    userID = Column(Integer, ForeignKey(User.ID), nullable=False)
    productID = Column(Integer, ForeignKey(Product.ID), nullable=False)

# Category class


class Category(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(String(30), unique=True, nullable=False)

# Product to category class (many to many)


class ProductCategory(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    categoryID = Column(Integer, ForeignKey(Category.ID), nullable=False)
    productID = Column(Integer, ForeignKey(Product.ID), nullable=False)


# UNCOMMENT THIS LINE TO CLEAR THE DATABASE
# db.drop_all()
db.create_all()
