from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
import datetime
import sqlalchemy
from sqlalchemy import orm
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from data.db_session import SqlAlchemyBase
from sqlalchemy_serializer import SerializerMixin
from data import db_session
from data.categories import Categories
from data.products import Product

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('products', required=True)


def abort_if_news_not_found(categories_id):
    session = db_session.create_session()
    categories = session.query(Categories).get(categories_id)
    if not categories:
        abort(404, message=f"Categories {categories_id} not found")
    elif session.query(Categories).filter(Categories.name == categories.name).first():
        abort(404, message=f"Categories {categories_id} act")
    prod_list = Categories.products.split(', ')
    for prod in prod_list:
        product = session.query(Product).get(int(prod))
        if not product:
            abort(404, message=f"Product {int(prod)} not found")
        product = None


class CategoriesResource(Resource):
    def get(self, categories_id):
        abort_if_news_not_found(categories_id)
        session = db_session.create_session()
        categories = session.query(Categories).get(categories_id)
        return jsonify({'Categories': categories.to_dict(
            only=('id', 'name', 'products'))})

    def delete(self, categories_id):
        abort_if_news_not_found(categories_id)
        session = db_session.create_session()
        categories = session.query(Categories).get(categories_id)
        session.delete(categories)
        session.commit()
        return jsonify({'success': 'OK'})


class CategoriesListResource(Resource):
    def get(self):
        session = db_session.create_session()
        categories = session.query(Categories).all()
        return jsonify({'categories': [item.to_dict(
            only=('id', 'name', 'products')) for item in categories]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        categories = Categories(
            surname=args['name'],
            name=args['products']
        )
        session.add(categories)
        session.commit()
        return jsonify({'success': 'OK'})
