from dataclasses import dataclass, field
from typing import List, Optional
import uuid
from src.features.hands.domain.entities.action import Action


@dataclass
class Hand:
    hole_cards: List[str] = field(default_factory=list) 
    actions: List[Action] = field(default_factory=list) 
    id: str = ''
    has_ended: bool = False
    number_of_players: int = 6
    small_blind_idx: int = 2
    big_blind_idx: int = 3
    dealer_idx: int = 1
    stack_size: int = 10000
    big_blind_size: int = 40
    
    players_stack: List[int] = field(default_factory=list)

    def __post_init__(self):
        self.players_stack = [self.stack_size] * self.number_of_players


  