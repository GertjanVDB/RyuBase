from dataclasses import dataclass, asdict
from uuid import uuid4
from pymongo import MongoClient
from db import DBRecord, DBRun, DBUser

from db.db_exceptions import FailedToConnectError, UserAlreadyExistsError
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

def get_user_db():
    client= connect_to_mongo()
    db = client.RyuBaseDB.UsersDB
    if db == None:
        raise FailedToConnectError
    return db

def get_run_db():
    logger.info("Getting Player runs DB")
    client= connect_to_mongo()
    db = client.RyuBaseDB.PlayerRunsDB
    if db == None:
        raise FailedToConnectError
    return db

def _create_runrecord(mongo_doc):
    run_obj = DBRun(run_id=mongo_doc.run_id,
        user_id=mongo_doc.user_id,
        user_name=mongo_doc.user_name,
        run_start=mongo_doc.run_start,
        run_end=mongo_doc.run_end)
    return run_obj

def new_user(user:DBUser):
    user_db = get_user_db()
    existing = list(user_db.find({"user_id":f"{user.user_id}"}))
    if existing:
        raise UserAlreadyExistsError
    else:
        user_db.insert_one(asdict(user))
        
    

def get_user(user_id):
    raise NotImplementedError


def new_run(user_id, user_name):
    run_id = uuid4()
    import datetime
    run_start = str(datetime.datetime.now())
    
    new_run = DBRun(run_id,user_id,user_name,run_start,"")
    return new_run

def write_run(run:DBRun):
    collection = get_run_db()
    collection.insert_one(asdict(run))


def find_run_id(run_id):
    logger.info("Looking for id: %s" % run_id)
    run_db = get_run_db()
    found = list(run_db.find({'course_id':f"{run_id}"}))
    
    logger.info("found: %s" % list(found))
    logger.info(run_db)
    # todo: find run by id, return a run record if found
    if found:
        return _create_runrecord(found)
    return found

