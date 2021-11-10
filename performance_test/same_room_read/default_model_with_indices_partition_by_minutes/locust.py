from time import sleep

from locust.runners import WorkerRunner

from base_test import _send_room_id, _receive_room_id, _on_locust_init, BaseMessages, _setup_test, MongoReadPreference

from locust import events, task, HttpUser

_room_id = None
_users = ['sahudy', 'eduardo', 'patricia']
_messages_route = 'messages'


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _room_id

    if not isinstance(environment.runner, WorkerRunner):
        _room_id = _setup_test(
            environment, create_indices=True, message_base_route=_messages_route,
            read_preference=MongoReadPreference.PRIMARY, users=_users
        )
    else:
        while not _room_id:
            environment.runner.send_message('send_room_id')
            sleep(1)


def send_room_id(environment, msg, **kwargs):
    global _room_id
    _send_room_id(environment, room_id=_room_id)


def receive_room_id(msg, **kwargs):
    global _room_id
    _room_id = _receive_room_id(msg)


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    _on_locust_init(environment, send_room_id_func=send_room_id, receive_room_id_func=receive_room_id)


class PutMessages(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_test = BaseMessages(app_users_=_users, room_id=_room_id, messages_route=_messages_route,
                                       client=self.client)
        self._last_seen = None

    @task(2)
    def put_messages(self):
        self._base_test.put_messages(message_len=100)

    @task(4)
    def get_messages(self):
        response = self._base_test.get_messages(last_seen=self._last_seen)
        if response.status_code == 200:
            messages = response.json()
            if messages:
                self._last_seen = messages[-1]['date']

    @task(1)
    def get_all_messages(self):
        self._base_test.get_messages()
