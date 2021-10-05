from typing import List

from pymongo import MongoClient
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError

from users.data import User
from users.exceptions import DuplicateUserError, UserNotFoundError


class UserRepository:

    def __init__(self, database: Database):
        self._database = database
        self._collection = self._database.get_collection('users')

    @staticmethod
    def _create_user_from_mongo(result: dict) -> User:
        return User(username=result['_id'], name=result['name'])

    def insert_user(self, user: User):
        try:
            self._collection.insert_one(
                {'_id': user.username, 'name': user.name}
            )
        except DuplicateKeyError:
            raise DuplicateUserError(username=user.username)

    def delete_user(self, username: str):
        self._collection.delete_one({'_id': username})

    def get_users(self) -> List[User]:
        users = []
        for result in self._collection.find():
            users.append(self._create_user_from_mongo(result))
        return users

    def get_user(self, username: str) -> User:
        user_result = self._collection.find_one({'_id': username})
        if user_result:
            return self._create_user_from_mongo(user_result)
        raise UserNotFoundError(username)
