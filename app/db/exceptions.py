class UserNotFoundException(Exception):
    pass


class UsernameAlreadyExistsException(Exception):
    pass


class EmailAlreadyExistsException(BaseException):
    pass
