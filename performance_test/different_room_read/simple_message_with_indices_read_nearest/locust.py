from time import sleep

from locust.runners import WorkerRunner

from base_test import _send_room_per_amount, _receive_room_per_amount, _on_locust_init, BaseMessages, _setup_test, \
    MongoReadPreference

from locust import events, task, HttpUser


_room_per_amount = None
_messages_route = 'simple_messages'


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    global _room_per_amount

    if not isinstance(environment.runner, WorkerRunner):
        _room_per_amount = _setup_test(
            environment, create_indices=True, message_base_route=_messages_route,
            read_preference=MongoReadPreference.NEAREST
        )
    else:
        while not _room_per_amount:
            environment.runner.send_message('send_room_per_amount')
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
        self._base_test = BaseMessages(
            room_per_amount=_room_per_amount,
            messages_route=_messages_route,
            client=self.client
        )

    @task(10)
    def put_in_room_with_2_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=2)

    @task(2)
    def put_in_room_with_3_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=3)

    @task(4)
    def put_in_room_with_5_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=5)

    @task(4)
    def put_in_room_with_10_users(self):
        self._base_test.put_messages(message_len=200, amount_per_room=10)

    @task(20)
    def get_messages_room_with_2(self):
        self._base_test.get_messages(amount_per_room=2, use_last_seen_control=True)

    @task(4)
    def get_messages_room_with_3(self):
        self._base_test.get_messages(amount_per_room=3, use_last_seen_control=True)

    @task(8)
    def get_messages_room_with_5(self):
        self._base_test.get_messages(amount_per_room=5, use_last_seen_control=True)

    @task(8)
    def get_messages_room_with_10(self):
        self._base_test.get_messages(amount_per_room=10, use_last_seen_control=True)

    @task(5)
    def get_full_messages_room_with_2(self):
        self._base_test.get_messages(amount_per_room=2, use_last_seen_control=False)

    @task(1)
    def get_full_messages_room_with_3(self):
        self._base_test.get_messages(amount_per_room=3, use_last_seen_control=False)

    @task(2)
    def get_full_messages_room_with_5(self):
        self._base_test.get_messages(amount_per_room=5, use_last_seen_control=False)

    @task(2)
    def get_full_messages_room_with_10(self):
        self._base_test.get_messages(amount_per_room=10, use_last_seen_control=False)
