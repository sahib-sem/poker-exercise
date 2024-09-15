from fastapi import APIRouter, Depends, HTTPException

from src.features.hands.data.dependacies import get_hand_service
from src.features.hands.data.services.hand_service import HandService
from src.features.hands.presentation.schema.action import (
    ActionCreate,
    ActionResponse,
)
from src.features.hands.presentation.schema.hand import (
    CreateHand,
    HandStatusEnum,
)

router = APIRouter()


@router.get("/hands")
def get_hands(
    status: HandStatusEnum,
    hand_service: HandService = Depends(get_hand_service),
):
    hands = hand_service.get_hands_by_status(
        status == HandStatusEnum.completed)
    return hands


@router.post("/hands")
def create_hand(
    hand_data: CreateHand,
    hand_service: HandService = Depends(get_hand_service),
):
    hand = hand_service.start_game(hand_data)
    return hand


@router.post("/hands/{hand_id}/actions", response_model=ActionResponse)
def add_action(
    hand_id: str,
    action: ActionCreate,
    hand_service: HandService = Depends(get_hand_service),
):

    action_response = hand_service.add_action(action)
    if not action_response.success:
        raise HTTPException(status_code=400, detail=action_response.message)
    return action_response
