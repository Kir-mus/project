from flask_restful import reqparse, abort, Api, Resource
from flask import Flask, jsonify
from data import db_session
from data.categories import Categories
from data.products import Product


class CatalogsResource(Resource):
    def get(self, catalog_id):
        session = db_session.create_session()
        categor = session.query(Categories).get(catalog_id)
        if categor:
            list_product = categor.products.split(', ')
            names_prod = {}
            for item in list_product:
                try:
                    name = session.query(Product).get(int(item))
                    names_prod[int(item)] = name.name
                except Exception as er:
                    pass
            return jsonify({'catalog': {'id': categor.id, 'name': categor.name, 'products': names_prod}})
        else:
            return jsonify({'error': 'not api categor fond'})


class CatalogsListResource(Resource):
    def get(self):
        session = db_session.create_session()
        catalog = session.query(Categories).all()
        o = []
        for categor in catalog:
            list_product = categor.products.split(', ')
            names_prod = {}
            for item in list_product:
                try:
                    name = session.query(Product).get(int(item))
                    if name is not None:
                        names_prod[int(item)] = name.name
                except Exception as ex:
                    jsonify({'error': f'error catalog {ex}'})
            o.append({'id': int(categor.id), 'name': categor.name, 'products': names_prod})
        return jsonify({'catalog': o})
