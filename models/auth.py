from datetime import datetime
from decimal import Decimal
from sqlmodel import Field, SQLModel

from config.database import CFS_METADATA


class User(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "User"

    id: int | None = Field(default=None, primary_key=True)
    user: str
    name: str
    email: str
    password: str
    max_storage_size_mb: Decimal = Field(decimal_places=2)
    created_date: datetime = Field(default_factory=datetime.now)
    is_admin: bool = Field(default=False)

class UserSession(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "UserSession"

    user_id: int | None = Field(default=None, primary_key=True, foreign_key="User.id")
    jwt: str
    expires_date: datetime