from pydantic import BaseModel


class JWTProperties(BaseModel):
    user_id: str
    user_role: str
    audience: str
    expires_in: int = 60 * 8


class InsertArtefactSchema(BaseModel):
    user_id: str
    is_destroyed: bool
    session_token: str
    access_token: str
