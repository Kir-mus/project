from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.stories import Stories

API_TOKEN = 'secret_token0000'


class StoriesResource(Resource):
    def get(self, stories_id, token):
        if token == API_TOKEN:
            session = db_session.create_session()
            stories = session.query(Stories).get(stories_id)
            if stories:
                return jsonify({'stories': stories.to_dict(
                    only=('id', 'user_id', 'product_id'))})
            else:
                return jsonify({'error': 'not id stories'})
        else:
            return jsonify({'error': 'not token'})

    def delete(self, stories_id, token):
        if token == API_TOKEN:
            session = db_session.create_session()
            stories = session.query(Stories).get(stories_id)
            if stories:
                session.delete(stories)
                session.commit()
                return jsonify({'success': 'OK'})
            else:
                return jsonify({'error': 'not fond stories'})
        else:
            return jsonify({'error': 'not token'})


class StoriesListResource(Resource):
    def get(self, token):
        if token == API_TOKEN:
            session = db_session.create_session()
            stories = session.query(Stories).all()
            return jsonify({'stories': [item.to_dict(
                only=('id', 'user_id', 'product_id')) for item in stories]})
        else:
            return jsonify({'error': 'not token'})
