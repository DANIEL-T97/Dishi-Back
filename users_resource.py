from flask import Flask,jsonify,request,make_response
from flask_restful import Resource,reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from flask_bcrypt import Bcrypt
from models import User,db

bcrypt = Bcrypt()
class Users(Resource):
    # @jwt_required()
    #def get(self):
        #users = User.query.all()
        #return make_response(jsonify([user.to_dict() for user in users]),200)
    

    # @jwt_required()
    def post(self):
        try:
            data = request.get_json()
            name=data.get('name')
            email=data.get('email')
            phone_number=data.get('phone_number')
            
            password=data.get('password')
            
            # Check if email is valid
            if not email or '@' not in email or '.' not in email:
                return {"error": "Invalid email address."}, 400

            # Check if password is strong enough (you can adjust the criteria)
            if not (8 <= len(password) <= 50):
                return {"error": "Password must be between 8 and 50 characters."}, 400
            #Check whether a user exists
            existing_user = User.query.filter_by(email=email).first()
            if existing_user:
                return {"error":"User with that email address already exists"}, 403
            # Check if phone number is exactly 10 digits
            if not (phone_number and len(phone_number) == 10 and phone_number.isdigit()):
                return {"error": "Phone number must be exactly 10 digits."}, 400
            # Initialize empty lists for Recipe, Comment, Favorite, MealPlan
            recipes = []
            comments = []
            favourites = []
            meal_plans = []

            hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")
            new_user = User(
                name=name,
                email=email,
                phone_number=phone_number,
                password=hashed_password,
                recipes=recipes,
                comments=comments,
                favourites=favourites,
                meal_plans=meal_plans,
            )
            db.session.add(new_user)
            db.session.commit()
            
            response_dict = {"message":"User Added  sucessfully"}
            response = make_response(
                jsonify(response_dict),200
            )
            return response
    

        except Exception as e:
            print(f"Login failed with exception: {str(e)}")
            return {"error": "An unexpected error occurred during login."}, 500
    pass



class UsersID(Resource):
    @jwt_required()
    def get(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        user_dict = {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'phone_number': user.phone_number
        }

        return make_response(jsonify(user_dict), 200)


    
    @jwt_required()
    def patch(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        data = request.get_json()

        for attr in data:
            setattr(user, attr, data[attr])

        db.session.commit()

        response = make_response(jsonify({"message": "User updated successfully!"}), 201)
        return response


    @jwt_required()
    def delete(self):
        current_user_email = get_jwt_identity()
        user = User.query.filter_by(email=current_user_email).first()

        if not user:
            return make_response(jsonify({"error": "User not found"}), 404)

        db.session.delete(user)
        db.session.commit()

        response = make_response(jsonify({"message": "User deleted successfully!"}), 200)
        return response


class UserLoginResource(Resource):
   def post(self):
        try:
            data = request.get_json()
            email = data.get('email')
            password = data.get('password')

            user = User.query.filter_by(email=email).first()
            if user and bcrypt.check_password_hash(user.password, password):
                access_token = create_access_token(identity=email)
                refresh_token = create_refresh_token(identity=email)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            else:
                return {"error": "Invalid username or password."}, 401
        except Exception as e:
            return {"error": str(e)}, 500

class RefreshTokenResource(Resource):
    # @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}, 200
    
    
