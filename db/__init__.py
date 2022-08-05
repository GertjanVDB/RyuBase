"""Interface for storing information in the database"""

from logging import getLogger

logger = getLogger()

logger.info("Importing DB")

class DBRecord:
    course_id=None
    ryu_lives_at_start=None
    ryu_lives_at_end=None
    

