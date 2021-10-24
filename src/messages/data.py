import datetime


class Message:

    def __init__(self, room_id: str, from_: str, message: str, date: datetime.datetime):
        self._room_id = room_id
        self._from = from_
        self._message = message
        self._date = date

    @property
    def room_id(self):
        return self._room_id

    @property
    def from_(self):
        return self._from

    @property
    def message(self):
        return self._message

    @property
    def date(self):
        return self._date

    def to_dict(self, message_info_only: bool = True):
        result = {'from': self._from, 'message': self._message, 'date': self._date.isoformat()}
        if not message_info_only:
            result['room_id'] = self._room_id
        return result

