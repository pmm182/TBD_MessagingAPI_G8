import json

import requests


protocol = 'http'
server = 'localhost'
port = 8080


def get_url(path_: str):
    return f'{protocol}://{server}:{port}/{path_}'


if __name__ == '__main__':
    users = ['sahudy', 'eduardo', 'patricia']

    # Creating users
    for username in users:
        response = requests.put(get_url('users'), json={'username': username, 'name': username.capitalize()})
        if response.status_code not in (200, 409):
            raise Exception(json.dumps(response.json()))

    # Create room
    requests.put(get_url('rooms'), json={'name': 'Test room', 'members': users})

