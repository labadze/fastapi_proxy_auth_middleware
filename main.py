from typing import Union, Dict

from fastapi import FastAPI
from fastapi.params import Cookie
from starlette.middleware.cors import CORSMiddleware

from api import auth_manager
from core.database import database

app = FastAPI()

origins = ['http://localhost:3000', 'http://127.0.0.1:3000',
           'https://localhost:3000', 'https://127.0.0.1:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=["*"],
)

app.include_router(auth_manager.router)


@app.get("/")
async def root() -> dict[str, Union[str, None, bool]]:
    return {
        "session_key": 'session_key',
        "success": True
    }


@app.on_event("startup")
async def connect_db():
    await database.connect()


@app.on_event("shutdown")
async def connect_db():
    await database.disconnect()
