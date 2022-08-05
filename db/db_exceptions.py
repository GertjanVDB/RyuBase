class FailedToConnectError(Exception):
    """Raised when a DB connection error occurs"""

class UserAlreadyExistsError(Exception):
    """Raises if DB already has a user with given id"""