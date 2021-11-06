import json

from enum import Enum

import requests
from locust.runners import MasterRunner, WorkerRunner

import string
from datetime import datetime
from random import choice


class MongoReadPreference(Enum):
    PRIMARY = 'Primary'
    SECONDARY = 'Secondary'
    NEAREST = 'Nearest'


def _setup_test(
        environment, create_indices: bool, message_base_route: str, read_preference: MongoReadPreference
):
    expected_room_amount = 600
    room_per_amount = {}
    print(f'Verifying data for tests...')
    response = requests.get(f'{environment.host}/{message_base_route}/amount')
    if response.status_code != 200 or response.json()['amount'] != 0:
        raise Exception(f'Error getting messages or database messages not cleaned')
    if create_indices:
        print('Creating indices...')
        response = requests.post(f'{environment.host}/{message_base_route}/indices')
        if response.status_code != 200:
            raise Exception(f'Error creating indices: {response.status_code}')
    print('Checking read_preference...')
    response = requests.get(f'{environment.host}/read_preference')
    if response.status_code != 200 or read_preference.value not in response.json()['read_preference']:
        raise Exception(f'Please set the READ_PREFERENCE env var to {read_preference.name}')
    response = requests.get(f'{environment.host}/rooms')
    response_data = response.json()
    if expected_room_amount != len(response_data):
        raise Exception(f'Rooms not loaded correctly... Expecting {expected_room_amount} but got {len(response_data)}')
    for room in response_data:
        members = room['members']
        room_id = room['id']
        amount_of_members = str(len(members))
        if amount_of_members not in room_per_amount:
            room_per_amount[amount_of_members] = {}
        room_per_amount[amount_of_members][room_id] = members
    return room_per_amount


def _send_room_per_amount(environment, room_per_amount: dict):
    environment.runner.send_message('receive_room_per_amount', json.dumps(room_per_amount))


def _receive_room_per_amount(msg):
    return json.loads(msg.data)


def _on_locust_init(environment, send_room_per_amount_func, receive_room_per_amount_func):
    if not isinstance(environment.runner, WorkerRunner):
        environment.runner.register_message('send_room_per_amount', send_room_per_amount_func)
    if not isinstance(environment.runner, MasterRunner):
        environment.runner.register_message('receive_room_per_amount', receive_room_per_amount_func)


class BaseMessages:

    def __init__(self, room_per_amount: dict, messages_route: str, client):
        self._room_per_amount = room_per_amount
        self._messages_route = messages_route
        self._last_seen_per_room = {}
        self.client = client

    @staticmethod
    def _generate_random_str(length: int = 32):
        return ''.join([choice(string.digits + string.ascii_letters + ' ') for __ in range(length)])

    def put_messages(self, message_len: int, amount_per_room: int):
        amount_per_room_str = str(amount_per_room)
        room_id = choice(list(self._room_per_amount[amount_per_room_str].keys()))
        username = choice(self._room_per_amount[amount_per_room_str][room_id])
        self.client.put(f'/rooms/{room_id}/{self._messages_route}',
                        json={'username': username,
                              'message': f'{self._generate_random_str(message_len)}',
                              'date': datetime.utcnow().isoformat()},
                        name=f'/{self._messages_route}')

    def get_messages(self, amount_per_room: int, use_last_seen_control: bool):
        amount_per_room_str = str(amount_per_room)
        room_id = choice(list(self._room_per_amount[amount_per_room_str].keys()))
        username = choice(self._room_per_amount[amount_per_room_str][room_id])
        param = {'username': username}
        name = f'/{self._messages_route}/full'
        if use_last_seen_control and room_id in self._last_seen_per_room:
            param['last_seen'] = self._last_seen_per_room[room_id]
            name = f'/{self._messages_route}'
        response = self.client.get(f'/rooms/{room_id}/{self._messages_route}',
                                   json=param, name=name)
        if response.status_code == 200:
            messages = response.json()
            if messages:
                self._last_seen_per_room[room_id] = messages[-1]['date']
