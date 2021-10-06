from datetime import datetime
from time import sleep

import requests


protocol = 'http'
server = 'localhost'
port = 8080


def get_url(path_: str):
    return f'{protocol}://{server}:{port}/{path_}'


if __name__ == '__main__':
    username = input('Type your username: ')

    response = requests.get(get_url('rooms_by_user'), params={'username': username})
    room_id = response.json()[0]['id']
    i = 0
    last_seen = None

    while True:
        response = requests.put(
            get_url(f'rooms/{room_id}/messages'),
            json={'username': username,
                  'message': f'Hi, I\'m {username} in message {i}',
                  'date': datetime.utcnow().isoformat()}
        )
        params = {'username': username}
        if last_seen:
            params['last_seen'] = last_seen
        response = requests.get(get_url(f'rooms/{room_id}/messages'), json=params)
        messages = sorted(response.json(), key=lambda m: m['date'])
        for message in messages:
            print(f"{message['date']} - {message['from']}: {message['message']}")
            last_seen = message['date']
        sleep(1)
        i += 1

