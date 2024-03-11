from app import app
from app import db, User, Recipe, Meal_plan, Comment, Favourite,Instruction,Ingredient

with app.app_context():
    db.drop_all()
    db.create_all()

    # Users
    user1 = User(name="John Kamau", email="johnkamau@example.com", phone_number="2345634222", password="password")
    user2 = User(name="Alice Wandia", email="alicewandia@example.com", phone_number="4567893222", password="password")
    user3 = User(name="Mike Ayieko", email="mikeayieko@example.com", phone_number="6889032222", password="password")
    user4 = User(name="Andriettah Mutoni", email="andriettahmuttoni@example.com", phone_number="6590432333", password="password")
    user5 = User(name="David Sakaja", email="davidsakaja@example.com", phone_number="6758902666", password="password")

    
    db.session.add(user1)
    db.session.add(user2)
    db.session.add(user3)
    db.session.add(user4)
    db.session.add(user5)

    db.session.commit()

    # Recipes
    recipes_data = [
        {
            'title': 'Caprese Salad',
            'description': 'Refreshing Italian salad',
            'category': 'Salad',
            'image_url': 'https://images.immediate.co.uk/production/volatile/sites/2/2016/07/24625.jpg?quality=90&resize=556,505',
            'prep_time': '10 minutes',
            'cook_time': '0 minutes',
            'user': user1.id,
            'ingredients': ['Tomatoes', 'Mozzarella', 'Basil', 'Balsamic vinegar'],
            'instructions': ['Slice tomatoes and mozzarella', 'Arrange on a plate', 'Add basil leaves', 'Drizzle with balsamic'],
            'ratings': [4.5, 5.0, 4.0]
        },
        {
            'title': 'Greek Salad',
            'description': 'Classic Greek salad',
            'category': 'Salad',
            'image_url': 'https://www.wellplated.com/wp-content/uploads/2022/05/Greek-Salad-Recipe-Easy.jpg',
            'prep_time': '10 minutes',
            'cook_time': '0 minutes',
            'user': user2.id,
            'ingredients': ['Cucumbers', 'Tomatoes', 'Onions', 'Feta cheese', 'Olives', 'Olive oil'],
            'instructions': ['Combine all ingredients', 'Dress with olive oil and vinegar'],
            'ratings': [4.0, 4.5, 3.5]
        },

         {
            'title': 'Chocolate Chip Cookies',
            'description': 'Classic chewy cookies',
            'category': 'Dessert',
            'image_url': 'https://cravebysaldemar.com/wp-content/uploads/2021/11/IMG_1222.jpg',
            'prep_time': '15 minutes',
            'cook_time': '10 minutes',
            'user': user3.id,
            'ingredients': ['Flour', 'Sugar', 'Butter', 'Eggs', 'Chocolate chips'],
            'instructions': ['Cream butter and sugar', 'Add eggs', 'Mix in dry ingredients', 'Fold in chocolate chips', 'Bake'],
            'ratings': [4.0, 4.5, 3.5]
        },
        {
            'title': 'Brownies',
            'description': 'Rich and fudgy brownies',
            'category': 'Dessert',
            'image_url': 'https://www.southernliving.com/thmb/eLSgazITlYrKf9EFTR9y1L2mSxg=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/Southern-Living-Homemade_Brownies_023-3c582f0fba1842dd918a3d9c26c1ab59.jpg',
            'prep_time': '15 minutes',
            'cook_time': '25 minutes',
            'user': user1.id,
            'ingredients': ['Flour', 'Sugar', 'Cocoa powder', 'Eggs', 'Butter'],
            'instructions': ['Melt butter and chocolate', 'Mix in dry ingredients', 'Add eggs', 'Bake'],
            'ratings': [4.5, 5.0, 4.0]
        },
       
        {
            'title': 'Vegetable Curry',
            'description': 'Flavorful vegan curry',
            'category': 'Vegetarian',
            'image_url': 'https://www.cookwithmanali.com/wp-content/uploads/2023/01/Mixed-Veg-Sabzi-500x500.jpg',
            'prep_time': '20 minutes',
            'cook_time': '30 minutes',
            'user': user2.id,
            'ingredients': ['Vegetables', 'Curry paste', 'Coconut milk', 'Rice'],
            'instructions': [
                'Sauté vegetables',
                'Add curry paste',
                'Stir in coconut milk',
                'Simmer',
                'Serve over rice'
            ],
            'ratings': [4.0, 4.5, 3.5]
        },

        {
            'title': 'Lentil Soup',
            'description': 'Hearty and healthy lentil soup',
            'category': 'Vegetarian',
            'image_url': 'https://www.howtocook.recipes/wp-content/uploads/2021/10/Lentil-soup-recipe-500x500.jpg',
            'prep_time': '15 minutes',
            'cook_time': '30 minutes',
            'user': user3.id,
            'ingredients': ['Lentils', 'Vegetables', 'Broth', 'Spices'],
            'instructions': [
                'Sauté vegetables',
                'Add lentils and broth',
                'Simmer until lentils are tender'
            ],
            'ratings': [4.2, 3.8, 4.5]
        },

        {
            'title': 'Avocado Toast',
            'description': 'Simple and nutritious snack',
            'category': 'Snacks',
            'image_url': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRxA8pqZVVMSHYVrwYtyhvOodpF8W-hiu3jr9cGpKEOCxWr-IHtPVvIiDqAcd9jfqd_WHc&usqp=CAU',
            'prep_time': '5 minutes',
            'cook_time': '0 minutes',
            'user': user1.id,
            'ingredients': ['Toast', 'Avocado', 'Olive oil', 'Salt', 'Pepper'],
            'instructions': [
                'Toast bread',
                'Mash avocado',
                'Spread on toast',
                'Drizzle with olive oil',
                'Season with salt and pepper'
            ],
            'ratings': [4.5, 4.0, 4.2]
        },

        {
            'title': 'Hummus and Pita Bread',
            'description': 'Easy and flavorful snack',
            'category': 'Snacks',
            'image_url': 'https://entertainingwithbeth.com/wp-content/uploads/2021/02/homemade-hummus-dip-recipe.jpg',
            'prep_time': '5 minutes',
            'cook_time': '0 minutes',
            'user': user4.id,
            'ingredients': ['Hummus', 'Pita bread', 'Vegetables'],
            'instructions': ['Serve hummus with pita bread and vegetables for dipping'],
            'ratings': [4.8, 4.2, 4.7]
        },

        {
            'title': 'Spaghetti Bolognese',
            'description': 'Classic Italian comfort food',
            'category': 'Full Dish',
            'image_url': 'https://img.hellofresh.com/hellofresh_s3/image/624c4724d734d42cde0d5c2e-b1fb90f6.jpg',
            'prep_time': '20 minutes',
            'cook_time': '30 minutes',
            'user': user4.id,
            'ingredients': ['Ground beef', 'Pasta', 'Tomato sauce', 'Vegetables'],
            'instructions': [
                'Cook pasta according to package directions',
                'Brown ground beef',
                'Add tomato sauce and vegetables',
                'Simmer',
                'Serve sauce over pasta'
            ],
            'ratings': [4.2, 4.0, 4.5]
        },

        {
            'title': 'Chicken Tikka Masala',
            'description': 'Flavorful Indian dish',
            'category': 'Full Dish',
            'image_url': 'https://www.supergoldenbakes.com/wordpress/wp-content/uploads/2023/09/Air_Fryer_Chicken_Tikka_Masala.jpg',
            'prep_time': '25 minutes',
            'cook_time': '35 minutes',
            'user': user5.id,
            'ingredients': ['Chicken', 'Curry paste', 'Coconut milk', 'Rice'],
            'instructions': [
                'Marinate chicken in curry paste',
                'Cook chicken',
                'Add coconut milk and simmer',
                'Serve with rice'
            ],
            'ratings': [4.5, 4.2, 4.8]
        },

        {
            'title': 'Eggs Benedict',
            'description': 'Elegant breakfast dish',
            'category': 'Breakfast',
            'image_url': 'https://www.foodandwine.com/thmb/kjM9_X7pnPTVjj3GXgoDnwQe7YI=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/smoked-salmon-eggs-benedict-FT-RECIPE0822-2000-dafeba30c20843589e734be9c8ee30f7.jpg',
            'prep_time': '15 minutes',
            'cook_time': '10 minutes',
            'user': user3.id,
            'ingredients': ['English muffins', 'Eggs', 'Hollandaise sauce', 'Ham'],
            'instructions': [
                'Toast English muffins',
                'Poach eggs',
                'Make hollandaise sauce',
                'Layer ham, eggs, and hollandaise on muffins'
            ],
            'ratings': [4.0, 4.5, 3.8]
        },

        {
            'title': 'Blueberry Pancakes',
            'description': 'Delicious and fluffy pancakes',
            'category': 'Breakfast',
            'image_url': 'https://www.mieleexperience.com.au/wp-content/uploads/2017/08/SDH_170608_3785sm_Insta_oatmeal-chia-ricotta-pancakes-w-blueberry-maple-syrup_angled3_spring17.jpg',
            'prep_time': '10 minutes',
            'cook_time': '5 minutes',
            'user': user5.id,
            'ingredients': ['Flour', 'Milk', 'Eggs', 'Blueberries'],
            'instructions': [
                'Mix dry ingredients',
                'Add wet ingredients and mix until just combined',
                'Fold in blueberries',
                'Cook pancakes on a griddle'
            ],
            'ratings': [4.2, 4.5, 4.8]
        }

    ]

    # Seed the database with sample data
    for recipe_data in recipes_data:
        user_id = recipe_data['user']  # Access the user ID instead of the user object

        new_recipe = Recipe(
            title=recipe_data['title'],
            description=recipe_data['description'],
            category=recipe_data['category'],
            image_url=recipe_data['image_url'],
            prep_time=recipe_data['prep_time'],
            cook_time=recipe_data['cook_time'],
            user_id=user_id,  # Assign the user ID
            total_ratings=sum(recipe_data['ratings']),
            num_ratings=len(recipe_data['ratings'])
        )

        for ingredient_content in recipe_data['ingredients']:
            new_ingredient = Ingredient(content=ingredient_content, recipe=new_recipe)
            db.session.add(new_ingredient)

        for instruction_content in recipe_data['instructions']:
            new_instruction = Instruction(content=instruction_content, recipe=new_recipe)
            db.session.add(new_instruction)

        db.session.add(new_recipe)

    db.session.commit()

    
    # Meal Plans
    meal_plan1 = Meal_plan(
        price=20, title="Weekly Meal Prep", description="Healthy and delicious meals for the week", user=user1
    )
    meal_plan2 = Meal_plan(
        price=15, title="Budget-Friendly Dinners", description="Affordable and satisfying dinners", user=user2
    )
    meal_plan3 = Meal_plan(
        price=25, title="Healthy Plant-Based Options", description="Nutritious and flavorful plant-based dishes", user=user3
    )
    meal_plan4 = Meal_plan(
        price=30, title="Family-Friendly Favorites", description="Kid-approved recipes for the whole family", user=user4
    )
    meal_plan5 = Meal_plan(
        price=35, title="International Cuisine Exploration", description="Explore new flavors from around the world", user=user5
    )
    db.session.add_all([meal_plan1, meal_plan2, meal_plan3, meal_plan4, meal_plan5])
    db.session.commit()



    comments_data = [
        {
            'comment': 'This salad is amazing!',
            'recipe_title': 'Caprese Salad',
        },
        {
            'comment': 'I love this Greek salad!',
            'recipe_title': 'Greek Salad',
        }
    
    ]

    # Seed the database with sample comments
    for comment_data in comments_data:
        recipe = Recipe.query.filter_by(title=comment_data['recipe_title']).first()
        
        if recipe:
            new_comment = Comment(comment=comment_data['comment'], recipe=recipe)
            db.session.add(new_comment)

    db.session.commit()



print("Database seeding completed successfully.")
