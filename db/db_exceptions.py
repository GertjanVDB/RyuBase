class FailedToConnectError(Exception):
    """Raised when a DB connection error occurs"""

class UserAlreadyExistsError(Exception):
    """Raises if DB already has a user with given id"""

class UserDoesNotExistError(Exception):
    """Raiss if a user does not exist"""

class CollectionDoesNotExistError(Exception):
    """Raises if collection does not exist"""

class CollectionNotOwnerByUserError(Exception):
    """Raises when looking for a collection not owned by user"""

class FailedToCreateUserError(Exception):
    """Raises if a user creation failed"""