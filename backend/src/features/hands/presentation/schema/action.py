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

class ActionResponse(BaseModel):
    success: bool = False
    message: str = ''
    next_actor: int | None = None
    current_actor: int | None = None
    possible_moves: list[ActionEnum] = []
    maximum_bet: int = 0
    game_ended: bool = False
    street_idx: int | None = None
    card_string: str = ''
    pot_amount: int = 0





    



