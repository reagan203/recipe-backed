from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import check_password_hash

db = SQLAlchemy()

class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String, nullable=False)
    last_name = db.Column(db.String, nullable=False)
    phone = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    role = db.Column(db.String, nullable=False)
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
    description = db.Column(db.String ,nullable=False)
    instructions = db.Column(db.String ,nullable=False)
    prep_time = db.Column(db.Integer ,nullable=False)
    cook_time = db.Column(db.Integer ,nullable=False)
    servings = db.Column(db.String, nullable=False)
    image_url = db.Column(db.String(255),nullable=False)  # Column for image URL or file path
    
    