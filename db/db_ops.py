import typing

from core.database import database
from core.schemas import InsertArtefactSchema


async def insert_authorization_artefact(data: InsertArtefactSchema) -> str:
    query = """INSERT INTO authorization_artefacts (user_id, is_destroyed, session_token, access_token)
                values (:user_id, :is_destroyed, :session_token, :access_token) RETURNING id;"""
    values = {
        "user_id": data.user_id,
        "is_destroyed": data.is_destroyed,
        "session_token": data.session_token,
        "access_token": data.access_token
    }
    result = await database.execute(query=query, values=values)
    return result


async def fetch_authorization_artefact_by_access_token(access_token: str) -> typing.Any:
    query = """SELECT * FROM authorization_artefacts WHERE access_token = :access_token LIMIT 1"""
    values = {
        "access_token": access_token
    }
    result = await database.execute(query=query, values=values)
    return result


async def fetch_authorization_artefact_by_session_token(session_token: str) -> typing.Any:
    query = """SELECT * FROM authorization_artefacts WHERE session_token = :session_token LIMIT 1"""
    values = {
        "session_token": session_token
    }
    result = await database.execute(query=query, values=values)
    return result


async def fetch_authorization_artefact_by_ext_id(ext_id: str, session_token: str) -> typing.Any:
    query = """SELECT user_id, is_destroyed, access_token FROM authorization_artefacts WHERE user_id = :ext_id 
    AND session_token = :session_token """
    values = {
        "ext_id": ext_id,
        "session_token": session_token
    }
    result = await database.fetch_one(query=query, values=values)
    return result


async def make_authorization_artefact_dead(artefact_id: str) -> None:
    query = """update authorization_artefacts set is_destroyed = :is_destroyed where id = :artefact_id;"""
    values = {
        "is_destroyed": True,
        "artefact_id": artefact_id,
    }
    await database.execute(query=query, values=values)
