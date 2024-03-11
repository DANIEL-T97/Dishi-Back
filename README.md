# Recipe App

## Introduction

This is a Flask-based backend for a Dishi-Tamu recipe app. It includes functionality for user management, recipes, comments, favorites, and meal plans.

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/Joyceachieng123/Dishi-Tamu-Webapp-backend
   ```

2. Navigate to the project directory:

   ```bash
   cd recipe-app
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Set up your database:

   - Create a database (e.g., PostgreSQL) and update the `SQLALCHEMY_DATABASE_URI` in the `app.py` file.

5. Run the application:
   ```bash
   python app.py
   ```

## Features

- User authentication and authorization using JWT tokens and bcrypt for password hashing.
- CRUD operations for recipes, comments, favorites, and meal plans.
- Email verification and confirmation for user sign up.
- Automatic initialization of Recipe, Comment, Favorite, and MealPlan lists for new users.

## API Endpoints

- **/signup** (POST): Create a new user account.
- **/login** (POST): Log in and obtain JWT tokens.
- **/refresh** (POST): Refresh the access token.
- **/users** (GET, POST): Get all users or create a new user.
- **/users/{id}** (GET, PATCH): Get user details or update user information.
- **/recipes** (GET, POST): Get all recipes or create a new recipe.
- **/recipes/{id}** (GET, PATCH, DELETE): Get, update, or delete a specific recipe.
- **/comments** (GET, POST): Get all comments or create a new comment.
- **/comments/{id}** (GET, PATCH, DELETE): Get, update, or delete a specific comment.
- **/favorites** (GET, POST): Get all favorites or create a new favorite.
- **/favorites/{id}** (GET, PATCH, DELETE): Get, update, or delete a specific favorite.
- **/mealplans** (GET, POST): Get all meal plans or create a new meal plan.
- **/mealplans/{id}** (GET, PATCH, DELETE): Get, update, or delete a specific meal plan.

## Usage

- Ensure the backend is running and accessible.
- Use a tool like ThunderClient or Postman to test the different endpoints.
- Include the necessary headers, such as Content-Type and Authorization with the JWT token.

## Contributors

- [Joyce Achieng](https://github.com/Joyceachieng123)
- [Daniel Mwangi](https://github.com/DANIEL-T97)
- [Sheila Chepkemoi](https://github.com/sheilabett)
- [Joseph Kagwi](https://github.com/joseph123-wq)
- [Klein Rutto](https://github.com/ruttoklein)
- [Isaac Kiplangat](https://github.com/isaac-kiplangat)

## License

This project is licensed under the [MIT License](LICENSE).
