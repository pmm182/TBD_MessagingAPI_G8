from flask import request, jsonify

from users.data import User
from users.repository import UserRepository


def register_user_routes(app, user_repository: UserRepository):

    @app.route('/users', methods=['PUT'])
    def create_user():
        name = request.json.get('name')
        username = request.json['username']
        user_repository.insert_user(User(username=username, name=name))
        return jsonify({'message': f'User {username} created'}), 200

    @app.route('/users/<username>', methods=['DELETE'])
    def delete_user(username: str):
        user_repository.delete_user(username)
        return jsonify({'message': f'User {username} created'}), 200

    @app.route('/users', methods=['GET'])
    def get_users():
        users = user_repository.get_users()
        response = [user.to_dict() for user in users]
        return jsonify(response), 200

    @app.route('/users/<username>', methods=['GET'])
    def get_user(username: str):
        user = user_repository.get_user(username)
        return jsonify(user.to_dict()), 200
