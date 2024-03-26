from flask_sqlalchemy import SQLAlchemy
from enum import Enum

db=SQLAlchemy()



class Gender(Enum):
    male = 'male'
    female = 'female'
    other = 'other'

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    gender = db.Column(db.Enum(Gender), default=Gender.other)
    created_at=db.Column(db.TIMESTAMP(),default=db.func.now())
    

class Recipe(db.Model):
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    created_at=db.Column(db.TIMESTAMP(),default=db.func.now())
    author = db.relationship('User', backref=db.backref('recipes', lazy=True))

class Category(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class RecipeCategory(db.Model):
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), primary_key=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.category_id'), primary_key=True)

class Comment(db.Model):
    comment_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at=db.Column(db.TIMESTAMP(),default=db.func.now())

class Rating(db.Model):
    rating_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipe.recipe_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at=db.Column(db.TIMESTAMP(),default=db.func.now())
    