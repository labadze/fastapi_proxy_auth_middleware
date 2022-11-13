"""
    Insert new artefact
"""
from core.database import database
from core.schemas import InsertArtefactSchema


async def insert_authorization_artefact(data: InsertArtefactSchema):
    query = """INSERT INTO authorization_artefacts (user_id, is_destroyed, session_token, access_token)
                values (:user_id, :is_destroyed, :session_token, :access_token) RETURNING id;"""
    values = {
        "user_id": data.user_id,
        "is_destroyed": data.is_destroyed,
        "session_token": data.session_token,
        "access_token": data.access_token
    }
    await database.execute(query=query, values=values)


async def set_session_token_to_artefact(artefact_id: str, session_token):
    query = """update authorization_artefacts set session_token = :session_token where id = :artefact_id;"""
    values = {
        "session_token": session_token,
        "artefact_id": artefact_id,
    }
    await database.execute(query=query, values=values)


async def fetch_authorization_artefact(artefact_id: str):
    query = """SELECT * FROM authorization_artefacts WHERE id = :artefact_id"""
    values = {
        "artefact_id": artefact_id
    }
    result = await database.execute(query=query, values=values)
    return result


async def make_authorization_artefact_dead(artefact_id: str):
    query = """update authorization_artefacts set is_destroyed = :is_destroyed where id = :artefact_id;"""
    values = {
        "is_destroyed": True,
        "artefact_id": artefact_id,
    }
    await database.execute(query=query, values=values)
