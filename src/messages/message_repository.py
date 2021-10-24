from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from pymongo.database import Database

from messages.data import Message


class MessageRepository(ABC):

    @abstractmethod
    def insert_message(self, message: Message):
        pass

    @abstractmethod
    def get_messages(self, room_id: str, last_seen: datetime = None):
        pass


class MessagesByRoomRepository(MessageRepository):

    def __init__(self, database: Database):
        self._database = database
        self._messages_collection = self._database.get_collection('messages')

    @staticmethod
    def _create_message_from_mongo(result: dict, room_id: str) -> Message:
        return Message(room_id=room_id, from_=result['from'], message=result['message'], date=result['date'])

    def insert_message(self, message: Message):
        mongo_message = {'from': message.from_, 'date': message.date, 'message': message.message}
        partition_start = message.date.date()
        partition_end = partition_start + timedelta(days=1)

        query = {
            'partition_date': [partition_start.isoformat(), partition_end.isoformat()],
            'room_id': message.room_id
        }
        values = {'$push': {'messages': mongo_message}}

        return self._messages_collection.update_one(query, values, upsert=True)

    def get_messages(self, room_id: str, last_seen: datetime = None):
        query_params = {'room_id': room_id}
        if last_seen:
            query_params['partition_date.1'] = {'$gt': last_seen.isoformat()}
        partitions = self._messages_collection.find(query_params)
        messages_result = []
        for partition in partitions:
            for message in partition['messages']:
                if not last_seen or message['date'] > last_seen:
                    messages_result.append(self._create_message_from_mongo(result=message, room_id=room_id))
        return messages_result


class SimpleMessageRepository(MessageRepository):

    def __init__(self, database: Database):
        self._database = database
        self._messages_collection = self._database.get_collection('simple_messages')

    @staticmethod
    def _create_message_from_mongo(result: dict, room_id: str) -> Message:
        return Message(room_id=room_id, from_=result['from'], message=result['message'], date=result['date'])

    def insert_message(self, message: Message):
        mongo_message = {'from': message.from_, 'date': message.date, 'message': message.message,
                         'room_id': message.room_id}
        return self._messages_collection.insert_one(mongo_message)

    def get_messages(self, room_id: str, last_seen: datetime = None):
        query_params = {'room_id': room_id}
        if last_seen:
            query_params['date'] = {'$gt': last_seen}
        messages = self._messages_collection.find(query_params).sort({'date': 1})
        messages_result = []
        for message in messages:
            messages_result.append(self._create_message_from_mongo(result=message, room_id=room_id))
        return messages_result
