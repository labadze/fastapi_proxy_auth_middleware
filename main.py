from typing import Union

from fastapi import FastAPI
from fastapi.params import Cookie
from starlette.middleware.cors import CORSMiddleware

from api import auth_manager
from core.database import database
from core.utils import decode_back_end_token

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
    await database.connect()
    token = "eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJOSVY4WHl2WXN0WG1TTFlaaFZ1OEdhZnVFWUhFNnVyMGF4c0NFT1Q2NkZ3In0.eyJleHAiOjE2NjgzMzM2MTksImlhdCI6MTY2ODMzMzMxOSwiYXV0aF90aW1lIjoxNjY4MzMzMzE5LCJqdGkiOiJiNTQ1YTZmOC0wMjZjLTQ2NTEtYjc2NS01NGIxNWRlOWU4NWUiLCJpc3MiOiJodHRwOi8vbG9jYWxob3N0OjgwODAvYXV0aC9yZWFsbXMvZmFweSIsImF1ZCI6ImFjY291bnQiLCJzdWIiOiI5MDk4YzNiMy04MWYxLTQ2MTMtYWI3Yy02MTdjNzNjZmJjOWQiLCJ0eXAiOiJCZWFyZXIiLCJhenAiOiJmYXB5Iiwic2Vzc2lvbl9zdGF0ZSI6ImVlY2EyMGI1LTdiMWYtNGRhNy1iNTRkLTRiNTM1YjNlM2NlMiIsImFjciI6IjEiLCJyZWFsbV9hY2Nlc3MiOnsicm9sZXMiOlsiZGVmYXVsdC1yb2xlcy1mYXB5Iiwib2ZmbGluZV9hY2Nlc3MiLCJ1bWFfYXV0aG9yaXphdGlvbiJdfSwicmVzb3VyY2VfYWNjZXNzIjp7ImFjY291bnQiOnsicm9sZXMiOlsibWFuYWdlLWFjY291bnQiLCJtYW5hZ2UtYWNjb3VudC1saW5rcyIsInZpZXctcHJvZmlsZSJdfX0sInNjb3BlIjoicHJvZmlsZSBlbWFpbCIsInNpZCI6ImVlY2EyMGI1LTdiMWYtNGRhNy1iNTRkLTRiNTM1YjNlM2NlMiIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJwcmVmZXJyZWRfdXNlcm5hbWUiOiJhZG9yYW11cyJ9.YX1LuYBrFxYia9jnYBA86a0JRbNSXCR1jadxOjhlxOABGn-c2tMdmo0_5QXoSVepxjQX8MzBrB4nRQnLsEo6aqklDxxRAE8aTd7eCQ6AsTZ8HAHrGIcMAeoeRxBsnnDqipQcPtWeV1735nydmH_C2ezapSoRZGQi129T09dlo76eA8WlI22978FOklGeKlEONx4qyZ0A8Umn_6PMNFK8aN-YRSVYpbSgDP1xvgZvas9kagdB_0ynSLc5njbIE0LLkJjNPYrwSbADjCirsnDn6N_Pnr_mqC9Y7EfH7ZcveJP8sAxrxCwB9ylFgNZYHdfk-sCAKBMg4ZzgBN89VnkgeA"
    await decode_back_end_token(encoded=token)


@app.on_event("shutdown")
async def connect_db():
    await database.disconnect()
