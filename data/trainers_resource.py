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
from data.trainers import Trainer

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('clientele', required=False)
parser.add_argument('email', required=True)


def abort_if_news_not_found(trainer_id):
    session = db_session.create_session()
    user = session.query(Trainer).get(trainer_id)
    if not user:
        abort(404, message=f"Trainer {trainer_id} not found")
    elif session.query(Trainer).filter(Trainer.email == user.email).first():
        abort(404, message=f"Trainer {trainer_id} act")


class TrainersResource(Resource):
    def get(self, trainer_id):
        abort_if_news_not_found(trainer_id)
        session = db_session.create_session()
        trainer = session.query(Trainer).get(trainer_id)
        return jsonify({'trainer': trainer.to_dict(
            only=('id', 'surname', 'name', 'age', 'email'))})

    def delete(self, trainer_id):
        abort_if_news_not_found(trainer_id)
        session = db_session.create_session()
        trainer = session.query(Trainer).get(trainer_id)
        session.delete(trainer)
        session.commit()
        return jsonify({'success': 'OK'})


class TrainersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        trainers = session.query(Trainer).all()
        return jsonify({'trainers': [item.to_dict(
            only=('id', 'surname', 'name', 'age',
                  'email')) for item in trainers]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        trainer = Trainer(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            email=args['email']
        )
        session.add(trainer)
        session.commit()
        return jsonify({'success': 'OK'})
