from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from config.database import CFS_METADATA


class CloudProvider(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "CloudProvider"

    id: int | None = Field(default=None, primary_key=True)
    name: str


# TODO: esto va con un TRIGGER AFTER_INTER DENTRO DE USERFILES.
# Queda el modelo para select nomas
class UserStorage(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "UserStorage"

    user_id: int = Field(primary_key=True, foreign_key="User.id")
    cloud_provider_id: int = Field(primary_key=True, foreign_key="CloudProvider.id")
    occupied_size: Decimal = Field(decimal_places=6)


class UserFiles(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "UserFiles"

    user_id: int = Field(primary_key=True, foreign_key="User.id")
    cloud_provider_id: int = Field(primary_key=True, foreign_key="CloudProvider.id")
    file_path: str
    file_name: str
    file_extension: str
    file_size: Decimal = Field(decimal_places=6)
    upload_date: datetime
