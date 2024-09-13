from pydantic import BaseModel, model_validator, ValidationError
from typing import List

class HandBase(BaseModel):
    number_of_players: int = 6
    small_blind_idx: int = 2
    big_blind_idx: int = 3
    stack_size: int = 10000

class CreateHand(HandBase):
    pass
