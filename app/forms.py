from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectMultipleField
from wtforms.validators import Email, EqualTo, DataRequired, Length, ValidationError, NumberRange
import sqlalchemy as sa
from app import db
from app.models import User, Tag

# Login form with fields for username, password, and submit button
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=4, max=35)])
    submit = SubmitField("Sign in")
    remember_me = BooleanField("Remember Me")

# Recipe form with fields for title, description, ingredients, and instructions
class RecipeForm(FlaskForm):
    title = StringField('Recipe', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients', validators=[DataRequired()])
    instructions = TextAreaField('Instructions', validators=[DataRequired()])
    tags = SelectMultipleField('Tags', coerce=int, validators=[DataRequired(message="Select at least one tag")])
    submit = SubmitField('Submit')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by(Tag.name).all()]


class CommentForm(FlaskForm):
    content = TextAreaField('Post what you think!', 
        render_kw={"placeholder ": "Add a comment..."}, validators=[DataRequired(message="Comment cannot be empty.")])
    submit = SubmitField('Post')

class RatingForm(FlaskForm):
    score = IntegerField('Rating', validators=[DataRequired(), NumberRange(min=1, max=5)])
    submit = SubmitField('Submit Rating')

# Registration form with fields for username, email, password, and password confirmation
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField("Re-Enter Password", validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    
    # Validates username to check if it already exists
    def validate_username(self, username):
        user = db.session.scalar(sa.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Username already taken')
    
    # Validates email to check if it already exists
    def validate_email(self, email):
        user = db.session.scalar(sa.select(User).where(User.email == email.data))
        if user is not None:
            raise ValidationError('Email already registered. Use a different email.')
