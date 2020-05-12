from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from data import db_session
from data.users import User

API_TOKEN = 'secret_token0000'


def set_password(password):
    hashed_password = generate_password_hash(password)
    return hashed_password


class UsersResource(Resource):
    def get(self, user_id, token):
        if token == API_TOKEN:
            session = db_session.create_session()
            user = session.query(User).get(user_id)
            if user:
                return jsonify({'user': user.to_dict(
                    only=('id', 'login', 'surname', 'name', 'age', 'address', 'email', 'admin_chek'))})
            else:
                return jsonify({'error': f'not fond user {user_id}'})
        else:
            return jsonify({'error': 'not token'})


class UsersListResource(Resource):
    def get(self, token):
        if token == API_TOKEN:
            session = db_session.create_session()
            user = session.query(User).all()
            return jsonify({'users': [item.to_dict(
                only=('id', 'login', 'surname', 'name', 'age', 'address',
                      'email', 'admin_chek')) for item in user]})
        else:
            return jsonify({'error': 'not token'})
