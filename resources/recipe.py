from flask_restful import Resource, reqparse, fields, marshal_with
from models import RecipeModel, db

recipe_fields = {
    'recipe_id': fields.Integer,
    'title': fields.String,
    'description': fields.String,
    'instructions': fields.String,
    'prep_time': fields.Integer,
    'cook_time': fields.Integer,
    'servings': fields.String,
    'image_url': fields.String
}

class Recipe(Resource):
    @marshal_with(recipe_fields)
    def get(self, recipe_id=None):
        if recipe_id:
            recipe = RecipeModel.query.get(recipe_id)
            if recipe:
                return recipe
            else:
                return {"message": "Recipe not found"}, 404
        else:
            recipes = RecipeModel.query.all()
            return recipes

class CreateRecipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str, required=True, help="Title is required")
    parser.add_argument('description', type=str, required=True, help="Description is required")
    parser.add_argument('instructions', type=str, required=True, help="Instructions are required")
    parser.add_argument('prep_time', type=int, required=True, help="Prep time is required")
    parser.add_argument('cook_time', type=int, required=True, help="Cook time is required")
    parser.add_argument('servings', type=str, required=True, help="Servings are required")
    parser.add_argument('image_url', type=str, required=True, help="Image URL is required")

    @marshal_with(recipe_fields)
    def post(self):
        data = CreateRecipe.parser.parse_args()

        recipe = RecipeModel(**data)

        try:
            db.session.add(recipe)
            db.session.commit()
            return recipe, 201
        except:
            db.session.rollback()
            return {"message": "Unable to create recipe"}, 400
    
class UpdateRecipe(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('title', type=str)
    parser.add_argument('description', type=str)
    parser.add_argument('instructions', type=str)
    parser.add_argument('prep_time', type=int)
    parser.add_argument('cook_time', type=int)
    parser.add_argument('servings', type=str)
    parser.add_argument('image_url', type=str)

    @marshal_with(recipe_fields)
    def put(self, recipe_id):
        data = UpdateRecipe.parser.parse_args()

        recipe = RecipeModel.query.get(recipe_id)

        if not recipe:
            return {"message": "Recipe not found"}, 404

        for key, value in data.items():
            if value is not None:
                setattr(recipe, key, value)

        try:
            db.session.commit()
            return recipe
        except:
            db.session.rollback()
            return {"message": "Unable to update recipe"}, 400

    def delete(self, recipe_id):
        recipe = RecipeModel.query.get(recipe_id)

        if not recipe:
            return {"message": "Recipe not found"}, 404

        try:
            db.session.delete(recipe)
            db.session.commit()
            return {"message": "Recipe deleted successfully"}
        except:
            db.session.rollback()
            return {"message": "Unable to delete recipe"}, 400
