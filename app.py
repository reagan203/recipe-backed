from flask import Flask
from flask_migrate import Migrate
from flask_restful import Resource,Api
from models import db

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'

migrations=Migrate(app,db)

api=Api(app)




