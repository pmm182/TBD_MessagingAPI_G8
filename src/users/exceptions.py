from src.exceptions import AppError


class DuplicateUserError(AppError):

    def __init__(self, username: str):
        super().__init__(status_code=409, msg=f'User {username} already exists')


class UserNotFoundError(AppError):

    def __init__(self, username: str):
        super().__init__(status_code=404, msg=f'User {username} not found')
