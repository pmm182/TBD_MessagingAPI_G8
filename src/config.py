from dataclasses import dataclass
from typing import Optional
import os


@dataclass
class ServerConfig:

    server: str
    port: int = 27017
    username: Optional[str] = None
    password: Optional[str] = None
    database: str = 'messaging8'


local_server = ServerConfig(server='localhost')
docker_server = ServerConfig(server='mongo')
atlas_server = ServerConfig(server=os.getenv('MONGODB_SERVER'),
                            username=os.getenv('MONGODB_USERNAME'),
                            password=os.getenv('MONGODB_PASSWORD'))
