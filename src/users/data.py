

class User:

    def __init__(self, username: str, name: str):
        self._username = username
        self._name = name

    @property
    def username(self):
        return self._username

    @property
    def name(self):
        return self._name

    def to_dict(self):
        return {'username': self._username, 'name': self._name}
