from dataclasses import dataclass
from typing import Optional


@dataclass
class ServerConfig:

    server: str
    port: int = 27017
    username: Optional[str] = None
    password: Optional[str] = None
    database: str = 'messaging8'


local_server = ServerConfig(server='localhost')
docker_server = ServerConfig(server='mongo')
atlas_server = ServerConfig(server='mongodb+srv://cluster0.jjwcl.mongodb.net', 
                             username='messagingappg8',
                             password='messagingappg8')
