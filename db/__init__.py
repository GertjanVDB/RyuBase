"""Interface for storing information in the database"""


from logging import getLogger
from dataclasses import dataclass
import re

logger = getLogger("db")

logger.info("Importing DB")

def get_run_by_id(dbrun_id):
    import db.mongo as mongo
    mongo_run = mongo.find_run_id(dbrun_id)

def create_run(user_id, user_name):
    import db.mongo as mongo
    new_run = mongo.new_run(user_id, user_name)
    mongo.write_run(new_run)

def create_user(user_id, user_name):
    import db.mongo as mongo
    user = DBUser(str(user_id), user_name)

    mongo.new_user(user)
 
@dataclass(repr=True)
class DBUser:
    user_id:str
    user_name:str

@dataclass(repr=True)
class DBRecord:
    run_id:str
    course_id:str
    ryu_lives_at_start:int
    ryu_lives_at_end:int
    
@dataclass(repr=True)
class DBRun:
    run_id:str
    user_id:str
    user_name:str
    run_start:str
    run_end:str

