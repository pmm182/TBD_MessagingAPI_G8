from exceptions import AppError


class RoomNotFoundError(AppError):

    def __init__(self, room_id: str):
        super().__init__(status_code=404, msg=f'Room {room_id} not found')


class NoSuchMemberFound(AppError):

    def __init__(self, username: str):
        super().__init__(status_code=404, msg=f'User {username} not found in any room')


class MemberNotInRoom(AppError):

    def __init__(self, username: str, room_id: str):
        super().__init__(status_code=403, msg=f'User {username} not in room {room_id}')


class InvalidDataError(AppError):

    def __init__(self):
        super().__init__(status_code=400, msg=f'Invalid data passed as parameter')
