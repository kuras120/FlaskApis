
class UserException(Exception):
    def __init__(self, message='Account error, please log in again.'):
        super(Exception, self).__init__(message)


class DatabaseException(Exception):
    def __init__(self, message='Database connection error.'):
        super(Exception, self).__init__(message)
