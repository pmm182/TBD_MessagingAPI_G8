from unittest import TestCase

from pymongo import MongoClient

from config import ServerConfig
from main import create_app


class TestCommon(TestCase):

    _COLLECTION_NAMES = ('messages', 'simple_messages', 'rooms', 'users')

    def setUp(self) -> None:
        server_config = ServerConfig(server='localhost', database='test_db')
        self.mongo = MongoClient(
            host=server_config.server, port=server_config.port
        )
        database = self.mongo.get_database(server_config.database)

        for collection_name in self._COLLECTION_NAMES:
            database.get_collection(collection_name).delete_many({})

        app = create_app(server_config)
        self.test_client = app.test_client()

    def tearDown(self) -> None:
        self.mongo.close()

