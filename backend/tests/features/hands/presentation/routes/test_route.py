import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.features.hands.data.services.hand_service import HandService
from src.features.hands.presentation.schema.action import ActionCreate, ActionResponse
from src.features.hands.presentation.schema.hand import CreateHand, HandStatusEnum
from uuid import uuid4

client = TestClient(app)

ID = str(uuid4())
NEXT_INVALID_MOVES = ["fold", "all_in"]

class MockHandService:
    def __init__(self):
       
        pass

    def get_hands_by_status(self, status: bool):
        return [{"id": ID, "status": "completed"}]

    def start_game(self, hand_data: CreateHand):
        return {"id": ID, "status": "in_progress"}

    def add_action(self, action_data: ActionCreate):
        if action_data.action_type not in NEXT_INVALID_MOVES:
            return ActionResponse(
                success=True,
                message="Action added",
                next_actor=2,
                current_actor=1,
                possible_moves=["call", "raise"],
                maximum_bet=500,
                game_ended=False,
                dealt_cards=[],
                pot_amount=1000,
            )
        return ActionResponse(success=False, message="Invalid action")

@pytest.fixture(autouse=True)
def mock_hand_service(mocker):

    mocker.patch.object(HandService, "__new__", return_value=MockHandService())

def test_get_hands():

    hand_id = ID
    response = client.get("/api/v1/hands", params={"status": "completed"})
    assert response.status_code == 200
    assert response.json() == [{"id": hand_id, "status": "completed"}]

def test_create_hand():
    # The mock returns a hardcoded UUID and status
    hand_id = ID
    response = client.post(
        "/api/v1/hands",
        json={"number_of_players": 6, "stack_size": 10000},
    )
    assert response.status_code == 200
    assert response.json() == {"id": hand_id, "status": "in_progress"}

def test_add_action():
    # The mock returns a fixed response for valid actions
    hand_id = ID
    response = client.post(
        f"/api/v1/hands/{hand_id}/actions",
        json={
            "amount": 100,
            "raise_amount": 0,
            "hand_id": hand_id,
            "action_type": "call",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "Action added",
        "next_actor": 2,
        "current_actor": 1,
        "possible_moves": ["call", "raise"],
        "maximum_bet": 500,
        "game_ended": False,
        "dealt_cards": [],
        "pot_amount": 1000,
    }

def test_add_action_invalid():
    hand_id = ID
    response = client.post(
        f"/api/v1/hands/{hand_id}/actions",
        json={
            "amount": 0,  
            "raise_amount": 0,
            "hand_id": hand_id,
            "action_type": "fold",
        },
    )
    assert response.status_code == 400
    assert response.json() == {"detail": "Invalid action"}
