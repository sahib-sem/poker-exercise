from pydantic import BaseModel, model_validator, ValidationError
from typing import List

class HandBase(BaseModel):
    num_players: int = 6
    small_blind_idx: int = 2
    big_blind_idx: int = 3
    dealer_idx: int = 1
    stack_size: int = 10000

    @model_validator(pre=True)
    def validate_indices(cls, values):
        num_players = values.get('num_players')
        small_blind_idx = values.get('small_blind_idx')
        big_blind_idx = values.get('big_blind_idx')
        dealer_idx = values.get('dealer_idx')

        for idx in [small_blind_idx, big_blind_idx, dealer_idx]:
            if not (0 <= idx < num_players):
                raise ValueError(f'Index {idx} is out of range for num_players {num_players}')

        
        indices = sorted([small_blind_idx, big_blind_idx, dealer_idx])
        if not (indices[1] == indices[0] + 1 and indices[2] == indices[1] + 1):
            raise ValueError('Indices must be adjacent and in the order: dealer_idx, small_blind_idx, big_blind_idx')

        
        if not (indices == [dealer_idx, small_blind_idx, big_blind_idx]):
            raise ValueError('Indices must be in the order: dealer_idx, small_blind_idx, big_blind_idx')

        return values

class HandCreate(HandBase):
    pass
