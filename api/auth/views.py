from flask_restx import Namespace, Resource, fields
from models.user import User
# from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from datetime import timedelta
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, JWTManager

auth_namespace = Namespace('auth', description='authentication process')
signup_namespace = auth_namespace.model('User', {
    'id': fields.Integer(readOnly=True, description='The user identifier'),
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password'),
    'email': fields.String(required=True, description='email')
})

login_namespace = auth_namespace.model('Login', {
    'username': fields.String(required=True, description='username'),
    'password': fields.String(required=True, description='password')
})

# jwtmanager for login
jwt = JWTManager()


@auth_namespace.route("/login")
class LoginAuth(Resource):
    @auth_namespace.expect(login_namespace)
    # @auth_namespace.marshal_with(login_namespace)
    def post(self):
        """
            login jwt for user
        """
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
        JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
        user = User.query.filter_by(username=username).first()
        if user is not None:
            access_token = create_access_token(identity=username)
            refresh_token = create_refresh_token(identity=username)
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }, 200


@auth_namespace.route("/signup")
class SignUpAuth(Resource):
    @auth_namespace.expect(signup_namespace)
    @auth_namespace.marshal_with(signup_namespace)
    def post(self):
        """
            signup auth for user
        """

        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        new_user = User(username=username, password=password, email=email)
        new_user.save()

        return new_user, 201, {'message': 'user created successfully'}


@auth_namespace.route("/refresh")
class RefreshAuth(Resource):
    @jwt_required(refresh=True)
    def post(self):
        """
            refresh jwt for user
        """
        username = get_jwt_identity()
        access_token = create_access_token(identity=username)
        return {'access_token': access_token}, 200


@auth_namespace.route('/me')
class MeAuth(Resource):
    @jwt_required()
    def get(self):
        """
            get user data
        """
        username = get_jwt_identity()
        email = User.query.filter_by(username=username).first().email
        return {'username': username, 'email': email}, 200
