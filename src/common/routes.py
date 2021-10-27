from pymongo import MongoClient

from config import ServerConfig


def register_generic_routes(app, server_config: ServerConfig):

    @app.route('/clear', methods=['GET'])
    def clear():
        mongo = MongoClient(
            host=server_config.server, port=server_config.port, username=server_config.username,
            password=server_config.password
        )
        mongo.drop_database(server_config.database)
        return '', 200
