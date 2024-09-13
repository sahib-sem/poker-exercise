from dataclasses import dataclass
from typing import Optional


@dataclass
class Action:
    
    hand_id: str
    player_idx: int  
    stack_idx: int  
    action_type: str  
    id:str = ''
    amount: Optional[int] = 0  
    card_string: Optional[str] = ""  