"""Interface for storing information in the database"""


from logging import getLogger
from dataclasses import dataclass
import re

logger = getLogger()

logger.info("Importing DB")

def get_run_by_id(run_id):
    import mongo
    mongo.find_run_id(run_id)
    
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

