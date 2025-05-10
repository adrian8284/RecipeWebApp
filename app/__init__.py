from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# Initialze Flask app
myapp_obj = Flask(__name__)

# Get absolute path to curr dir
basedir = os.path.abspath(os.path.dirname(__file__))

# Initialize the LoginManager for managing user logins
login = LoginManager(myapp_obj)
login.login_view = 'login'

# Configure the app with secret key and database URI
myapp_obj.config.from_mapping(
    SECRET_KEY = 'you-will-never-guess',
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db'),
)
# Initialize the database
db = SQLAlchemy(myapp_obj)

from app import routes, models
