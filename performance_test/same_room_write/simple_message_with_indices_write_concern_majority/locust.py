import sys

import requests

sys.path.insert(0, '../..')

import string
from datetime import datetime
from random import choice

from locust import HttpUser, task, events

_room_id = None
_users = ['sahudy', 'eduardo', 'patricia']


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _room_id

    print('Cleaning up...')
    response = requests.get(f'{environment.host}/clear')
    if response.status_code != 200:
        raise Exception(f'Error cleaning up: {response.status_code}')
    response = requests.post(f'{environment.host}/simple_messages/indices')
    if response.status_code != 200:
        raise Exception(f'Error creating indices: {response.status_code}')
    response = requests.get(f'{environment.host}/write_concern')
    if response.status_code != 200 or response.json()['write_concern'] != 'majority':
        raise Exception(f'Please set the WRITE_CONCERN env var as majority before starting the app')

    # Creating users
    for username in _users:
        response = requests.put(f'{environment.host}/users', json={'username': username})
        if response.status_code != 200:
            raise Exception(response.json())

    # Create room
    response = requests.put(f'{environment.host}/rooms', json={'name': 'Test room', 'members': _users})
    _room_id = response.json()['room_id']


class PutMessages(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.username = _users[0]

    @staticmethod
    def _generate_random_str(length: int = 32):
        return ''.join([choice(string.digits + string.ascii_letters + ' ') for __ in range(length)])

    def _put_messages(self, message_len: int):
        self.client.put(f'/rooms/{_room_id}/simple_messages',
                        json={'username': self.username,
                              'message': f'{self._generate_random_str(message_len)}',
                              'date': datetime.utcnow().isoformat()}
                        )

    @task
    def put_small_messages(self):
        self._put_messages(message_len=50)

    @task
    def put_medium_messages(self):
        self._put_messages(message_len=100)

    @task
    def put_big_messages(self):
        self._put_messages(message_len=256)