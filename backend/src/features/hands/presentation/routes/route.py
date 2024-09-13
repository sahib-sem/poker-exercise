from fastapi import APIRouter, Depends

from src.features.hands.presentation.schema.action import ActionCreate, ActionResponse
from src.features.hands.presentation.schema.hand import CreateHand
from src.features.hands.data.services.hand_service import HandService
from src.features.hands.data.dependacies import get_hand_service

router = APIRouter()

@router.get('/hands')
def get_hands(status: bool, hand_service: HandService = Depends(get_hand_service)):
    hands = hand_service.get_hands_by_status(status)
    return hands

@router.post('/hands')
def create_hand(hand_data: CreateHand, hand_service: HandService = Depends(get_hand_service)):
    hand = hand_service.start_game(hand_data)
    return hand

@router.post('/hands/{hand_id}/actions', response_model=ActionResponse)
def add_action(hand_id: str, action: ActionCreate, hand_service: HandService = Depends(get_hand_service)):
    action_response = hand_service.add_action(action)
    return action_response