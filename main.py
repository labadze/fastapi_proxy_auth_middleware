from typing import Union

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import Response, JSONResponse

from api import auth_manager, item_manager, account_manager

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
app.include_router(item_manager.router)
app.include_router(account_manager.router)


@app.get("/")
async def root(response: Response) -> JSONResponse:
    response = JSONResponse(content={
        "success": True
    })
    # response.set_cookie(
    #     key="session_state",
    #     value='deleted',
    #     httponly=True,
    #     secure=True,
    #     samesite='none',
    #     max_age=4,
    #     expires=3,
    #     path='/',
    #     domain=None
    # )
    return response

