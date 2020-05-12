from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.trainers import Trainer

parser = reqparse.RequestParser()
parser.add_argument('surname', required=True)
parser.add_argument('name', required=True)
parser.add_argument('age', required=True, type=int)
parser.add_argument('telefon', required=True)
parser.add_argument('email', required=True)


class TrainersResource(Resource):
    def get(self, trainer_id):
        session = db_session.create_session()
        trainer = session.query(Trainer).get(trainer_id)
        if trainer:
            return jsonify({'trainer': trainer.to_dict(
                only=('id', 'surname', 'name', 'age', 'email', 'telefon'))})
        else:
            return jsonify({'error': 'get treter'})


class TrainersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        trainers = session.query(Trainer).all()
        return jsonify({'trainers': [item.to_dict(
            only=('id', 'surname', 'name', 'age', 'email', 'telefon')) for item in trainers]})
