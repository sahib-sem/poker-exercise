from fastapi import Depends, FastAPI

from src.features.hands.domain.entities.hand import Hand
from src.features.hands.data.services.hand_service import HandService
from src.features.hands.presentation.schema.hand import CreateHand
from src.features.hands.data.dependacies import get_hand_service
from src.core.database.create_tables import create_tables
from src.features.hands.presentation.routes.route import router

from .core.database.connection import get_db_connection


create_tables()
app = FastAPI()

app.include_router(router)
