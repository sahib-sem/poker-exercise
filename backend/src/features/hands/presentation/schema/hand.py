from enum import Enum

from pydantic import BaseModel, Field


class HandStatusEnum(str, Enum):
    completed = "completed"
    in_progress = "in_progress"


class HandBase(BaseModel):
    number_of_players: int = Field(
        default=6, ge=3, le=10, description="the number of players in the hand"
    )
    stack_size: int = Field(
        default=10000,
        ge=100,
        description="the initial stack size for each player",
    )


class CreateHand(HandBase):
    pass
