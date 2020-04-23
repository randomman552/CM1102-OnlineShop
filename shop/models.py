# File to hold database models
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float, BigInteger, DECIMAL, func
from datetime import datetime
import json
from decimal import Decimal

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

    # Price is stored as an decimal so no precision is lost to floating point accuracy
    # As this is currently a signed number, its largest value is 9,223,372,036,854,775,807‬ (9 Quintillion)
    _price = Column(BigInteger, nullable=False, default=0)
    public = Column(Boolean, default=False)
    description = Column(Text, nullable=False, default="This is a description")

    # Some item specific attributes (could be changed if items the shop sells changes)
    # Using DECIMAL here, so we can store numbers of massive size.
    # These all have a default of -1 so we can treat any value less than 0 as n/a
    _mass = Column(DECIMAL(65, 0), default=-1)
    _surface_gravity = Column(DECIMAL(64, 2), default=-1)
    _orbital_period = Column(DECIMAL(64, 2), default=-1)

    # Properties so that the format of our attributes are in the right format
    # This common function handles the formatting
    def __format_decimal(self, number, before: str = "", after: str = ""):
        """
        This function formats the number it is given into standard form 
        if it is more than 10 characters long without it.\n
        @param number - The number to format.\n
        @param before - A string to add to the begining of the return value.\n
        @param after - A string to add to the end of the return value.\n
        @return - A string representation of that number in standard form.
        """

        return_value = str(number)

        # If the number is more than 20 characters long, use the standard form
        if len(return_value) > 10:
            return_value = '{:.2e}'.format(number)
        else:
            if len(return_value.split(".")) > 1:
                # Add zeros until it is at 2 significant figures
                while len(return_value.split(".")[1]) < 2:
                    return_value += "0"

        # Return our formatted number
        return f"{before}{return_value}{after}"

    @property
    def mass(self) -> str:
        return self.__format_decimal(self._mass, after=" kg")

    @mass.setter
    def set_mass(self, number):
        self._mass = Decimal(str(number))

    @property
    def surface_gravity(self) -> str:
        return self.__format_decimal(self._surface_gravity, after=" m/s²")

    @surface_gravity.setter
    def set_gravity(self, number):
        self._surface_gravity = Decimal(str(number))

    @property
    def orbital_period(self) -> str:
        return self.__format_decimal(self._orbital_period, after=" years")

    @orbital_period.setter
    def set_orbital_period(self, number):
        self._orbital_period = Decimal(str(number))

    @property
    def price(self) -> str:
        return self.__format_decimal(self._price / 100, before="£")

    @price.setter
    def set_price(self, number: float):
        self._price = round(number * 100)

# Review class


class Review(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    userID = Column(Integer, ForeignKey(User.ID))
    productID = Column(Integer, ForeignKey(Product.ID))
    rating = Column(Integer, nullable=False, default=1)
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
