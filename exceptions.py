class AppError(Exception):

    def __init__(self, status_code: int, msg: str = None):
        super().__init__(msg)
        self.msg = msg
        self.status_code = status_code
