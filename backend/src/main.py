from fastapi import  FastAPI
from src.core.database.create_tables import create_tables
from src.features.hands.presentation.routes.route import router
from fastapi.middleware.cors import CORSMiddleware


create_tables()

app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(router)
