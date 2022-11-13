import uuid

import sqlalchemy
from sqlalchemy import sql, DateTime, Boolean, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class AuthorizationArtefacts(Base):
    __tablename__ = 'authorization_artefacts'
    id = uuid.UUID = sqlalchemy.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                       server_default=sql.func.gen_random_uuid(), nullable=False)

    created_at = sqlalchemy.Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = sqlalchemy.Column(DateTime(timezone=True), onupdate=sql.func.now())
    user_id = sqlalchemy.Column(String(512), nullable=False, unique=False)
    is_destroyed = sqlalchemy.Column(Boolean, default=False)
    session_token = sqlalchemy.Column(String(2048), nullable=False, unique=True)
    access_token = sqlalchemy.Column(String(2048), nullable=False, unique=True)
