import json
import string
from datetime import datetime
from random import choice, randint

from locust import HttpUser, task


class PutMessages(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.room_id = None
        self.users = ['sahudy', 'eduardo', 'patricia']
        self.username = self.users[0]

    @staticmethod
    def _generate_random_str(length: int = 32):
        return ''.join([choice(string.digits + string.ascii_letters + ' ') for __ in range(length)])

    @task
    def put_messages(self):
        self.client.put(f'/rooms/{self.room_id}/messages',
                        json={'username': self.username,
                              'message': f'Hi, I\'m {self.username}. {self._generate_random_str(randint(0, 512))}',
                              'date': datetime.utcnow().isoformat()}
                        )

    def on_start(self):
        # Creating users
        for username in self.users:
            response = self.client.put('/users', json={'username': username})
            if response.status_code not in (200, 409):
                raise Exception(response.json())

        # Create room
        self.client.put('/rooms', json={'name': 'Test room', 'members': self.users})

        # Get room
        response = self.client.get('/rooms_by_user', params={'username': self.username})
        self.room_id = response.json()[0]['id']
