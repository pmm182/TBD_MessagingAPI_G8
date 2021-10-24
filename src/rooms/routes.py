
from flask import request, jsonify

from rooms.data import Room
from rooms.exceptions import InvalidDataError
from rooms.room_repository import RoomRepository
from users.repository import UserRepository


def register_room_routes(app, room_repository: RoomRepository, user_repository: UserRepository):

    @app.route(f'/rooms', methods=['PUT'])
    def create_room():
        name = request.json.get('name')
        members = request.json['members']

        if members:
            # Validate whether the users exist
            for member in members:
                user_repository.get_user(member)
            id_ = room_repository.insert_room(Room(members=members, name=name))
            return jsonify({'message': f'Successfully created room {id_}'}), 200
        else:
            raise InvalidDataError()

    @app.route('/rooms_by_user', methods=['GET'])
    def get_rooms_by_user():
        username = request.values['username']
        rooms = room_repository.get_rooms_by_member(username=username)
        return jsonify([room.to_dict() for room in rooms]), 200
