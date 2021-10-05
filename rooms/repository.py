from typing import List

from bson import ObjectId
from pymongo.database import Database

from rooms.data import Room
from rooms.exceptions import RoomNotFoundError, NoSuchMemberFound


class RoomRepository:

    def __init__(self, database: Database):
        self._database = database
        self._collection = self._database.get_collection('rooms')

    @staticmethod
    def _create_room_from_mongo(result: dict) -> Room:
        return Room(id_=str(result['_id']), members=result['members'], name=result.get('name'))

    def insert_room(self, room: Room) -> str:
        doc_ = {'members': room.members}
        if room.name:
            doc_['name'] = room.name
        inserted_doc = self._collection.insert_one(doc_)
        return str(inserted_doc.inserted_id)

    def get_rooms(self) -> List[Room]:
        rooms = []
        for result in self._collection.find():
            rooms.append(self._create_room_from_mongo(result))
        return rooms

    def get_room(self, id_: str) -> Room:
        room_result = self._collection.find_one({'_id': ObjectId(id_)})
        if room_result:
            return self._create_room_from_mongo(room_result)
        raise RoomNotFoundError(id_)

    def get_rooms_by_member(self, username: str) -> List[Room]:
        rooms = []
        room_results = self._collection.find({'members': username})
        for room_result in room_results:
            rooms.append(self._create_room_from_mongo(room_result))
        if not rooms:
            raise NoSuchMemberFound(username)
        return rooms
