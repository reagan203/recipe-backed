# from flask_restful import Resource, reqparse, fields, marshal_with
# from flask_jwt_extended import jwt_required, get_jwt_identity
# from models import CommentModel, db

# comment_fields = {
#     'comment_id': fields.Integer,
#     'recipe_id': fields.Integer,
#     'content': fields.String,
#     'created_at': fields.DateTime
# }

# class Comment(Resource):
#     @marshal_with(comment_fields)
#     def get(self, comment_id=None):
#         if comment_id:
#             comment = CommentModel.query.get(comment_id)
#             if comment:
#                 return comment
#             else:
#                 return {"message": "comment not found"}, 404
#         else:
#             comments = CommentModel.query.all()
#             return comments

# class CreateComment(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('recipe_id', type=int, required=True, help="Recipe ID is required")
#     parser.add_argument('content', required=True, help="Content is required")

#     @jwt_required()
#     @marshal_with(comment_fields)
#     def post(self):
#         data = CreateComment.parser.parse_args()
#         author_id = get_jwt_identity()

#         comment = CommentModel(user_id=author_id, **data)

#         try:
#             db.session.add(comment)
#             db.session.commit()
#             return comment, 201
#         except:
#             db.session.rollback()
#             return {"message": "Unable to create comment"}, 400

# class UpdateComment(Resource):
#     parser = reqparse.RequestParser()
#     parser.add_argument('content')

#     @jwt_required()
#     @marshal_with(comment_fields)
#     def put(self, comment_id):
#         data = UpdateComment.parser.parse_args()
#         author_id = get_jwt_identity()

#         comment = CommentModel.query.filter_by(comment_id=comment_id, user_id=author_id).first()

#         if not comment:
#             return {"message": "Comment not found or you are not authorized to update"}, 404

#         for key, value in data.items():
#             if value is not None:
#                 setattr(comment, key, value)

#         try:
#             db.session.commit()
#             return comment
#         except:
#             db.session.rollback()
#             return {"message": "Unable to update comment"}, 400

#     @jwt_required()
#     def delete(self, comment_id):
#         author_id = get_jwt_identity()

#         comment = CommentModel.query.filter_by(comment_id=comment_id, user_id=author_id).first()

#         if not comment:
#             return {"message": "Comment not found or you are not authorized to delete"}, 404

#         try:
#             db.session.delete(comment)
#             db.session.commit()
#             return {"message": "Comment deleted successfully"}
#         except:
#             db.session.rollback()
#             return {"message": "Unable to delete comment"}, 400
