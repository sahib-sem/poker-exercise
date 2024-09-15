from dataclasses import dataclass, field
from typing import List

from src.features.hands.domain.entities.action import Action

from .player import Player


@dataclass
class Hand:

    id: str = ""
    has_ended: bool = False
    number_of_players: int = 6
    small_blind_idx: int = 3
    big_blind_idx: int = 4
    dealer_idx: int = 2
    stack_size: int = 10000
    big_blind_size: int = 40
    actions: List[Action] = field(default_factory=list)
    players: List[Player] = field(default_factory=list)
