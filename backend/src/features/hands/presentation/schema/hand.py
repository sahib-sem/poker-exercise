from pydantic import BaseModel, model_validator, ValidationError
from typing import List

class HandBase(BaseModel):
    num_players: int = 6
    small_blind_idx: int = 2
    big_blind_idx: int = 3
    stack_size: int = 10000

    @model_validator(pre=True)
    def validate_indices(cls, values):
        num_players = values.get('num_players')
        small_blind_idx = values.get('small_blind_idx')
        big_blind_idx = values.get('big_blind_idx')

        for idx in [small_blind_idx, big_blind_idx]:
            if not (0 <= idx < num_players):
                raise ValueError(f'Index {idx} is out of range for num_players {num_players}')

        
        
        if not (small_blind_idx + 1) % num_players == big_blind_idx:
            raise ValueError('Indices must be adjacent and in the order: small_blind_idx, big_blind_idx')

        return values

class CreateHand(HandBase):
    pass
