"""Interface for storing information in the database"""

from logging import getLogger
from dataclasses import dataclass
from enum import Enum
from uuid import uuid4
from db.data_structures import DBUser, DBUserCollection, DBLevelAttempt
from db.db_exceptions import UserDoesNotExistError, CollectionNotOwnerByUserError

logger = getLogger("db")

logger.info("Importing DB")


class DBTypes(Enum):
    MONGO = 0


DBTYPE = DBTypes.MONGO


# Player stuff
def create_user(maker_id: str, maker_name: str):
    if DBTYPE == DBTypes.MONGO:
        # create mongo db user
        import db.mongo as mongo

        new_user = DBUser(maker_id=maker_id,
                          maker_name=maker_name,
                          user_collections=[])
        mongo.add_user(new_user)
        logger.info("Created new user : %s" % new_user)
    else:
        raise NotImplementedError

def get_user_by_id(maker_id)->DBUser:
    if DBTYPE == DBTypes.MONGO:
        import db.mongo as mongo
        return mongo.get_user_by_id(maker_id)


# Collections stuff
def create_run(run_name, maker_id):
    if DBTYPE == DBTypes.MONGO:
        import db.mongo as mongo
        new_collection = DBUserCollection(collection_id=str(uuid4()), collection_name=run_name)
        mongo.add_user_collection(new_collection)
        user = mongo.get_user_by_id(maker_id)
        if not user:
            raise UserDoesNotExistError()

        user.user_collections.append(new_collection.id)

def get_collection_by_id(collection_id) -> DBUserCollection:
    if DBTYPE == DBTypes.MONGO:
        import db.mongo as mongo
        col = mongo.get_user_collection(collection_id)
        return col

def create_level_attempt(course_id: str, maker_id: str, run_id: str,
                         attempt_result, result_context: str,
                         lives_gained: int, lives_lost: int) -> None:
    attempt = DBLevelAttempt(course_id, maker_id, run_id,
                             attempt_result, result_context,
                             lives_gained, lives_lost)

    if DBTYPE == DBTypes.MONGO:
        import db.mongo as mongo

        # check if maker and run exist
        user = mongo.get_user_by_id(maker_id)
        if not user:
            raise UserDoesNotExistError()
        user_cols = mongo.get_user_collection_ids(maker_id)
        if run_id not in user_cols:
            raise CollectionNotOwnerByUserError()

        mongo.add_attempt(attempt)
