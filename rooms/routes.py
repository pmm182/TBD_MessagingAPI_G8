from datetime import datetime

from flask import request, jsonify

from rooms.data import Room, Message
from rooms.exceptions import InvalidDataError
from rooms.repository import RoomRepository
from users.repository import UserRepository


def register_room_routes(app, room_repository: RoomRepository, user_repository: UserRepository):

    @app.route('/rooms', methods=['PUT'])
    def create_room():
        name = request.json['name']
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

    @app.route('/rooms/<id_>/messages', methods=['PUT'])
    def create_message(id_):
        room_id = id_
        username = request.json['username']
        message = request.json['message']
        date_str = request.json.get('date')

        if date_str:
            date = datetime.fromisoformat(date_str)
        else:
            date = datetime.utcnow()

        # Validations
        room_repository.check_member_in_room(username=username, room_id=room_id)

        room_repository.insert_message(Message(room_id=room_id, from_=username, message=message, date=date))
        return jsonify({'message': 'Message sent'}), 200

    @app.route('/rooms/<id_>/messages', methods=['GET'])
    def get_messages(id_):
        room_id = id_
        username = request.json['username']
        last_seen_str = request.json.get('last_seen')
        last_seen = None
        if last_seen_str:
            last_seen = datetime.fromisoformat(last_seen_str)

        # Validations
        room_repository.check_member_in_room(username=username, room_id=room_id)

        messages = room_repository.get_messages(room_id=room_id, last_seen=last_seen)
        return jsonify([message.to_dict() for message in messages])
