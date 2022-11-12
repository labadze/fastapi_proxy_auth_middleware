from typing import Union

from fastapi import FastAPI
from fastapi.params import Cookie
from starlette.middleware.cors import CORSMiddleware

from api import auth_manager

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
async def root(session_key: Union[str, None] = Cookie(None)):
    return {
        "session_key": session_key,
        "success": True
    }


@app.on_event("startup")
async def connect_db():
    print("Started")


@app.on_event("shutdown")
async def connect_db():
    print("power off")
