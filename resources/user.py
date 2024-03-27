from flask import jsonify
from flask_restful import Resource, reqparse, fields, marshal_with
from flask_bcrypt import generate_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from models import UserModel, db

user_fields = {
    'id': fields.Integer,
    'first_name': fields.String,
    'last_name': fields.String,
    'phone': fields.String,
    'email': fields.String,
    'role': fields.String,
    'created_at': fields.DateTime
}

response_field = {
    "message": fields.String,
    "status": fields.String,
    "user": fields.Nested(user_fields)
}

class Signup(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('first_name', required=True, help="Firstname is required")
    parser.add_argument('last_name', required=True, help="Last name is required")
    parser.add_argument('phone', required=True, help="Phone number is required")
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    @marshal_with(response_field)
    def post(self):
        data = Signup.parser.parse_args()

        # encrypt password
        data['password'] = generate_password_hash(data['password'])
        # set default role
        data['role'] = 'member'

        user = UserModel(**data)

        # verify email and phone uniqueness before saving to the db
        email = UserModel.query.filter_by(email = data['email']).one_or_none()

        if email:
            return {"message": "Email already taken", "status": "fail"}, 400

        phone = UserModel.query.filter_by(phone = data['phone']).one_or_none()

        if phone:
            return {"message": "Phone number already exists", "status": "fail"}, 400

        try:
            # save user to db
            db.session.add(user)
            db.session.commit()
            # get user from db after saving
            db.session.refresh(user)

            user_json = user.to_json()
            access_token = create_access_token(identity=user_json['id'])
            refresh_token = create_refresh_token(identity=user_json['id'])

            return {"message": "Account created successfully",
                    "status": "success",
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "user": user_json }, 201
        except:
            return {"message": "Unable to create account", "status": "fail"}, 400

class Login(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', required=True, help="Email address is required")
    parser.add_argument('password', required=True, help="Password is required")

    def post(self):
        data = Login.parser.parse_args()

        # 1. Get user using email
        user = UserModel.query.filter_by(email = data['email']).first()

        if user:
            # 2. check if provided password is correct
            is_password_correct = user.check_password(data['password'])

            if is_password_correct:
                # 3. Generate token and return user dict
                user_json = user.to_json()
                access_token = create_access_token(identity=user_json['id'])
                refresh_token = create_refresh_token(identity=user_json['id'])
                return {"message": "Login successful",
                        "status": "success",
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "user": user_json,
                        }, 200
            else:
                return {"message": "Invalid email/password", "status": "fail"}, 403
        else:
            return {"message": "Invalid email/password", "status": "fail"}, 403

class RefreshAccess(Resource):
    @jwt_required(refresh=True)
    def post(self):
        identity = get_jwt_identity()

        access_token = create_access_token(identity=identity)

        return jsonify(access_token = access_token)