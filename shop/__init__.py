#Any code we want to run before creating any routes or models should be put in here
from flask import Flask
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

from . import routes