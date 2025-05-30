from app import myapp_obj
from app.forms import LoginForm, RecipeForm, RegistrationForm, CommentForm, RatingForm, EditProfileForm
from app.models import User, Recipe, Comment, Rating, Tag, recipe_tags
from app import db
from flask import redirect, render_template, request, flash, url_for
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from urllib.parse import urlsplit

# If logged in, shows current user's profile information, their recipes and saved recipes
@myapp_obj.route("/profile")
@login_required
def show_recipes():
    recipes = Recipe.query.filter_by(user_id=current_user.id).all()
    saved_recipes = current_user.saved_recipes
    return render_template("all_recipes.html", user=current_user, recipes=recipes, saved_recipes = saved_recipes)

# Shows all users and their recipe regardless if logged in or not
@myapp_obj.route("/")
@myapp_obj.route("/home", methods=['GET', 'POST'])
def home():
    users = User.query.all()
    tags = Tag.query.order_by(Tag.name).all()
    trending_recipes = Recipe.query.filter(Recipe.views > 0).order_by(Recipe.views.desc()).limit(5).all()
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

    return render_template("home.html", users=users, tags=tags, selected_tags=selected_tags, filtered_recipes=filtered_recipes,trending_recipes=trending_recipes)

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

    recipe.views += 1
    db.session.commit()

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
    
    if request.method == "POST" and request.form.get("form_type") == "save_toggle":
        if recipe in current_user.saved_recipes:
            current_user.saved_recipes.remove(recipe)
            flash("Recipe removed from favorites!")
        else:
            current_user.saved_recipes.append(recipe)
            flash("Recipe added to favorites!")
        db.session.commit()
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

@myapp_obj.route("/recipe/edit/<int:recipe_id>", methods=['GET', 'POST'])
@login_required
def edit_recipe(recipe_id):
    recipe = Recipe.query.get_or_404(recipe_id)
    if recipe.user_id != current_user.id:
        flash("You are not authorized to edit this recipe.", "danger")
        return redirect(url_for("show_recipes"))

    form = RecipeForm(obj=recipe)

    if form.validate_on_submit():
        recipe.title = form.title.data
        recipe.description = form.description.data
        recipe.ingredients = form.ingredients.data
        recipe.instructions = form.instructions.data
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags.data)).all()
        recipe.tags = selected_tags
        db.session.commit()
        flash("Recipe updated successfully!", "success")
        return redirect(url_for("show_recipe", integer=recipe.id))

    return render_template("new_recipe.html", form=form, active_page="new_recipe")

# Edit Profile page
@myapp_obj.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        if form.username.data:
            current_user.username = form.username.data
        if form.email.data:
            current_user.email = form.email.data
        if form.password.data:
            current_user.set_password(form.password.data)

        db.session.commit()
        flash("Your profile has been updated!")
        return redirect(url_for("show_recipes"))

    return render_template("edit_profile.html", title='Edit Profile', form=form)

# Search for recipes based on available ingredients
@myapp_obj.route("/cook_now", methods=["GET", "POST"])
@login_required
def cook_now():
    matched_recipes = []
    close_recipes = []
    input_ingredients_list = []

    if request.method == "POST":
        # Get raw input and clean it
        input_ingredients = request.form.get("ingredients", "").strip().lower()
        max_missing = request.form.get("max_missing", 3)
        try:
            max_missing = int(max_missing)
        except ValueError:
            max_missing = 3

        # Parse and clean ingredients list
        for i in input_ingredients.split(","):
            clean_i = i.strip()
            if clean_i:
                input_ingredients_list.append(clean_i)

        all_recipes = Recipe.query.all()

        # Search through recipes
        for recipe in all_recipes:
            # Parse recipe ingredients
            recipe_ingredients = []
            for i in recipe.ingredients.splitlines():
                clean_ingredient = i.strip().lower()
                if clean_ingredient:
                    recipe_ingredients.append(clean_ingredient)

            # Find matching & missing ingredients
            matched = set()
            missing_ingredients = set()

            for rec_ing in recipe_ingredients:
                match_found = False
                for user_ing in input_ingredients_list:
                    if user_ing in rec_ing:
                        matched.add(user_ing)
                        match_found = True
                        break
                if not match_found:
                    missing_ingredients.add(rec_ing)

            matched = list(matched)
            missing_ingredients = list(missing_ingredients)

            # Sort matched vs close
            if not missing_ingredients:
                matched_recipes.append((recipe, matched))
            elif len(missing_ingredients) <= max_missing:
                close_recipes.append((recipe, matched, missing_ingredients))

        # Sort close matches by fewest ingredients missing
        def sort_by_missing(item):
            recipe, matched, missing = item
            return len(missing)

        close_recipes.sort(key=sort_by_missing)

    return render_template(
        "cook_now.html",
        matched_recipes=matched_recipes,
        close_recipes=close_recipes,
        input_ingredients_list=input_ingredients_list
    )
