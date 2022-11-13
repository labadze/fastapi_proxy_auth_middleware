import uuid

import sqlalchemy
from sqlalchemy import sql, DateTime, Boolean, String
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserRole(Base):
    __tablename__ = 'user_roles'
    id = uuid.UUID = sqlalchemy.Column(postgresql.UUID(as_uuid=True), primary_key=True, default=uuid.uuid4,
                                       server_default=sql.func.gen_random_uuid(), nullable=False)

    created_at = sqlalchemy.Column(DateTime(timezone=True), server_default=sql.func.now())
    updated_at = sqlalchemy.Column(DateTime(timezone=True), onupdate=sql.func.now())
    is_enabled = sqlalchemy.Column(Boolean, default=False)

    entry_value = sqlalchemy.Column(String(128), nullable=False, unique=True)
