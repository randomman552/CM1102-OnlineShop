# Any code we want to run before creating any routes or models should be put in here
from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import os

# Setup the flask app
app = Flask(__name__)
app.secret_key = os.urandom(24)

# Setup the flask upload variables (currently not used)
UPLOAD_FOLDER = 'static/products/temp'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

bootstrap = Bootstrap(app)

login_manager = LoginManager()
login_manager.init_app(app)

from . import routes
from . import models

@login_manager.user_loader
def load_user(user_id):
    return models.User.query.get(user_id)