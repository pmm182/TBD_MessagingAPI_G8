from flask import jsonify
from pymongo import MongoClient


def register_generic_routes(app, mongo: MongoClient, database_name: str):

    @app.route('/health', methods=['GET'])
    def health():
        return '', 200

    @app.route('/clear', methods=['GET'])
    def clear():
        mongo.drop_database(database_name)
        return '', 200

    @app.route('/write_concern', methods=['GET'])
    def write_concern():
        return jsonify({'write_concern': mongo.write_concern.document.get('w')}), 200

    @app.route('/read_preference', methods=['GET'])
    def read_preference():
        return jsonify({'read_preference': str(mongo.read_preference)}), 200


