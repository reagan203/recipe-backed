from flask_restful import Api
from flask_cors import CORS
from flask_mail import Mail
from flask import Flask
from flask_migrate import Migrate
from models import db   # Import db instance from models module

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize db with Flask app instance

migrate = Migrate(app, db)  # Initialize Flask-Migrate with Flask app and db instance

# Add other configurations and extensions here


mail = Mail(app)

api=Api(app)
CORS(app)



if __name__ == "__main__":
    app.run(debug=True)
