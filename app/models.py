from app import db
from app import login
from datetime import date, datetime
from flask_login import UserMixin

# Association table for Recipe-Tag many-to-many relationship
recipe_tags = db.Table('recipe_tags',
    db.Column('recipe_id', db.Integer, db.ForeignKey('recipe.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'), primary_key=True)
)

# User class 
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), unique=True)
    password = db.Column(db.String(32))
    email = db.Column(db.String(32), unique=True)
    
    # A user can have many recipes, comments, ratings
    recipes = db.relationship('Recipe', backref='user')
    comments = db.relationship('Comment', backref='user')
    ratings = db.relationship('Rating', backref='user')
    
    # Function that sets password
    def set_password(self, password):
        self.password = password
    
    # Function that checks password
    def check_password(self, password):
        return self.password == password

# Tag class
class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

# Recipe class
class Recipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=False)
    ingredients = db.Column(db.Text, nullable=False)
    instructions = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, default=date.today)    
    # Foreign key to link recipe to user
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)

    # A recipe can have many comments and ratings
    comments = db.relationship('Comment', backref='recipe_comments')
    ratings = db.relationship('Rating', backref='recipe_ratings')
    # Many-to-many relationship with Tag
    tags = db.relationship('Tag', secondary=recipe_tags, backref=db.backref('recipes'))
    
    def average_rating(self):
        if not self.ratings:
            return 0
        total = sum(rating.score for rating in self.ratings)
        return round(total / len(self.ratings), 1)

#Comment class
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.Date, default=date.today)    
    #Foreign key to link comments to recipes and users
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), index=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey(Recipe.id), index=True)

#Rating class
class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    #Foreign key to link ratings to recipes and users
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.id'), nullable=False)


# Load function to load user by id
@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))