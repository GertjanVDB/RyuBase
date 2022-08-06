from dataclasses import dataclass
from dataclasses import asdict
from dacite import from_dict
from enum import Enum

class AttemptResult(Enum):
    DEATH = 0
    COMPLETE = 1
    SKIP = 2

@dataclass(repr=True)
class DBUser:
    maker_id:str
    maker_name:str
    user_collections:list[str]

    def as_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(dct):
        return from_dict(DBUser, dct)



@dataclass(repr=True)
class DBLevelAttempt:
    course_id:str
    maker_id:str
    collection_id:str

    attempt_result:AttemptResult
    result_context:str

    lives_gained:int = 0
    lives_lost:int = 0

    def as_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(dct):
        return from_dict(DBLevelAttempt, dct)

@dataclass(repr=True)
class DBUserCollection:
    collection_id:str
    collection_name:str
    def as_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(dct):
        return from_dict(DBUserCollection, dct)




