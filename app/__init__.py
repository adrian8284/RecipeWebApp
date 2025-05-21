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

# Import models
from app.models import User, Recipe, Comment, Rating, Tag

# Initialize database and tags
with myapp_obj.app_context():
    db.create_all()
    # Populate tags 
    tags = ['dessert', 'gluten-free', 'breakfast', 'dinner', 'lunch', 'quick', 'healthy', 'spicy']
    for tag_name in tags:
        if not Tag.query.filter_by(name=tag_name).first():
            tag = Tag(name=tag_name)
            db.session.add(tag)
    db.session.commit()

from app import routes, models
