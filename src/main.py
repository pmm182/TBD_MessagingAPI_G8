import os

from flask import Flask, jsonify
from pymongo import MongoClient

from config import local_server, docker_server, atlas_server, ServerConfig
from exceptions import AppError
from common.routes import register_generic_routes, register_messages_indices_routes, \
    register_simple_messages_indices_routes
from messages.message_repository import MessagesByRoomRepository, SimpleMessageRepository
from messages.routes import register_message_routes, register_simple_message_routes
from rooms.room_repository import RoomRepository
from rooms.routes import register_room_routes
from users.repository import UserRepository
from users.routes import register_user_routes


def register_error_handler(app_):

    @app_.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'message': error.msg}), error.status_code


def create_app(server_config: ServerConfig):
    app = Flask(__name__)
    write_concern = os.getenv('WRITE_CONCERN', 1)
    mongo = MongoClient(
        host=server_config.server, port=server_config.port, username=server_config.username,
        password=server_config.password, w=write_concern
    )
    database = mongo.get_database(server_config.database)
    user_repository = UserRepository(database)
    room_repository = RoomRepository(database)
    messages_by_room_repository = MessagesByRoomRepository(database)
    register_user_routes(app=app, user_repository=user_repository)
    register_room_routes(app=app, user_repository=user_repository, room_repository=room_repository)
    register_message_routes(app=app, room_repository=room_repository, message_repository=messages_by_room_repository)
    simple_message_repository = SimpleMessageRepository(database)
    register_simple_message_routes(app=app, room_repository=room_repository,
                                   message_repository=simple_message_repository)
    register_generic_routes(app=app, mongo=mongo, database_name=server_config.database)
    register_messages_indices_routes(app=app, message_repository=messages_by_room_repository)
    register_simple_messages_indices_routes(app=app, message_repository=simple_message_repository)
    register_error_handler(app)
    return app


def get_app():
    env_type = os.getenv('ENVIRONMENT')
    print('Loading DB from environment:', env_type)
    if env_type == 'DOCKER':
        server_config = docker_server
    elif env_type == 'ATLAS':
        server_config = atlas_server
    else:
        server_config = local_server
    return create_app(server_config)


if __name__ == '__main__':
    print("*******************************************************************************************************")
    print('Bem vindo ao servidor de API para mensageria com MongoDB.')
    print('O objetivo desta aplicação é fornecer um caminho para avaliar o comportamento do MongoDB como NoSQL '
          'sob diferentes configurações.')
    print("*******************************************************************************************************")
    app_ = get_app()
    app_.run(debug=True, port=8080)
