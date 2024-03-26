from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource,Api
from flask_cors import CORS
from flask_mail import Mail
from models import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

migrations=Migrate(app,db)
mail = Mail(app)


api=Api(app)
CORS(app)




