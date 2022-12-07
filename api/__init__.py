from flask import Flask
from flask_restx import Api
from models.user import db
from .orders.views import orders_namespace
from .auth.views import auth_namespace
from flask_jwt_extended import JWTManager


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ndjej90128937843u7jfdhjfsdkjhe'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()
    api = Api(app)
    jwt = JWTManager(app)

    api.add_namespace(orders_namespace, path='/orders')
    api.add_namespace(auth_namespace, path='/auth')

    return app
