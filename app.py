from flask import Flask, make_response,jsonify, request, abort
from flask_migrate import Migrate
from sqlalchemy.exc import IntegrityError
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db, Recipe, Favourite, Meal_plan, User, Comment,Instruction,Ingredient
from users_resource import Users,UserLoginResource,UsersID
from flask_jwt_extended import jwt_required, get_jwt_identity
from comments import CommentsResource, CommentByIDResource,  CommentsResourceID
from recipe import RecipesResource, RecipesListResource, RatingsResource,RatingsResourceID, RecipeByID
from sqlalchemy.exc import SQLAlchemyError
from payment import callback_url, lipa_na_mpesa
import requests
import base64
import datetime
import json
import os 

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
app.config['JWT_TOKEN_LOCATION'] = ['headers', 'cookies'] 
app.config['JWT_COOKIE_CSRF_PROTECT'] = False  # Disable CSRF protection for cookies
app.config['JWT_COOKIE_SECURE'] = False  # Set to True in a production environment with HTTPS
app.config['JWT_REFRESH_COOKIE_PATH'] = '/refresh'  
app.config['JWT_REFRESH_COOKIE_SECURE'] = False  # Set to True in a production environment with HTTPS
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = False  # Use False to make refresh tokens never expire
app.json.compact = False

api = Api(app)
jwt = JWTManager(app)
CORS(app)
migrate = Migrate(app, db)
db.init_app(app)

api.add_resource(Users,'/users')
api.add_resource(UsersID,'/users')
api.add_resource(UserLoginResource, '/login')
api.add_resource(CommentsResource, '/comments')
api.add_resource(CommentByIDResource, '/comments/<int:id>')
api.add_resource(RecipesResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipesListResource, '/recipes')
api.add_resource(RatingsResource, '/ratings')
api.add_resource(RatingsResourceID, '/ratings/<int:recipe_id>')
api.add_resource( CommentsResourceID, '/comments/<int:recipe_id>')
api.add_resource( RecipeByID, '/recipe')

@app.route('/callback_url', methods=['POST'])
def callback_route():
    return 



def login_required(route_function):
    def wrapper(*args, **kwargs):
        try:
            # Extract user information from JWT token
            current_user = get_jwt_identity()
            if current_user:
                return route_function(*args, **kwargs)
            else:
                return jsonify({'error': 'Authentication required'}), 401
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return wrapper


@app.route('/meal_plan/<int:meal_plan_id>', methods=['GET'])
def get_meal_plan(meal_plan_id):
    meal_plan = Meal_plan.query.get(meal_plan_id)

    if meal_plan is None:
        return jsonify({"message": "Meal plan not found"}), 404

    return jsonify( {
        'id': meal_plan.id,
        'user_id': meal_plan.user_id,
        'title': meal_plan.title,
        'price': meal_plan.price,
        'description': meal_plan.description
    }),200

@app.route('/meal_plan/all', methods=['GET'])
def get_all_meal_plans():
    all_meal_plans = Meal_plan.query.all()

    return jsonify([
        {
            'id': meal_plan.id,
            'user_id': meal_plan.user_id,
            'title': meal_plan.title,
            'price': meal_plan.price,
            'description': meal_plan.description
        } for meal_plan in all_meal_plans
    ])

@app.route('/meal_plans', methods=['GET'])
@jwt_required()
def get_meal_plans():
    current_user_email = get_jwt_identity()
    user = User.query.filter_by(email=current_user_email).first()

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    meal_plans = Meal_plan.query.filter_by(user_id=user.id).all()
    
    serialized_meal_plans = [{
        'id': meal_plan.id,
        'title': meal_plan.title,
        'price': meal_plan.price,
        'description': meal_plan.description,
        'user_id': meal_plan.user_id
    } for meal_plan in meal_plans]

    return jsonify(serialized_meal_plans)

@app.route('/meal_plan', methods=['POST'])
@jwt_required()
def create_meal_plan():
    current_user_email = get_jwt_identity()

    # Assuming you have a User model
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user is None:
        return jsonify({'error': 'User not found'}), 404

    print("Current User ID:", current_user.id)  # Add this line for debugging

    data = request.json

    if not data or 'title' not in data or 'price' not in data or 'description' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400

    if 'price' not in data or not isinstance(data['price'], (int, float)):
        return jsonify({'error': 'Price must be provided as a number'}), 400
    
    if not data['price']:
        return jsonify({'error': 'Price cannot be empty'}), 400

    new_meal_plan = Meal_plan(
        user_id=current_user.id,
        title=data['title'],
        price=data['price'],
        description=data['description']
    )

    db.session.add(new_meal_plan)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

    return jsonify({
        'id': new_meal_plan.id,
        'user_id': new_meal_plan.user_id,
        'title': new_meal_plan.title,
        'price': new_meal_plan.price,
        'description': new_meal_plan.description
    }), 201


@app.route('/meal_plan/<int:meal_plan_id>', methods=['PATCH'])
@jwt_required()
def update_meal_plan(meal_plan_id):
    current_user_email = get_jwt_identity()
    
    # Assuming you have a User model
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user is None:
        return jsonify({'error': 'User not found'}), 404

    meal_plan = Meal_plan.query.get_or_404(meal_plan_id)

    if meal_plan.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized to update this meal plan'}), 403

    data = request.json

    if 'price' in data:
        if not isinstance(data['price'], (int, float)):
            return jsonify({'error': 'Price must be provided as a number'}), 400
        if not data['price']:
            return jsonify({'error': 'Price cannot be empty'}), 400

    meal_plan.title = data.get('title', meal_plan.title)
    meal_plan.price = data.get('price', meal_plan.price)
    meal_plan.description = data.get('description', meal_plan.description)

    db.session.commit()

    return jsonify({
        'id': meal_plan.id,
        'user_id': meal_plan.user_id,
        'title': meal_plan.title,
        'price': meal_plan.price,
        'description': meal_plan.description
    }), 200

@app.route('/meal_plan/<int:meal_plan_id>', methods=['DELETE'])
@jwt_required()
def delete_meal_plan(meal_plan_id):
    current_user_email = get_jwt_identity()

    # Assuming you have a User model
    current_user = User.query.filter_by(email=current_user_email).first()
    if current_user is None:
        return jsonify({'error': 'User not found'}), 404

    meal_plan = Meal_plan.query.get(meal_plan_id)
    if not meal_plan or meal_plan.user_id != current_user.id:
        return make_response(jsonify({"error": "Meal plan not found or unauthorized"}), 404)

    db.session.delete(meal_plan)
    db.session.commit()

    return make_response(jsonify({"message": "Meal plan deleted successfully"}), 204)

#favourites

@app.route("/favorites", methods=["GET"])
@jwt_required()
def get():
    try:
        current_user_email = get_jwt_identity()
        current_user = User.query.filter_by(email=current_user_email).first()
        if not current_user:
            return jsonify({"error": "User not found"}), 404

        favorites = Favourite.query.filter_by(user_id=current_user.id).all()
        serialized_favorites = []
        for favourite in favorites:
            recipe = Recipe.query.get(favourite.recipe_id)
            if recipe:
                serialized_favorites.append({
                    "favourite_id": favourite.id,
                    "recipe_id": recipe.id,
                    "title": recipe.title,
                    "image": recipe.image_url,
                    "user_id": favourite.user_id
                })
        return jsonify(serialized_favorites), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/favorites/<int:favorite_id>', methods=['DELETE'])
@jwt_required()
def delete_favorite(favorite_id):
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    existing_favorite = Favourite.query.filter_by(id=favorite_id, user_id=current_user.id).first()
    if not existing_favorite:
        return jsonify({"error": "Favorite not found"}), 404

    try:
        db.session.delete(existing_favorite)
        db.session.commit()
        return jsonify({"message": "Favorite deleted successfully"}), 204
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@app.route('/favorites', methods=['POST'])
@jwt_required()
def add_favorite():
    current_user_email = get_jwt_identity()
    current_user = User.query.filter_by(email=current_user_email).first()
    if not current_user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    recipe_id = data.get('recipe_id')

    recipe = Recipe.query.get(recipe_id)
    if not recipe:
        return jsonify({"error": "Recipe not found"}), 404

    existing_favorite = Favourite.query.filter_by(user_id=current_user.id, recipe_id=recipe_id).first()
    if existing_favorite:
        return jsonify({"error": "Recipe already in favorites"}), 400

    new_favorite = Favourite(user_id=current_user.id, recipe_id=recipe_id)
    db.session.add(new_favorite)
    db.session.commit()

    response_data = {
        "id": new_favorite.id,
        "user_id": new_favorite.user_id,
        "recipe_id": new_favorite.recipe_id
    }
    return jsonify(response_data), 201


# Replace these values with your actual Safaricom Daraja API credentials
CONSUMER_KEY = "MfvOvpKRZJL3dbRFDUyq7pSLRzOU5bD3HAwbKmjGhEGKXCBj"
CONSUMER_SECRET = "AqX64RHWaPeBHMICIwFgRrrjyokEJgHF0nT3GIAsBPZTwcl7v2KrwF6zaJZGxnzT"
LIPA_NA_MPESA_PASSKEY = "bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919"
SHORTCODE = "174379"
LIPA_NA_MPESA_ONLINE_ENDPOINT = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

@app.route('/callback_url', methods=['POST'])
def callback_url():
    data = request.json

    # Process the callback data
    transaction_status = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
    print(data)
    if transaction_status == 0:
        print("Payment successful")
    else:
        # Payment failed
        # Handle the failure scenario
        print("Payment failed")

    return jsonify({"ResultCode": 0, "ResultDesc": "Success"})  # Respond to Safaricom with a success message

@app.route('/lipa_na_mpesa', methods=['POST'])
def lipa_na_mpesa():
    try:
        token = generate_token()
        if token is None:
            return jsonify({"error": "Failed to generate token"}), 500
        phone_number = request.json.get('phone_number')
        amount = request.json.get('amount')
        
        if not phone_number or not amount:
            return jsonify({"error": "Phone number and amount are required"}), 400

        timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        password = base64.b64encode((SHORTCODE + LIPA_NA_MPESA_PASSKEY + timestamp).encode()).decode('utf-8')

        payload = {
            "BusinessShortCode": SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://2488-197-232-152-187.ngrok-free.app/lipa_na_mpesa",
            "AccountReference": "Test123",
            "TransactionDesc": "Payment for testing"
        }

        headers = {
            "Authorization": "Bearer " + generate_token(),
            "Content-Type": "application/json"
        }

        response = requests.post(LIPA_NA_MPESA_ONLINE_ENDPOINT, json=payload, headers=headers)

        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

def generate_token():
    token_endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    credentials = base64.b64encode((CONSUMER_KEY + ':' + CONSUMER_SECRET).encode()).decode('utf-8')
    headers = {
        'Authorization': 'Basic ' + credentials
    }

    try:
        response = requests.get(token_endpoint, headers=headers)
        response.raise_for_status()  
        return response.json().get('access_token')
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Failed to generate token: {e}") from e





if __name__ == '_main_':
    app.run(port=5555, debug=True, use_reloader=True)