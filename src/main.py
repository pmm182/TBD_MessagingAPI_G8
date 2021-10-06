import os

from flask import Flask, jsonify
from pymongo import MongoClient

from config import local_server, docker_server
from exceptions import AppError
from rooms.repository import RoomRepository
from rooms.routes import register_room_routes
from users.repository import UserRepository
from users.routes import register_user_routes


def register_error_handler(app_):

    @app_.errorhandler(AppError)
    def handle_app_error(error):
        return jsonify({'message': error.msg}), error.status_code


def get_app():
    app = Flask(__name__)

    env_type = os.getenv('ENVIRONMENT')
    if env_type == 'DOCKER':
        server_config = docker_server
    else:
        server_config = local_server
    mongo = MongoClient(
        host=server_config.server, port=server_config.port, username=server_config.username,
        password=server_config.password
    )
    database = mongo.get_database(server_config.database)
    user_repository = UserRepository(database)
    room_repository = RoomRepository(database)
    register_user_routes(app=app, user_repository=user_repository)
    register_room_routes(app=app, user_repository=user_repository, room_repository=room_repository)
    register_error_handler(app)
    return app


if __name__ == '__main__':
    print("*******************************************************************************************************")
    print('Bem vindo ao servidor de API para mensageria com MongoDB.')
    print('O objetivo desta aplicação é fornecer um caminho para avaliar o comportamento do MongoDB como NoSQL '
          'sob diferentes configurações.')
    print("*******************************************************************************************************")
    app_ = get_app()
    app_.run(debug=True, port=8080)
