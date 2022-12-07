from flask_restx import Namespace, Resource

orders_namespace = Namespace('orders', description='Orders related operations')


@orders_namespace.route('/')
class Orders(Resource):
    def get(self):
        return {'message': 'orders'}
