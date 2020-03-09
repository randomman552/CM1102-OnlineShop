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