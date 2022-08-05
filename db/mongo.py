from pymongo import MongoClient
from db import DBRecord
from db_exceptions import FailedToConnectError

from logging import getLogger
logger = getLogger("dbmongo")



class MongoRecord:
    def __init__(self, rec:DBRecord):
        logger.info("Created MongoRecord from DBRecord %s" % rec)
        

def write_to_mongo(record:MongoRecord):
    
    logger.info("Writing to mongodb")


def connect_to_mongo()->MongoClient:
    logger.info("Connecting to mongodb")
    from os import environ
    mongo_uri = environ.get("DB_RESOURCE")
    client = MongoClient(mongo_uri)
    assert client

    return client

def get_run_db(client:MongoClient):
    logger.info("Getting Player runs DB")
    db = client.RyuBaseDB.PlayerRunsDB
    if not db:
        raise FailedToConnectError
    return db


def find_run_id(run_id):
    logger.info("Looking for id: %s" % run_id)
    run_db = get_run_db()
    

