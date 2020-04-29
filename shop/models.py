# File to hold database models
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime, Float, BigInteger, DECIMAL, func
from datetime import datetime
import json
from decimal import Decimal

from . import app

# Set config location here
config_location = "shop/config/dbconfig.json"


def read_json(file_location: str) -> dict:
    """Read a json file and return it as a dict.\n
    @param file_location - The location of the file to read.\n
    @return - A dict with the contents of the file.
    """

    result = dict()
    with open(file_location, "r") as file:
        result = json.load(file)
    return result


def write_json(to_write: dict, file_location: str) -> None:
    """Write a dict to a json file.\n
    @param to_write - The dict to write to the file.\n
    @param file_location - The location to write to.
    """

    with open(file_location, "w") as file:
        json.dump(to_write, file, indent=4)


config = read_json(config_location)

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

    def get_id(self):
        return self.ID

# Products class


class Product(db.Model):
    ID = Column(Integer, primary_key=True, unique=True, nullable=False)
    name = Column(Text, nullable=False)

    # Price is stored as an decimal so no precision is lost to floating point accuracy
    _price = Column(DECIMAL(65, 2), nullable=False, default=0)
    public = Column(Boolean, default=False)
    description = Column(Text, nullable=False, default="This is a description")

    # Some item specific attributes (could be changed if items the shop sells changes)
    # Using DECIMAL here, so we can store numbers of massive size.
    # These all have a default of -1 so we can treat any value less than 0 as n/a
    _mass = Column(DECIMAL(65, 0), default=-1)
    _surface_gravity = Column(DECIMAL(65, 4), default=-1)
    _orbital_period = Column(DECIMAL(65, 4), default=-1)

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
        return self.__format_decimal(self._price, before="£")

    @price.setter
    def set_price(self, number: float):
        self._price = Decimal(str(number))

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


# Create all the tables (if not already created)
db.create_all()
