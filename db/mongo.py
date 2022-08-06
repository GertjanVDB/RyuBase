from dataclasses import dataclass, asdict
from uuid import uuid4
import pymongo
from pymongo import MongoClient
from db.data_structures import DBUser, DBUserCollection, DBLevelAttempt
from enum import Enum

from db.db_exceptions import FailedToConnectError, UserAlreadyExistsError, UserDoesNotExistError, \
    FailedToCreateUserError, CollectionDoesNotExistError
from logging import getLogger

logger = getLogger("dbmongo")


class DBCollections(Enum):
    Users = 'UsersDB'
    LevelAttempts = 'LevelAttemptsDB'
    UserCollections = 'UserCollectionsDB'


def connect_to_mongo() -> MongoClient:
    logger.info("Connecting to mongodb")
    from os import environ
    mongo_uri = environ.get("DB_RESOURCE")
    client = MongoClient(mongo_uri)
    assert client

    return client


def get_db(collection: DBCollections) -> pymongo.collection.Collection:
    client = connect_to_mongo()
    db = client.RyuBaseDB  # type: pymongo.collection.Database
    if db == None:
        raise FailedToConnectError

    col = db.get_collection(collection.value)
    return col


# User stuff
def get_user_by_id(maker_id: str) -> DBUser | None:
    """
    Retrieves user data by maker_id

    Args:
        maker_id: Nintendo maker id

    Returns:
        DBUser: db user data

    """
    user_db = get_db(DBCollections.Users)
    existing = list(user_db.find({"maker_id": f"{maker_id}"}))
    if existing:
        user = DBUser.from_dict(existing[0])

        return user
    else:
        return None


def add_user(user: DBUser) -> None:
    """
    Creates a new mongo user

    Args:
        user: DB.User
    Raises:
        UserAlreadyExistsError: On duplicate user
        FailedToCreateUserError: If fails for any reason
    """
    user_db = get_db(DBCollections.Users)
    exists = get_user_by_id(user.maker_id)

    if exists:
        raise UserAlreadyExistsError()
    else:
        try:
            user_db.insert_one(user.as_dict())
        except Exception as ex:
            logger.error(ex)
            raise FailedToCreateUserError(ex)


# Collection stuff


def add_user_collection(user_col: DBUserCollection):
    logger.info("Creating user collection: %s" % user_col.name)
    db = get_db(DBCollections.UserCollections)
    db.insert_one(user_col.as_dict())


def get_user_collection_ids(maker_id: str) -> list[str]:
    logger.info("Getting all collections of user: %s" % maker_id)
    user = get_user_by_id(maker_id)
    if not user:
        raise UserDoesNotExistError()
    return user.user_collections


def get_user_collection(collection_id):
    logger.info("Getting collection: %s" % collection_id)
    db = get_db(DBCollections.UserCollections)
    doc = db.find_one({'collection_id':collection_id})
    if not doc:
        raise CollectionDoesNotExistError()
    return DBUserCollection.from_dict(doc)


# Attempt stuff

def add_attempt(attempt: DBLevelAttempt) -> None:
    collection = get_db(DBCollections.LevelAttempts)
    collection.insert_one(attempt.as_dict())
