from pydantic import BaseModel, typing


class User(BaseModel):
    id: str
    user_name: str
    ext_id: str
    display_name: str
    roles: list[str]
    is_active: bool


class JWTProperties(BaseModel):
    user_id: str
    user_role: str
    audience: str
    expires_in: int = 60 * 8
    access_token: str


class InsertArtefactSchema(BaseModel):
    user_id: str
    is_destroyed: bool
    session_token: str
    access_token: str


class DestroyTokenBodySchema(BaseModel):
    access_token: str


class DestroyTokenInsertSchema(BaseModel):
    user_id: str
    token_value: str
    ext_id: str


class ItemInsertSchema(BaseModel):
    entry_value: str
    is_active: bool
    rate: int
    carma: float
    user_id: str


class ItemUpdateSchema(BaseModel):
    entry_value: str
    is_active: bool
    rate: int
    carma: float
    user_id: str
    item_id: str


class ItemResponseCollectionBase(BaseModel):
    id: str
    created_at: typing.Any
    updated_at: typing.Any
    entry_value: str
    is_active: bool
    rate: int
    carma: float
    user_id: str


class ItemBodySchema(BaseModel):
    entry_value: str
    is_active: bool
    rate: int
    carma: float


class SuccessResponseSchema(BaseModel):
    success: bool
    message: str

