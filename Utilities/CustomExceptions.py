
class UserException(Exception):
    def __init__(self, message='User doesn\'t exists.'):
        super(Exception, self).__init__(message)


class DatabaseException(Exception):
    def __init__(self, message='Database connection error.'):
        super(Exception, self).__init__(message)
