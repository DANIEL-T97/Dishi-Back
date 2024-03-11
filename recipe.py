from flask import jsonify, request,Response,json
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy.exc import SQLAlchemyError
from models import Recipe, Ingredient, Instruction, db, User
import cloudinary
import cloudinary.uploader


import logging

# Configure Cloudinary with your credentials       
cloudinary.config( 
  cloud_name = "dzcexrbjs", 
  api_key = "248311674828873", 
  api_secret = "lZdDDH2G6fVsclVsb4WsbSM1pzE" 
)

def handle_error(e, status_code):
    logging.error(str(e))
    return jsonify({'error': str(e)}), status_code

class RecipesResource(Resource):

    
    def get(self, recipe_id):
        try:
            recipe = Recipe.query.get_or_404(recipe_id)
            average_rating = recipe.average_rating
            user_name = None

            if recipe.user_id:
                user = User.query.get(recipe.user_id)
                if user:
                    user_name = user.name

            result = {
                'id': recipe.id,
                'title': recipe.title,
                'ingredients': [ingredient.content for ingredient in recipe.ingredients],
                'instructions': [instruction.content for instruction in recipe.instructions],
                'description': recipe.description,
                'category': recipe.category,
                'image_url': recipe.image_url,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'user_id': recipe.user_id,
                'average_rating': average_rating,
                'user_name': user_name
            }

            return result

        except SQLAlchemyError as e:
            return handle_error(str(e), 500)


    @jwt_required()
    def delete(self, recipe_id):
        try:
            
            recipe = Recipe.query.get_or_404(recipe_id)
            current_user_email = get_jwt_identity()

            current_user = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                return 'User not found', 404

            if recipe.user_id != current_user.id:
                return "Unauthorized to Delete this recipe", 401

            Ingredient.query.filter_by(recipe_id=recipe_id).delete()
            Instruction.query.filter_by(recipe_id=recipe_id).delete()

            db.session.delete(recipe)
            db.session.commit()

            return 'Recipe deleted successfully'

        except SQLAlchemyError as e:
            db.session.rollback()
            return handle_error(str(e), 500)

    @jwt_required()
    def patch(self, recipe_id):
        try:
            data = request.get_json()
            recipe = Recipe.query.get_or_404(recipe_id)
            current_user_email = get_jwt_identity()

            current_user = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                return 'User not found', 404

            if recipe.user_id != current_user.id:
                return 'Unauthorized to update this recipe', 401
            if 'ingredients' in data:
                # Delete existing ingredients and add new ones
                Ingredient.query.filter_by(recipe_id=recipe_id).delete()
                recipe.ingredients = [Ingredient(content=ingredient, recipe=recipe) for ingredient in data['ingredients']]

            if 'instructions' in data:
                # Delete existing instructions and add new ones
                Instruction.query.filter_by(recipe_id=recipe_id).delete()
                recipe.instructions = [Instruction(content=instruction, recipe=recipe) for instruction in data['instructions']]

            # Update additional fields
            if 'title' in data:
                recipe.title = data['title']
            if 'description' in data:
                recipe.description = data['description']
            if 'category' in data:
                recipe.category = data['category']
            if 'image_url' in data:
                recipe.image_url = data['image_url']
            if 'prep_time' in data:
                recipe.prep_time = data['prep_time']
            if 'cook_time' in data:
                recipe.cook_time = data['cook_time']

            db.session.commit()

            # Prepare the response
            response = {
                'id': recipe.id,
                'title': recipe.title,
                'ingredients': [ingredient.content for ingredient in recipe.ingredients],
                'instructions': [instruction.content for instruction in recipe.instructions],
                'description': recipe.description,
                'category': recipe.category,
                'image_url': recipe.image_url,
                'prep_time': recipe.prep_time,
                'cook_time': recipe.cook_time,
                'user_id': recipe.user_id
            }

            return 'Recipe updated successfully'

        except SQLAlchemyError as e:
            db.session.rollback()
            return handle_error(str(e), 500)

class RecipesListResource(Resource):
  
    def get(self):
        try:

            category_filter = request.args.get('category')

            if category_filter:
                recipes = Recipe.query.filter_by(category=category_filter).all()
            else:
                recipes = Recipe.query.all()

            result = []
            
            for recipe in recipes:
                average_rating = recipe.average_rating 
                
                result.append({
                    'id': recipe.id,
                    'title': recipe.title,
                    'ingredients': [ingredient.content for ingredient in recipe.ingredients],
                    'instructions': [instruction.content for instruction in recipe.instructions],
                    'description': recipe.description,
                    'category': recipe.category,
                    'image_url': recipe.image_url,
                    'prep_time': recipe.prep_time,
                    'cook_time': recipe.cook_time,
                    'user_id': recipe.user_id,
                     'average_rating': average_rating
                    
                })
            return jsonify(result)

        except SQLAlchemyError as e:
            return handle_error(str(e), 500)
        
        

    
    # @jwt_required()
    # def post(self):
    #     try:
    #         data = request.get_json()
    #         current_user_email = get_jwt_identity()

    #         current_user = User.query.filter_by(email=current_user_email).first()
    #         if not current_user:
    #             return jsonify({'error': 'User not found'}), 404

    #         required_fields = ['title', 'ingredients', 'description', 'category', 'instructions', 'image_url', 'prep_time', 'cook_time']
    #         if not all(field in data for field in required_fields):
    #             return jsonify({'error': 'Missing data fields'}), 400

    #         new_recipe = Recipe(
    #             title=data['title'],
    #             description=data['description'],
    #             category=data['category'],
    #             image_url=data['image_url'],
    #             prep_time=data['prep_time'],
    #             cook_time=data['cook_time'],
    #             user_id=current_user.id
    #         )

    #         if 'ingredients' in data:
    #             for ingredient_content in data['ingredients']:
    #                 new_ingredient = Ingredient(content=ingredient_content, recipe=new_recipe)
    #                 db.session.add(new_ingredient)

    #         if 'instructions' in data:
    #             for instruction_content in data['instructions']:
    #                 new_instruction = Instruction(content=instruction_content, recipe=new_recipe)
    #                 db.session.add(new_instruction)

    #         db.session.add(new_recipe)
    #         db.session.commit()

    #         return jsonify({
    #             'id': new_recipe.id,
    #             'title': new_recipe.title,
    #             'description': new_recipe.description,
    #             'category': new_recipe.category,
    #             'image_url': new_recipe.image_url,
    #             'prep_time': new_recipe.prep_time,
    #             'cook_time': new_recipe.cook_time,
    #             'user_id': new_recipe.user_id,
    #             'instructions': [instruction.to_dict() for instruction in new_recipe.instructions],
    #             'ingredients': [ingredient.to_dict() for ingredient in new_recipe.ingredients]
    #         }), 201

    #     except SQLAlchemyError as e:
    #         db.session.rollback()
    #         return jsonify({"error": str(e)}), 500
    # Uncommented and slightly modified POST method in RecipesListResource


    @jwt_required()
    def post(self):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                return jsonify({'error': 'User not found'}), 404

            parser = reqparse.RequestParser()
            parser.add_argument('title', type=str, required=True, help='Title is required')
            parser.add_argument('description', type=str, required=True, help='Description is required')
            parser.add_argument('category', type=str, required=True, help='Category is required')
            parser.add_argument('image_url', type=str, required=True, help='Image URL is required')
            parser.add_argument('prep_time', type=str, required=True, help='Prep time is required')
            parser.add_argument('cook_time', type=str, required=True, help='Cook time is required')
            parser.add_argument('ingredients', type=list, required=True, location='json', help='Ingredients are required')
            parser.add_argument('instructions', type=list, required=True, location='json', help='Instructions are required')
            
            args = parser.parse_args()

            # Create a new recipe
            new_recipe = Recipe(
                title=args['title'],
                description=args['description'],
                category=args['category'],
                image_url=args['image_url'],
                prep_time=args['prep_time'],
                cook_time=args['cook_time'],
                user_id=current_user.id
            )

            # Add ingredients to the recipe
            for ingredient in args['ingredients']:
                new_ingredient = Ingredient(content=ingredient, recipe=new_recipe)
                db.session.add(new_ingredient)

            # Add instructions to the recipe
            for instruction in args['instructions']:
                new_instruction = Instruction(content=instruction, recipe=new_recipe)
                db.session.add(new_instruction)

            # Add the new recipe to the database
            db.session.add(new_recipe)
            db.session.commit()

            return {'message': 'Recipe created successfully'}, 201

        except SQLAlchemyError as e:
            db.session.rollback()
            return handle_error(str(e), 500)
    
        
        
class RatingsResource(Resource):
    @jwt_required()
    def post(self):
        try:
            
            data = request.get_json()

            if 'recipe_id' not in data or 'rating' not in data:
                return {"error": "Missing recipe_id or rating value"}, 400

            rating_value = float(data['rating'])
            if not (0 <= rating_value <= 5):
                return {"error": "Invalid rating value. Should be between 0 and 5."}, 400

            recipe_id = data['recipe_id']
            recipe = Recipe.query.get_or_404(recipe_id)

            recipe.total_ratings += rating_value
            recipe.num_ratings += 1

            db.session.commit()

            response = {
                'message': 'Rating submitted successfully',
                'total_rating': recipe.total_ratings
            }

            return (response), 200
        except Exception as e:
            return {"error": str(e)}, 400



   
    


class RatingsResourceID(Resource):
    @jwt_required()
    def patch(self, recipe_id):
        try:
            
            data = request.get_json()

            if 'rating' not in data:
                return {"error": "Missing rating value"}, 400

            rating_value = float(data['rating'])
            if not (0 <= rating_value <= 5):
                return {"error": "Invalid rating value. Should be between 0 and 5."}, 400

            # Assuming you have a previous rating that needs to be updated
            previous_rating_value = float(data.get('previous_rating', 0))

            # Update the total_ratings based on the previous rating
            recipe = Recipe.query.filter_by(id=recipe_id).first()
            if recipe is None:
                return {"error": "Recipe not found"}, 404

            recipe.total_ratings = recipe.total_ratings - previous_rating_value + rating_value
            recipe.num_ratings += 1  # Increment num_ratings

            db.session.commit()

            response = {
                'message': 'Rating updated successfully',
                'total_ratings': recipe.total_ratings
            }

            return  response, 200
        except Exception as e:
            return {"error": str(e)}, 400
        
    @jwt_required()
    def get(self, recipe_id):
        try:
            # Get the current user's identity using the JWT token
            current_user_id = get_jwt_identity()

            # Fetch the recipe by its ID
            recipe = Recipe.query.get(recipe_id)



            # Format the response
            response = {
                'user_id': current_user_id,
                'recipe_id': recipe.id,
                'total_ratings': recipe.total_ratings
                # Add more information as needed
            }

            return response, 200

        except Exception as e:
            return {"error": str(e)}, 400 
        
class RecipeByID(Resource):
    @jwt_required()
    def get(self):
        try:
            current_user_email = get_jwt_identity()
            current_user = User.query.filter_by(email=current_user_email).first()
            if not current_user:
                return jsonify({"error": "User not found"}), 404

            recipes = Recipe.query.filter_by(user_id=current_user.id).all()

            serialized_recipes = []
            for recipe in recipes:
                serialized_recipe = {
                    'id': recipe.id,
                    'title': recipe.title,
                    'description': recipe.description,
                    'image_url': recipe.image_url,
                    'user_id': recipe.user_id
                }
                serialized_recipes.append(serialized_recipe)

            return jsonify(serialized_recipes)

        except SQLAlchemyError as e:
            return handle_error(str(e), 500)

             
    
        
    