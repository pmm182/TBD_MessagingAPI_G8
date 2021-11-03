from time import sleep

from locust.runners import WorkerRunner

from base_test import _send_room_id, _receive_room_id, _on_locust_init, BasePutMessages, _setup_test

from locust import events, task, HttpUser

_room_id = None
_users = ['sahudy', 'eduardo', 'patricia']
_messages_route = 'simple_messages'


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _room_id

    if not isinstance(environment.runner, WorkerRunner):
        _room_id = _setup_test(
            environment, create_indices=True, message_base_route=_messages_route, write_concern_majority=False,
            users=_users
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
        self._base_test = BasePutMessages(app_users_=_users, room_id=_room_id, messages_route=_messages_route,
                                          client=self.client)

    @task
    def put_small_messages(self):
        self._base_test.put_messages(message_len=50)

    @task
    def put_medium_messages(self):
        self._base_test.put_messages(message_len=100)

    @task
    def put_big_messages(self):
        self._base_test.put_messages(message_len=256)
