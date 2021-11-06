from time import sleep

from locust.runners import WorkerRunner

from base_test import _send_room_per_amount, _receive_room_per_amount, _on_locust_init, BasePutMessages, _setup_test

from locust import events, task, HttpUser


_room_per_amount = None
_messages_route = 'messages'


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _room_per_amount

    if not isinstance(environment.runner, WorkerRunner):
        _room_per_amount = _setup_test(
            environment, create_indices=True, message_base_route=_messages_route, write_concern_majority=False
        )
    else:
        while not _room_per_amount:
            environment.runner.send_message('send_user_room_per_amount')
            sleep(1)


def send_room_per_amount(environment, msg, **kwargs):
    _send_room_per_amount(environment, room_per_amount=_room_per_amount)


def receive_room_per_amount(msg, **kwargs):
    global _room_per_amount
    _room_per_amount = _receive_room_per_amount(msg)


@events.init.add_listener
def on_locust_init(environment, **_kwargs):
    _on_locust_init(environment, send_room_per_amount_func=send_room_per_amount,
                    receive_room_per_amount_func=receive_room_per_amount)


class PutMessages(HttpUser):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._base_test = BasePutMessages(
            room_per_amount=_room_per_amount,
            messages_route=_messages_route,
            client=self.client
        )

    @task(5)
    def put_in_room_with_2_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=2)

    @task(1)
    def put_in_room_with_3_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=3)

    @task(2)
    def put_in_room_with_5_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=5)

    @task(2)
    def put_in_room_with_10_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=10)
