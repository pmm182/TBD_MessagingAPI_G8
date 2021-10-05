from datetime import datetime, timedelta
from typing import List

from bson import ObjectId
from pymongo.database import Database

from src.rooms.data import Room, Message
from src.rooms.exceptions import RoomNotFoundError, NoSuchMemberFound, MemberNotInRoom


class RoomRepository:

    def __init__(self, database: Database):
        self._database = database
        self._rooms_collection = self._database.get_collection('rooms')
        self._messages_collection = self._database.get_collection('messages')

    @staticmethod
    def _create_message_from_mongo(result: dict, room_id: str) -> Message:
        return Message(room_id=room_id, from_=result['from'], message=result['message'], date=result['date'])

    @staticmethod
    def _create_room_from_mongo(result: dict) -> Room:
        return Room(id_=str(result['_id']), members=result['members'], name=result.get('name'))

    def insert_room(self, room: Room) -> str:
        doc_ = {'members': room.members}
        if room.name:
            doc_['name'] = room.name
        inserted_doc = self._rooms_collection.insert_one(doc_)
        return str(inserted_doc.inserted_id)

    def get_rooms(self) -> List[Room]:
        rooms = []
        for result in self._rooms_collection.find():
            rooms.append(self._create_room_from_mongo(result))
        return rooms

    def get_room(self, id_: str) -> Room:
        room_result = self._rooms_collection.find_one({'_id': ObjectId(id_)})
        if room_result:
            return self._create_room_from_mongo(room_result)
        raise RoomNotFoundError(id_)

    def get_rooms_by_member(self, username: str) -> List[Room]:
        rooms = []
        room_results = self._rooms_collection.find({'members': username})
        for room_result in room_results:
            rooms.append(self._create_room_from_mongo(room_result))
        if not rooms:
            raise NoSuchMemberFound(username)
        return rooms

    def check_member_in_room(self, username: str, room_id: str):
        member = self._rooms_collection.find_one({'members': username, '_id': ObjectId(room_id)})
        if not member:
            raise MemberNotInRoom(username=username, room_id=room_id)

    def insert_message(self, message: Message):
        mongo_message = {'from': message.from_, 'date': message.date, 'message': message.message}
        partition_start = message.date.date()
        partition_end = partition_start + timedelta(days=1)

        query = {
            'partition_date': [partition_start, partition_end],
            'room_id': message.room_id
        }
        values = {'$push': {'messages': mongo_message}}

        return self._messages_collection.update_one(query, values, upsert=True)

    def get_messages(self, room_id: str, last_seen: datetime = None):
        query_params = {'room_id': room_id}
        if last_seen:
            query_params['partition_date.1'] = {'$gt': last_seen}
            query_params['messages.date'] = {'$gt': last_seen}
        partitions = self._messages_collection.find(query_params)
        messages_result = []
        for partition in partitions:
            for message in partition['messages']:
                messages_result.append(self._create_message_from_mongo(result=message, room_id=room_id))
        return messages_result
