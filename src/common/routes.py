from flask import jsonify
from pymongo import MongoClient

from messages.message_repository import MessageRepository


def register_generic_routes(app, mongo: MongoClient, database_name: str):

    @app.route('/clear', methods=['GET'])
    def clear():
        mongo.drop_database(database_name)
        return '', 200

def _create_indices(message_repository: MessageRepository):
    message_repository.create_indices()
    return jsonify({'message': 'Indices created'}), 200


def register_messages_indices_routes(app, message_repository: MessageRepository):

    @app.route('/messages/indices', methods=['POST'])
    def create_message():
        return _create_indices(message_repository=message_repository)


def register_simple_messages_indices_routes(app, message_repository: MessageRepository):

    @app.route('/simple_messages/indices', methods=['POST'])
    def create_message():
        return _create_indices(message_repository=message_repository)
