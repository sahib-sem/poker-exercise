from fastapi import Depends
import psycopg2
from src.features.hands.data.repositories.hand_repo import HandRepository
from src.features.hands.data.repositories.action_repo import ActionRepository
from src.core.database.connection import get_db_connection

def get_hand_repository(db_conn: psycopg2.extensions.connection = Depends(get_db_connection)) -> HandRepository:
    return HandRepository(db_conn)

def get_action_repository(db_conn: psycopg2.extensions.connection = Depends(get_db_connection)) -> ActionRepository:
    return ActionRepository(db_conn)
