from pydantic import BaseModel


class JWTProperties(BaseModel):
    user_id: str
    user_role: str
    audience: str
    expires_in: int = 60 * 8