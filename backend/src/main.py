from fastapi import Depends, FastAPI

from src.features.hands.domain.entities.hand import Hand
from .core.database.connection import get_db_connection

app = FastAPI(dependencies=[Depends(get_db_connection)])

print(Hand())

app.get('/')
def health():
    # print(Hand()) 
    return {"message": "api working fine"}