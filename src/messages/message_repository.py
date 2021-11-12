from abc import ABC, abstractmethod
from datetime import datetime, timedelta

import pymongo
from pymongo import ASCENDING
from pymongo.database import Database

from messages.data import Message


class MessageRepository(ABC):

    @abstractmethod
    def insert_message(self, message: Message):
        pass

    @abstractmethod
    def get_messages(self, room_id: str, last_seen: datetime = None):
        pass

    @abstractmethod
    def create_indices(self):
        pass

    @abstractmethod
    def get_amount(self):
        pass


class MessagesByRoomRepository(MessageRepository):

    def __init__(self, database: Database, enable_sharding: bool = False, partition_interval: str = 'days'):
        self._database = database
        self._partition_interval = partition_interval
        if enable_sharding:
            response = database.client.admin.command('shardCollection',
                                                     f'{database.name}.messages', key={'room_id': 'hashed'})
            if response['ok'] != 1:
                raise Exception('Could not create sharded collection')
        self._messages_collection = self._database.get_collection('messages')

    @staticmethod
    def _create_message_from_mongo(result: dict, room_id: str) -> Message:
        return Message(room_id=room_id, from_=result['from'], message=result['message'], date=result['date'])

    def insert_message(self, message: Message):
        mongo_message = {'from': message.from_, 'date': message.date, 'message': message.message}
        if self._partition_interval == 'days':
            partition_start = message.date.date()
        elif self._partition_interval == 'minutes':
            partition_start = message.date.replace(second=0, microsecond=0)
        else:
            raise NotImplementedError()
        partition_end = partition_start + timedelta(**{self._partition_interval: 1})

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
        return sorted(messages_result, key=lambda m: m.date)

    def create_indices(self):
        self._messages_collection.create_index([
            ('room_id', pymongo.ASCENDING), ('partition_date', pymongo.ASCENDING)
        ])

    def get_amount(self):
        return self._messages_collection.count()


class SimpleMessageRepository(MessageRepository):

    def __init__(self, database: Database, enable_sharding: bool = False):
        self._database = database
        if enable_sharding:
            response = database.client.admin.command('shardCollection',
                                                     f'{database.name}.simple_messages', key={'room_id': 'hashed'})
            if response['ok'] != 1:
                raise Exception('Could not create sharded collection')
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
        messages = self._messages_collection.find(query_params).sort([('date', ASCENDING)])
        messages_result = []
        for message in messages:
            messages_result.append(self._create_message_from_mongo(result=message, room_id=room_id))
        return messages_result

    def create_indices(self):
        self._messages_collection.create_index([
            ('room_id', pymongo.ASCENDING)
        ])

    def get_amount(self):
        return self._messages_collection.count()
