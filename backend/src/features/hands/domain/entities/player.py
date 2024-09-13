from dataclasses import dataclass


@dataclass
class Player:
    hand_id: str
    player_idx: int 
    initial_stack_size: int
    hole_cards: str
    winnings: int = 0