from typing import List


class Room:

    def __init__(self, members: List[str], name: str = None, id_: str = None):
        self._id = id_
        self._members = members
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def members(self) -> List[str]:
        return self._members

    @property
    def name(self):
        return self._name

    def to_dict(self):
        return {'id': self._id, 'name': self._name, 'members': self._members}
