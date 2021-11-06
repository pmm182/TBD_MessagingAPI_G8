from datetime import datetime
from flask import jsonify, request

from messages.data import Message
from messages.message_repository import MessageRepository
from rooms.room_repository import RoomRepository


def _create_message(id_, request_json: dict, room_repository: RoomRepository,
                    message_repository: MessageRepository):
    room_id = id_
    username = request_json['username']
    message = request_json['message']
    date_str = request_json.get('date')

    if date_str:
        date = datetime.fromisoformat(date_str)
    else:
        date = datetime.utcnow()

    # Validations
    room_repository.check_member_in_room(username=username, room_id=room_id)

    message_repository.insert_message(Message(room_id=room_id, from_=username, message=message, date=date))
    return jsonify({'message': 'Message sent'}), 200


def _get_messages(id_, request_json: dict, room_repository: RoomRepository,
                  message_repository: MessageRepository):
    room_id = id_
    username = request_json['username']
    last_seen_str = request_json.get('last_seen')
    last_seen = None
    if last_seen_str:
        last_seen = datetime.fromisoformat(last_seen_str)

    # Validations
    room_repository.check_member_in_room(username=username, room_id=room_id)

    messages = message_repository.get_messages(room_id=room_id, last_seen=last_seen)
    return jsonify([message.to_dict() for message in messages])


def _get_messages_amount(message_repository: MessageRepository):
    return jsonify({'amount': message_repository.get_amount()})


def register_message_routes(app, room_repository: RoomRepository, message_repository: MessageRepository):

    @app.route('/rooms/<id_>/messages', methods=['PUT'])
    def create_message(id_):
        return _create_message(id_=id_, request_json=request.json, room_repository=room_repository,
                               message_repository=message_repository)

    @app.route('/rooms/<id_>/messages', methods=['GET'])
    def get_messages(id_):
        return _get_messages(id_=id_, request_json=request.json, room_repository=room_repository,
                             message_repository=message_repository)

    @app.route('/rooms/<id_>/messages/amount', methods=['GET'])
    def get_messages_amount(id_):
        return _get_messages_amount(message_repository)


def register_simple_message_routes(app, room_repository: RoomRepository, message_repository: MessageRepository):

    @app.route('/rooms/<id_>/simple_messages', methods=['PUT'])
    def simple_create_message(id_):
        return _create_message(id_=id_, request_json=request.json, room_repository=room_repository,
                               message_repository=message_repository)

    @app.route('/rooms/<id_>/simple_messages', methods=['GET'])
    def simple_get_messages(id_):
        return _get_messages(id_=id_, request_json=request.json, room_repository=room_repository,
                             message_repository=message_repository)

    @app.route('/rooms/<id_>/simple_messages/amount', methods=['GET'])
    def get_simple_messages_amount(id_):
        return _get_messages_amount(message_repository)
