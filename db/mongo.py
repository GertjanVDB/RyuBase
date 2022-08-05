import pymongo
from db import DBRecord

from logging import getLogger
logger = getLogger()


class MongoRecord:
    def __init__(self, rec:DBRecord):
        logger.info("Created MongoRecord from DBRecord %s" % rec)
        

def write_to_mongo(record:MongoRecord):
    logger.info("Writing to mongodb")

def connect_to_mongo():
    logger.info("Connecting to mongodb")

