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
from data.stories import Stories

parser = reqparse.RequestParser()
parser.add_argument('user_id', required=True, type=int)
parser.add_argument('product_id', required=True, type=int)


def abort_if_news_not_found(stories_id):
    session = db_session.create_session()
    stories = session.query(Stories).get(stories_id)
    if not stories:
        abort(404, message=f"stories {stories_id} not found")


class UsersResource(Resource):
    def get(self, stories_id):
        abort_if_news_not_found(stories_id)
        session = db_session.create_session()
        user = session.query(Stories).get(stories_id)
        return jsonify({'stories': user.to_dict(
            only=('id', 'user_id', 'product_id'))})

    def delete(self, stories_id):
        abort_if_news_not_found(stories_id)
        session = db_session.create_session()
        user = session.query(Stories).get(stories_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        user = session.query(Stories).all()
        return jsonify({'stories': [item.to_dict(
            only=('id', 'user_id', 'product_id')) for item in user]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = Stories(
            user_id=args['user_id'],
            product_id=args['product_id'],
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})
