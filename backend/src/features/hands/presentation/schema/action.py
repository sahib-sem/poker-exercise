from enum import Enum
from pydantic import BaseModel

class ActionEnum(str, Enum):
    FOLD = 'fold'
    CHECK = 'check'
    CALL = 'call'
    BET = 'bet'
    RAISE = 'raise'
    ALLIN = 'all_in'

class ActionBase(BaseModel):
    amount:int = 0
    hand_id: str
    action_type:ActionEnum

class ActionCreate(ActionBase):
    pass


    



