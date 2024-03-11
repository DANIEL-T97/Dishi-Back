from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
#from flask_bcrypt import Bcrypt


db = SQLAlchemy() 
#bcrypt = Bcrypt()

class User(db.Model,SerializerMixin):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    
    
class Recipe(db.Model):

    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(100), nullable=False)
    image_url = db.Column(db.String(500), nullable=False)
    prep_time = db.Column(db.String(60), nullable=False)
    cook_time = db.Column(db.String(60), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )

    # Rating logic directly in the Recipe table
    total_ratings = db.Column(db.Float, default=0.0)
    num_ratings = db.Column(db.Integer, default=0)
    
    user =db.relationship('User', backref = 'recipes')

    @property
    def average_rating(self):
        return (self.total_ratings + self.num_ratings) / 5
    
class Ingredient(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship('Recipe', backref='ingredients')

    def to_dict(self):
        return {
            'content': self.content,
            # Add other attributes as needed
        }

class Instruction(db.Model):
    __tablename__ = "instructions"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.id'), nullable=False)
    recipe = db.relationship('Recipe', backref ='instructions')

    def to_dict(self):
        return {
            'content': self.content,
            # Add other attributes as needed
        }
   
    
class Meal_plan(db.Model):

    __tablename__ = "meal_plans"
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Integer, nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )
    
#relationship with users (one to many)
    user =db.relationship('User', backref = 'meal_plans')

class Comment(db.Model):

    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id") )
    
    #relationship with users (one to many)
    user =db.relationship('User', backref = 'comments')
    recipe =db.relationship('Recipe', backref = 'comments')
    
class Favourite(db.Model):

    __tablename__ = "favourites"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id") )
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id") )
    
    #relationship with users (one to many)
    user =db.relationship('User', backref = 'favourites')
    recipe =db.relationship('Recipe', backref = 'favourites')
    
    


