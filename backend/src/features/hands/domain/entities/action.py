from dataclasses import dataclass



@dataclass
class Action:
    
    hand_id: str 
    action_type: str  
    id:str = ''
    amount: int = 0  
    card_string: str = ""  