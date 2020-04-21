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
from data.catalog import Catalog
from data.categories import Categories

parser = reqparse.RequestParser()
parser.add_argument('name', required=True)
parser.add_argument('categorss', required=True)


def abort_if_news_not_found(catalog_id):
    session = db_session.create_session()
    catalog = session.query(Catalog).get(catalog_id)
    if not catalog:
        abort(404, message=f"Catalog {catalog_id} not found")
    elif session.query(Catalog).filter(Catalog.name == catalog.name).first():
        abort(404, message=f"Catalog {catalog_id} act")


class CatalogsResource(Resource):
    def get(self, catalog_id):
        abort_if_news_not_found(catalog_id)
        session = db_session.create_session()
        catalog = session.query(Catalog).get(catalog_id)
        return jsonify({'catalog': catalog.to_dict(
            only=('id', 'surname', 'name', 'age', 'email'))})

    def delete(self, catalog_id):
        abort_if_news_not_found(catalog_id)
        session = db_session.create_session()
        catalog = session.query(Catalog).get(catalog_id)
        session.delete(catalog)
        session.commit()
        return jsonify({'success': 'OK'})

    def put(self, catalog_id):
        abort_if_news_not_found(catalog_id)
        args = parser.parse_args()
        session = db_session.create_session()
        catalog = session.query(Catalog).get(catalog_id)
        catalog.name = args['name']
        catalog.categorss = args['categorss']
        session.commit()
        return jsonify({'success': 'OK'})


class CatalogsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        catalog = session.query(Catalog).all()
        return jsonify({'catalog': [item.to_dict(
            only=('id', 'name', 'categorss')) for item in catalog]})

