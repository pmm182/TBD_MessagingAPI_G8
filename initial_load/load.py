from queue import Queue, Empty
from threading import Thread

import requests


class UserLoad(Thread):

    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue
        self.exception_happened = False

    def run(self) -> None:
        while True:
            try:
                route, user_ = self._queue.get(timeout=1)
                response = requests.put(route, json={'username': user_})
                if response.status_code != 200:
                    self.exception_happened = True
                    raise Exception(response.json())
            except Empty:
                break


class RoomLoad(Thread):

    def __init__(self, queue: Queue):
        super().__init__()
        self._queue = queue
        self.exception_happened = False
        self.user_room_per_amount = {}

    def run(self) -> None:
        while True:
            try:
                route, name_, users_ = self._queue.get(timeout=1)
                response = requests.put(route, json={'name': name_, 'members': users_})
                if response.status_code != 200:
                    self.exception_happened = True
                    raise Exception(response.json())
                room_id = response.json()['room_id']
                amount_in_room = str(len(users_))
                if amount_in_room not in self.user_room_per_amount:
                    self.user_room_per_amount[amount_in_room] = {}
                for user in users_:
                    if user not in self.user_room_per_amount[amount_in_room]:
                        self.user_room_per_amount[amount_in_room][user] = []
                    self.user_room_per_amount[amount_in_room][user].append(room_id)
            except Empty:
                break


def _perform_load(queue_: Queue, worker_class, worker_amount: int = 30):
    workers = []
    for __ in range(worker_amount):
        worker = worker_class(queue_)
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()
        if worker.exception_happened:
            raise Exception('Error loading!')
    return workers


if __name__ == '__main__':
    # Creating users
    queue = Queue()
    with open('users.txt') as f:
        for line in f.readlines():
            username = line.strip()
            if username:
                queue.put((f'http://localhost:8080/users', username))
    _perform_load(queue_=queue, worker_class=UserLoad)
    print('Created users')

    # Create room
    queue = Queue()
    with open('rooms.txt') as f:
        i = 0
        for line in f.readlines():
            if line.strip():
                users = [u.strip() for u in line.split(',')]
                queue.put((f'http://localhost:8080/rooms', f'Test room {i}', users))
    workers = _perform_load(queue_=queue, worker_class=RoomLoad)
    print('Created rooms')
