from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from .db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from data import db_session
from data.products import Product

parser = reqparse.RequestParser()

parser.add_argument('name', required=True)
parser.add_argument('info', required=True)
parser.add_argument('coin', required=True)


def abort_if_news_not_found(product_id):
    session = db_session.create_session()
    product = session.query(Product).get(product_id)
    if not product:
        abort(404, message=f"Product {product_id} not found")
    elif session.query(Product).filter(Product.name == product.name).first():
        abort(404, message=f"Product {product_id} act")


class ProductsResource(Resource):
    def get(self, product_id):
        abort_if_news_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        return jsonify({'product': product.to_dict(
            only=('id', 'surname', 'name', 'age', 'email'))})

    def delete(self, product_id):
        abort_if_news_not_found(product_id)
        session = db_session.create_session()
        product = session.query(Product).get(product_id)
        session.delete(product)
        session.commit()
        return jsonify({'success': 'OK'})


class ProductsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        product = session.query(Product).all()
        return jsonify({'products': [item.to_dict(
            only=('id', 'name', 'info', 'coin')) for item in product]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        trainer = Product(
            surname=args['name'],
            name=args['info'],
            age=args['coin']
        )
        session.add(trainer)
        session.commit()
        return jsonify({'success': 'OK'})
