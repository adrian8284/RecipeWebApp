from app import myapp_obj
from app.forms import LoginForm, RecipeForm, RegistrationForm, CommentForm, RatingForm
from app.models import User, Recipe, Comment, Rating, Tag, recipe_tags
from app import db
from flask import redirect, render_template, request, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit

# Shows current user, if logged in, recipes
@myapp_obj.route("/recipes")
@login_required
def show_recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    return render_template("all_recipes.html", recipes=recipes)

# Shows all users and their recipe regardless if logged in or not
@myapp_obj.route("/")
@myapp_obj.route("/home", methods=['GET', 'POST'])
def home():
    users = User.query.all()
    tags = Tag.query.order_by(Tag.name).all()
    selected_tags = []
    filtered_recipes = None

    if request.method == 'POST':
        selected_tags = request.form.getlist('tags')
        if selected_tags:
            selected_tags = [int(tag_id) for tag_id in selected_tags]
            filtered_recipes = Recipe.query.join(recipe_tags).join(Tag).filter(
                Tag.id.in_(selected_tags)
            ).group_by(Recipe.id).having(
                sa.func.count(Tag.id) == len(selected_tags)
            ).all()
            if not filtered_recipes:
                flash('No recipes match the selected tags.', 'info')
        else:
            flash('Please select at least one tag.', 'error')

    return render_template("home.html", users=users, tags=tags, selected_tags=selected_tags, filtered_recipes=filtered_recipes)

@myapp_obj.route("/search", methods=['GET', 'POST'])
def search():
    user_input = None
    search_results = None

    if request.method == 'POST':
        user_input = request.form.get('user_input', '').strip()
        if not user_input:
            flash('Please enter a recipe title or ingredient to search.')
        else:
            search_results = Recipe.query.filter(
                sa.or_(
                    Recipe.title.ilike(f'%{user_input}%'),
                    Recipe.ingredients.ilike(f'%{user_input}%')
                )
            ).all()
    return render_template("search.html", user_input=user_input, search_results=search_results)


# Shows more details of a specific recipe
@myapp_obj.route("/recipe/<int:integer>", methods=['GET', 'POST'])
@login_required
def show_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    comment_form = CommentForm()
    rating_form = RatingForm()

    if comment_form.validate_on_submit():
        comment = Comment(
            content = comment_form.content.data,
            user_id = current_user.id,
            recipe_id = recipe.id
            )
        db.session.add(comment)
        db.session.commit()
        flash('Comment, posted!')
        return redirect(url_for('show_recipe', integer=recipe.id))
    
    if rating_form.validate_on_submit():
        rating = Rating(
            score = rating_form.score.data,
            user_id = current_user.id,
            recipe_id = recipe.id
        )
        db.session.add(rating)
        db.session.commit()
        flash('Rating submitted!')
        return redirect(url_for('show_recipe', integer=recipe.id))
    return render_template("recipe_details.html", recipe=recipe, 
                           comment_form=comment_form, rating_form=rating_form)

# Url that deletes recipe 
@myapp_obj.route("/recipe/<integer>/delete", methods=['GET'])
@login_required
def delete_recipe(integer):
    recipe = Recipe.query.get_or_404(integer)
    if recipe.user_id != current_user.id:
        flash('You can only delete your own recipes.')
        return redirect(url_for('show_recipes'))
    db.session.delete(recipe)
    db.session.commit()
    return render_template("recipe_deleted.html")

# Login page to sign in 
@myapp_obj.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('show_recipes'))
    
    form = LoginForm()
        
    if form.validate_on_submit():
        user = db.session.scalar(sa.select(User).where(User.username == form.username.data))
        
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('show_recipes')
        return redirect(next_page)
    return render_template("login.html", title="Login", form=form)

# Logs out current user
@myapp_obj.route("/logout")
def logout():
    logout_user()
    return redirect("login")

# Register page
@myapp_obj.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('recipes'))
    
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a user!')
        return redirect(url_for('login'))
    return render_template("register.html", title='Register', form=form)

# Page to create new recipes
@myapp_obj.route("/recipe/new", methods=['GET', 'POST'])
@login_required
def new_recipe():
    form = RecipeForm()
    if form.validate_on_submit():
        recipe = Recipe(
            title=form.title.data, 
            description=form.description.data,
            ingredients=form.ingredients.data,
            instructions=form.instructions.data,
            user_id=current_user.id
            )
        db.session.add(recipe)
        db.session.commit()
        # Add selected tags to the recipe
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        recipe.tags = selected_tags
        db.session.add(recipe)
        db.session.commit()
        flash('Recipe created!', 'success')
        return redirect("/")
    return render_template("new_recipe.html", form=form)