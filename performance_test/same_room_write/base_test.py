import sys
from time import sleep

import requests
from locust.runners import MasterRunner, WorkerRunner

import string
from datetime import datetime
from random import choice


def _setup_test(
        environment, create_indices: bool, message_base_route: str, write_concern_majority: bool,
        users: list
):
    print(f'Cleaning up for tests in {message_base_route}...')
    response = requests.get(f'{environment.host}/clear')
    if response.status_code != 200:
        raise Exception(f'Error cleaning up: {response.status_code}')
    if create_indices:
        print('Creating indices...')
        response = requests.post(f'{environment.host}/{message_base_route}/indices')
        if response.status_code != 200:
            raise Exception(f'Error creating indices: {response.status_code}')
    if write_concern_majority:
        print('Checking write_concern majority...')
        response = requests.get(f'{environment.host}/write_concern')
        if response.status_code != 200 or response.json()['write_concern'] != 'majority':
            raise Exception(f'Please set the WRITE_CONCERN env var as majority before starting the app')

    # Creating users
    for username in users:
        response = requests.put(f'{environment.host}/users', json={'username': username})
        if response.status_code != 200:
            raise Exception(response.json())

    # Create room
    response = requests.put(f'{environment.host}/rooms', json={'name': 'Test room', 'members': users})
    return response.json()['room_id']


def _send_room_id(environment, room_id: str):
    environment.runner.send_message('receive_room_id', room_id)


def _receive_room_id(msg):
    return msg.data


def _on_locust_init(environment, send_room_id_func, receive_room_id_func):
    if not isinstance(environment.runner, WorkerRunner):
        environment.runner.register_message('send_room_id', send_room_id_func)
    if not isinstance(environment.runner, MasterRunner):
        environment.runner.register_message('receive_room_id', receive_room_id_func)


class BasePutMessages:

    def __init__(self, app_users_: list, room_id: str, messages_route: str, client):
        self.username = app_users_[0]
        self._room_id = room_id
        self._messages_route = messages_route
        self.client = client

    @staticmethod
    def _generate_random_str(length: int = 32):
        return ''.join([choice(string.digits + string.ascii_letters + ' ') for __ in range(length)])

    def put_messages(self, message_len: int):
        self.client.put(f'/rooms/{self._room_id}/{self._messages_route}',
                        json={'username': self.username,
                              'message': f'{self._generate_random_str(message_len)}',
                              'date': datetime.utcnow().isoformat()}
                        )


