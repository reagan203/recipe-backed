from flask_restful import Resource, reqparse, fields, marshal_with
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import RatingModel, db

rating_fields = {
    'rating_id': fields.Integer,
    'recipe_id': fields.Integer,
    'rating': fields.Integer,
    'created_at': fields.DateTime
}

class Rating(Resource):
    @marshal_with(rating_fields)
    def get(self, rating_id=None):
        if rating_id:
            rating = RatingModel.query.get(rating_id)
            if rating:
                return rating
            else:
                return {"message": "Recipe not found"}, 404
        else:
            ratings = RatingModel.query.all()
            return ratings
    

class CreateRating(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('recipe_id', type=int, required=True, help="Recipe ID is required")
    parser.add_argument('rating', type=int, required=True, help="Rating is required")

    @jwt_required()
    @marshal_with(rating_fields)
    def post(self):
        data = CreateRating.parser.parse_args()

        rating = RatingModel(**data)

        try:
            db.session.add(rating)
            db.session.commit()
            return rating, 201
        except:
            db.session.rollback()
            return {"message": "Unable to create rating"}, 400

class UpdateRating(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('rating', type=int, required=True, help="Rating is required")

    @jwt_required()
    @marshal_with(rating_fields)
    def put(self, rating_id):
        data = UpdateRating.parser.parse_args()

        rating = RatingModel.query.get(rating_id)

        if not rating:
            return {"message": "Rating not found"}, 404

        rating.rating = data['rating']

        try:
            db.session.commit()
            return rating
        except:
            db.session.rollback()
            return {"message": "Unable to update rating"}, 400

    @jwt_required()
    def delete(self, rating_id):
        rating = RatingModel.query.get(rating_id)

        if not rating:
            return {"message": "Rating not found"}, 404

        try:
            db.session.delete(rating)
            db.session.commit()
            return {"message": "Rating deleted successfully"}
        except:
            db.session.rollback()
            return {"message": "Unable to delete rating"}, 400
