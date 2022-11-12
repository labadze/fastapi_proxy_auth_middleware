from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from api import auth_manager

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['POST, PUT, PATCH, GET, DELETE, OPTIONS'],
    allow_headers=["*"],
)

app.include_router(auth_manager.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.on_event("startup")
async def connect_db():
    print("Started")


@app.on_event("shutdown")
async def connect_db():
    print("power off")
