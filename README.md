# recipe-backed
a backed for the recipe website
we create the vertual environment in order to be able to use python code   
  python3 venv .venv
we enter the virtual environment and then carry out the relevant installments
  source .venv/bin/activate
¬¬`¬¬                             ```` INSTALLMENTS¬¬¬
pip install flask
pip install flask_sqlalchemy
pip install flask_restfull
pip install flask_bycrpt
pip install flask_jwt_extended
pip install flask_migrate
pip install flask_cors
pip install flask_mail

we start by creating the tables to show the relationship between the user,recipes,comments and ratings all of this is done in the models.py file here are the tables 
 for the specific user table we us flask _bycrypt to ensure the passwords are hashed to ensure the safety of the users info in the website 


    from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.Text, nullable=False)
    password = db.Column(db.String, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    
    def check_password(self, plain_password):
        return check_password_hash(self.password, plain_password)

    def to_json(self):
        return {"id": self.id, "role": self.role}

class RecipeModel(db.Model):
    __tablename__ ='recipes'
    
    recipe_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    instructions = db.Column(db.Text)
    prep_time = db.Column(db.Integer)
    cook_time = db.Column(db.Integer)
    total_time = db.Column(db.Integer)
    servings = db.Column(db.Integer)
    image_url = db.Column(db.String(255))  # Column for image URL or file path
    author_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())
    author = db.relationship('UserModel', backref=db.backref('recipes', lazy=True))



class CommentModel(db.Model):
    __tablename__ = 'comments'
    
    comment_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

class RatingModel(db.Model):
    __tablename__ = 'ratings'
    
    rating_id = db.Column(db.Integer, primary_key=True)
    recipe_id = db.Column(db.Integer, db.ForeignKey('recipes.recipe_id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.TIMESTAMP, server_default=db.func.now())

after this we create the .gitignore file where we will house all our unused files eg .venv,.vscode
the .vscode is the file am using to set up my personal vscode so that it can best fit my needs 
touch .gitignore



secondly we go to the app.py and create a new  instance of the app
app = Flask(__name__)
we initializre the database 
db.init_app(app)
Initialize Flask-Migrate with Flask app and db instance
migrate = Migrate(app, db)

Initialize Flask-Restful API
api = Api(app)
 Enable Cross-Origin Resource Sharing (CORS)
CORS(app)


initialize bcrypt
bcrypt = Bcrypt(app)
initialize JWT
jwt = JWTManager(app)

after this we do the configuration for the development stage oof the app buildingthis will be changed during the deployment stage 
app.config['SQLALCHEMY_DATABASE_URI'] =( 'sqlite:///data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
 Setup the Flask-JWT-Extended extension
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")  # Change this!
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=15)

ater this we set up the database with some few steps in the terminal 
                    steps
flask db init
flask db revision --autogenerate -m "message"
flask db upgradeor you can use flask db upgrade head


after configing that the tables are good in the database we now create the resources folder which is going to hold the logic of each model created in the models.py
touch user.py ----which haldles the signup and login logic
touch recipe.py ----which handles all the CRUD processes in the recipe model
touch  ratings.py ---- which handles all the CRUD processes in the rating model
touch comment.py ---- which handles all the CRUD processes in the comment model

after alll of this you test the routes in the 
postman appp or the thunderclient 
if all routes are good we carry out this command in order to create the requirments.txt file
pip freeze > requirments.txt

