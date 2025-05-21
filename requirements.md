## Functional Requirements

1. User Registration - A visitor can create an account by providing a username, email, and password.

2. User Login - Registered users can log in using their email and password.

3. User Logout - Logged-in users can log out of their account securely.

4. Create Recipe - Logged-in users can add new recipes with title, description, ingredients, and instructions.

5. Edit Recipe - Users can update their own recipes after creation.

6. Delete Recipe - Users can delete their own recipes.

7. View Recipe - Anyone can view the details of a recipe including ingredients and instructions.

8. Search Recipe - Users can search recipes by title or ingredient keywords.

9. Filter Recipes - Users can filter recipes by tags like 'vegan', 'dessert', etc.

10. Rate Recipe - Users can rate a recipe from 1 to 5 stars.

11. Comment on Recipe - Users can leave comments on a recipe.

12. View All Recipes - Homepage or main recipe list shows all recipes available in the database.

13. View User Profile - Users can view their own profile, including their submitted recipes.

14. Edit User Profile - Users can update their display name, email, or password.

15. Save Recipe (Favorites) - Users can save or 'favorite' recipes for quick access later.

16. Spit Out Recipes Based on Ingredients - Suggest recipes based on user's available ingredients.

17. Recipe Image API Integration - Use an external API to retrieve and display images for recipes.

18. Trending Now - Users can view some of the most viewed recipes.

## Use Cases

### 1. User Registration (Handled by: Irving Bautista)

- **Summary:** A visitor can create an account by providing a username, email, and password.

- **Pre-condition:** User is not currently logged in.

- **Trigger:** User clicks "Register"

- **Primary Sequence:**

    1. User clicks the "Register" button.

    2. System produces the register form with username, email, and password.

    3. User fills out the form.

    4. System validates form fields.

    5. If valid, system saves the user account info into the database.

    6. User is now logged in and redirected to the logged in home page.

- **Primary Postconditions:** User account is saved into database, and is logged in.

- **Alternate Sequence:**

    1. Email or username already exists.

    2. System produces an error message, such as "Email/Username already exists."

    3. User remains on the form page, with only valid input preserved.

- **Alternate Sequence:**

    1. Email, username, or password is invalid.

    2. System produces an error message, such as "Email/Username/Password is invalid."

    3. User remains on the form page, with only valid input preserved.

### 2. User Login (Handled by: Irving Bautista)

- **Summary:** Registered users can log in using their email and password.

- **Pre-condition:** User has a registered account and is not logged in.

- **Trigger:** User clicks "Log In"

- **Primary Sequence:**

    1. User clicks the "Log In" button.

    2. System produces the log in form, with email and password.

    3. User fills out the form.

    4. System validates the form fields.

    5. If valid, system logs in the user.

    6. User is now logged in and redirected to the logged in home page.

- **Primary Postconditions:** User is logged in.

- **Alternate Sequence:**

    1. User inputs an incorrect email or password.

    2. System produces an error message, such as "Incorrect email or password".

    3. User remains on the form page, email is preserved (if it exists in database).

- **Alternate Sequence:**

    1. User has forgotten their password.

    2. User clicks the "Forgot password" button.

    3. System sends a verification code to user email, and redirects user to user verification page.

    4. User inputs verification code.

    5. System validates the verification code.

    6. If valid, system produces the reset password form.

    7. System validates the password form fields.

    8. If valid, system updates user account password, and logs in the user.

    9. User is now logged in and redirected to the logged in home page.

### 3. User Logout (Handled by: Irving Bautista)

- **Summary:** Logged-in users can log out of their account securely.

- **Pre-condition:** User is logged in.

- **Trigger:** User clicks "Log Out"

- **Primary Sequence:**

    1. User clicks the "Log Out" button.

    2. System logs out the user.

    3. User is now logged out and redirected to the logged out home page.

- **Primary Postconditions:** User is logged out.

- **Alternate Sequence:** N/A

### 4. Create Recipe (Handled by: Irving Bautista)

- **Summary:** Logged-in users can add new recipes with title, description, ingredients, and instructions.

- **Pre-condition:** User is logged in.

- **Trigger:** User clicks “Add New Recipe”

- **Primary Sequence:**

    1. User clicks the “Add New Recipe” button.

    2. System produces the recipe form with title, description, ingredients, and instructions.

    3. User fills out the form.

    4. System validates form fields.

    5. If valid, the system saves the recipe into the database.

    6. User is redirected to the newly created recipe page, or recipe list.

- **Primary Postconditions:** New recipe is saved into the database.

- **Alternate Sequence:**

    1. Required fields are missing.

    2. System produces an error message, such as “Title is required.”

    3. User remains on the form page, with input preserved.

### 5. Edit Recipe (Handled by: Adrian Agustin)

- **Summary:** Users can update their own recipes after creation.

- **Pre-condition:** User is logged in and has a pre-existing recipe in the database.

- **Trigger:** User clicks “Edit Recipe”

- **Primary Sequence:**

    1. User clicks the “Edit Recipe” button.

    2. System produces the existing recipe form, with existing input preserved.

    3. User makes changes to the form.

    4. System validates form fields.

    5. If valid, the system saves the recipe into the database.

    6. User is redirected to the edited recipe page, or recipe list.

- **Primary Postconditions:** Recipe changes are updated to the database.

- **Alternate Sequence:**

    1. Existing required field is cleared and missing.

    2. System produces an error message, such as “Description is required.”

    3. User remains on the form page, with input preserved.

### 6. Delete Recipe (Handled by: Irving Bautista)

- **Summary:** Users can delete their own recipes.

- **Pre-condition:** User is logged in and has a pre-existing recipe in the database.

- **Trigger:** User clicks “Delete Recipe” button.

- **Primary Sequence:**

    1. User clicks "Delete Recipe" button.

    2. System produces a verification message, such as "You are about to delete this recipe permanently. Are you sure?"

    3. User clicks "Yes" button.

    4. System deletes the recipe from the database.

    5. User recipe is now deleted, and user is redirected to updated recipe list.

- **Primary Postconditions:** Existing recipe is deleted from database.

- **Alternate Sequence:**

    1. User changes their mind, and clicks "No" button.
    
    2. User remains on the recipe page.

### 7. View Recipe (Handled by: Irving Bautista)

- **Summary:** Anyone can view the details of a recipe including ingredients and instructions.

- **Pre-condition:** User is on the recipe list page.

- **Trigger:** User clicks on recipe.

- **Primary Sequence:**

    1. User clicks on the desired recipe.

    2. System produces specific recipe details page.

    3. User is redirected to the specific recipe details page.

- **Primary Postconditions:** User is on the recipe details page.

- **Alternate Sequence:** N/A

### 8. Search Recipe (Handled by: Irving Bautista)

- **Summary:** Users can search recipes by title or ingredient keywords.

- **Pre-condition:** User is on the recipe page

- **Trigger:** User types in recipe or keyword in the search bar and clicks search or enter

- **Primary Sequence:**

    1. User navigates to recipe page

    2. User enters recipe or ingredient keywords in the search field

    3. User clicks search or hits Enter

    4. The system retrieves from the database the recipes containing the keywords

    5. A list of ingredients is displayed on the page containing keywords user entered

- **Primary Postconditions:**

    - The system displays various recipes matching the user’s input

    - The user is able to interact with the list of recipes

- **Alternate Sequence:**

    1. The user leaves search field blank

    2. The system prompts user to enter a valid recipe/keyword

    3. User then clicks submit

### 9. Rate Recipe (Handled by: Irving Bautista)

- **Summary:** Users can rate a recipe from 1 to 5 stars.

- **Pre-condition:** The user has selected a recipe and is logged in

- **Trigger:** User clicks on the star rating system displayed when viewing recipe

- **Primary Sequence:**

    1. User selects a recipe from the recipe page

    2. A rating system is displayed along with description, date created, etc

    3. The user can select from 1 to 5 stars

    4. The system saves the rating

    5. The system updates overall rating of the recipe

    6. The system displays a message confirming rating was successful

- **Primary Postconditions:**

    - User’s rating is stored in the system

    - The number of stars the user selected are highlighted

- **Alternate Sequence:**

    1. The user already rated the recipe

    2. The system updates the previously selected rating

    3. The overall rating is updated

### 10. Comment on Recipe (Handled by: Irving Bautista)

- **Summary:** Users can leave comments on a recipe.

- **Pre-condition:** The user has selected a recipe and is logged in

- **Trigger:** User selects the option to leave a comment

- **Primary Sequence:**

    1. User selects a recipe from the recipe page

    2. An ingredients information is displayed (rating, title, description) along with comments

    3. The user selects the option to leave a comment

    4. A textbox is displayed where the user can enter their comment

    5. The user selects post button

    6. The system validates the comment

    7. User’s comment is displayed in the comment section

- **Primary Postconditions:**

    - The comment is displayed immediately

- **Alternate Sequence:**

    1. User submits an invalid comment that is empty or too long

    2. An error message is displayed

    3. User can try again

### 11. View All Recipes (Handled by: Irving Bautista)

- **Summary:** Homepage or main recipe list shows all recipes available in the database.

- **Pre-condition:** At least one recipe is in the database

- **Trigger:** User accesses the homepage or recipe list

- **Primary Sequence:**

    1. User selects the homepage/main recipe list

    2. The system fetches all recipes in the database

    3. A list of all the recipes then displayed

    4. The user selects the recipe of their choice

    5. The user is taken to that specific recipe for more information

- **Primary Postconditions:**

    - A list of recipes is displayed

- **Alternate Sequence:**

    1. No recipes are in the database

    2. The page displays a message informing the user

### 12. Filter Recipes (Handled by: Irving Bautista)

- **Summary:** Users can filter recipes by tags like 'vegan', 'dessert', etc.

- **Pre-condition:** Recipes are tagged with categories

- **Trigger:** User selects one or many tags

- **Primary Sequence:**

    1. User is in the homepage

    2. User selects tags displayed on the homepage

    3. User selects one or many tags

    4. The system retrieves recipes containing the user selected filters

    5. The system displays all recipes containing those tags

- **Primary Postconditions:**

    - The user sees a list of recipes based on selected tags

    - The tags are visible and selected filters are highlighted

- **Alternate Sequence:**

    1. No recipes match the filters

    2. A message is displayed informing the user

    3. User can clear filters or select a different combination of filters

### 13. View User Profile (Handled by: Kirill Vladimirov)

- **Summary:** Users can view their own profile, including their submitted recipes.

- **Pre-condition:** User is logged in.

- **Trigger:** User selects “Profile” from the navigation menu.

- **Primary Sequence:** 

    1. User clicks on "Profile" menu item.

    2. System routes user to their profile page.

    3. System loads user’s profile data from the database.

    4. System displays user information on the page:  username, email

    5. System displays all recipes submitted by the user.

- **Primary Postconditions:**

    1. User views their profile information.

- **Alternate Sequence:**

    5. If user has no recipes, "No recipes yet. Add your first one!" message is displayed instead.

### 14. Edit User Profile (Handled by: Kirill Vladimirov)

- **Summary:** Users can update their username, email, or password.

- **Pre-condition:** User is logged in.

- **Trigger:** User clicks on the “Edit Profile” button from their profile page.

- **Primary Sequence:**

    1. System displays form with current username, email, and a password with an option to edit one or more fields.

    2. User updates one or more fields and clicks "Save changes"

    3. System validates submitted form fields.

    4. If valid, system updates the database.

    5. System displays "Information updated successfully." message.

- **Primary Postconditions:**

    - User's profile page displayed with updated information.

    - Database is updated with the users new information.

- **Alternate Sequence:**

    1. User submits information and one or more fields are invalid

    2. System displays error message with specified failed input.

    3. User remains on the same form page and is able to edit the form with correct information.

    4. User fixes errors and submits the form



### 15. Save Recipe (Favorites) (Handled by: Kirill Vladimirov)

- **Summary:** Users can save or 'favorite' recipes for quick access later.

- **Pre-condition:** 

    - User is logged in. 

    - User is viewing recipe they want to add to favorites.

    - Recipe is not added to favorites yet

- **Trigger:** User clicks "Save" button on a recipe page.

- **Primary Sequence:**

    1. User clicks on the recipe.

    2. User clicks on "Save" button

    3. System adds the recipe to the user's list of favorites.

    4. System updates database 

    5. System displays confirmation message: "Recipe is saved!"

    6. Button changes to indicate recipe is saved now.

- **Primary Postconditions:**

    - Recipe is saved to user's list of favorites.

    - DB is updated with the user's saved recipe.

### 16. Spit Out Recipes Based on Ingredients (Handled by: Kirill Vladimirov)

- **Summary:** Suggest recipes based on user's available ingredients.

- **Pre-condition:** 

    - User is on the “What Can I Make?” page

    - System has recipes with indexed ingredient lists in the database.

- **Trigger:** User enters one or more ingredients into the input field and clicks “Find Recipes”.

- **Primary Sequence:**

    1. User types in a list of available ingredients (e.g., “eggs, milk, tomato”) into the search field.

    2. User submits the list.

    3. System splits the input into individual ingredients and matches it against stored recipes and their ingredients.

    4. System filters recipes based on the number of matching ingredients.

    5. System displays on the webpage a list of recipes the user can make or can almost make.

    6. Each result has: title, description, and a list of missing ingredients if any (“Missing: tomato”).

- **Primary Postconditions:**	

    - User sees a list of recipes based on the provided ingredients.

    - Matching recipes are retrieved from the database and displayed on the page.

- **Alternate Sequence 1:**

    1. User submits empty form with no ingredients.

    2. System displays an error message: "Please, enter at least 1 ingredient"

    3. User is allowed to type into the search field and submit with corrected error.

- **Alternate Sequence 2:**

    1. No recipes with matched ingredients found.

    2. System displays "No recipes found with the provided ingredients. Try to enter different ingredients."

### 17. Recipe Image API Integration (Handled by: Kirill Vladimirov)

- **Summary:** Use an external API to get and display images for recipes.

- **Pre-condition:**

    - Recipe has a clear and correct title or keywords.

    - System is connected to an external image API

- **Trigger:** A recipe is viewed.

- **Primary Sequence:**

    1. User views a recipe.

    2. System checks if the recipe already has an image associated with it. 

    3. If not, system gets the recipe tittle and send request to image API.

    4. API provides a list of relevant pictures.

    5. System selects the 1st image and retrieve it's URL.

    6. System updates the database for the recipe with the retrieved URL.

    7. System uses image's URL to embed the picture on the recipe page.

- **Primary Postconditions:**

    - On the recipe's page, there is a photo of the finished dish.

- **Alternate Sequence:**

    1. API fails to return image URL

    2. System uses default image.

### 18. Trending Now (Handled by: Adrian Agustin)

- **Summary:** Users can view some of the most viewed recipes

- **Pre-condition:** At least one recipe is trending

- **Trigger:** User selects the trending tab or opens homepage

- **Primary Sequence:**

    1. The user selects the trending tab or opens the homepage

    2. The system displays some of the recipes with the most views

    3. Recipe information is displayed like rating, images, etc

    4. User selects a specific recipe to view more information

- **Primary Postconditions:**

    - The user views more information based on the recipe selected

    - The user views some of the trending recipes

- **Alternate Sequence:**

    1. The system displays a message stating there are no trending recipes

