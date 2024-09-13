from fastapi import Depends
import psycopg2
from src.features.hands.data.services.hand_service import HandService
from src.features.hands.data.repositories.player_repo import PlayerRepository
from src.features.hands.data.repositories.hand_repo import HandRepository
from src.features.hands.data.repositories.action_repo import ActionRepository
from src.core.database.connection import get_db_connection


def get_player_repository(db_conn: psycopg2.extensions.connection = Depends(get_db_connection)) -> PlayerRepository:
    return PlayerRepository(db_conn)

def get_action_repository(db_conn: psycopg2.extensions.connection = Depends(get_db_connection)) -> ActionRepository:
    return ActionRepository(db_conn)

def get_hand_repository(db_conn: psycopg2.extensions.connection = Depends(get_db_connection), action_repo: ActionRepository = Depends(get_action_repository), player_repo: PlayerRepository = Depends(get_player_repository)) -> HandRepository:
    return HandRepository(db_conn, action_repo, player_repo)

def get_hand_service(hand_repo: HandRepository = Depends(get_hand_repository), action_repo: ActionRepository = Depends(get_action_repository), player_repo: PlayerRepository = Depends(get_player_repository)) -> HandService:
    return HandService(action_repo, hand_repo, player_repo)

