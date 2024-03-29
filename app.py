from flask_restful import  Api,Resource
from flask_cors import CORS
from flask import Flask
from flask_migrate import Migrate
from models import db  ,UserModel
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from resources.user import Signup, Login, RefreshAccess,AllUsers
from resources.recipe import CreateRecipe, UpdateRecipe,Recipe
# from resources.comment import CreateComment, UpdateComment,Comment
# from resources.rating import CreateRating, UpdateRating,Rating


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] =( 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = ("JWT_SECRET_KEY")  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)



# Initialize database with Flask app instance
db.init_app(app)

# Initialize Flask-Migrate with Flask app and db instance
migrate = Migrate(app, db)

# Initialize Flask-Restful API
api = Api(app)

# Enable Cross-Origin Resource Sharing (CORS)
CORS(app)


# initialize bcrypt
bcrypt = Bcrypt(app)
# initialize JWT
jwt = JWTManager(app)
# Add resources

# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return UserModel.query.filter_by(id=identity).one_or_none().to_json()# an error might occure

class AppResource(Resource):
    def get(self):
        return "Welcome to the recipe  api"


api.add_resource(AppResource, '/')
api.add_resource(Signup, '/signup')
api.add_resource(Login, '/login')
api.add_resource(RefreshAccess, '/refresh-access')
api.add_resource(Recipe, '/recipe','/recipe/<int:recipe_id>')
api.add_resource(CreateRecipe, '/createrecipe')  
api.add_resource(UpdateRecipe, '/updaterecipe','/updaterecipe/<int:recipe_id>')
# api.add_resource(Comment, '/comment')
# api.add_resource(CreateComment, '/createcomment')
# api.add_resource(UpdateComment, '/updatecomment','/updatecomment/<int:comment_id>')
# api.add_resource(Rating, '/rating','/rating/<int:rating_id>')
# api.add_resource(CreateRating, '/createrating')
# api.add_resource(UpdateRating, '/updaterating','/updaterating/<int:rating_id>')
api.add_resource(AllUsers, '/users' ,'/users/<int:user_id>')



# Run the application if executed directly
if __name__ == '__main__':
    app.run(debug=True, port=5000)
