from enum import Enum

from pydantic import BaseModel, Field


class ActionEnum(str, Enum):
    FOLD = "fold"
    CHECK = "check"
    CALL = "call"
    BET = "bet"
    RAISE = "raise"
    ALLIN = "all_in"


class ActionBase(BaseModel):
    amount: int = Field(default=0, ge=0)
    raise_amount: int = Field(default=0, ge=0)
    hand_id: str
    action_type: ActionEnum


class ActionCreate(ActionBase):
    pass


class DealtCards(BaseModel):
    street_idx: int
    card_string: str


class ActionResponse(BaseModel):
    success: bool = False
    message: str = ""
    next_actor: int | None = None
    current_actor: int | None = None
    possible_moves: list[ActionEnum] = []
    maximum_bet: int = 0
    game_ended: bool = False
    dealt_cards: list[DealtCards] = []
    pot_amount: int = 0
