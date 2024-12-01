from datetime import datetime
from decimal import Decimal

from sqlmodel import Field, SQLModel

from config.database import CFS_METADATA


class CloudProvider(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "CloudProvider"

    id: int | None = Field(default=None, primary_key=True)
    name: str


class UserStorage(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "UserStorage"

    user_id: int = Field(primary_key=True, foreign_key="User.id")
    cloud_provider_id: int = Field(primary_key=True, foreign_key="CloudProvider.id")
    occupied_size: Decimal = Field(decimal_places=6)
    year_month: int


class UserFiles(SQLModel, table=True):
    metadata = CFS_METADATA
    __tablename__ = "UserFiles"

    user_id: int = Field(primary_key=True, foreign_key="User.id")
    cloud_provider_id: int = Field(primary_key=True, foreign_key="CloudProvider.id")
    file_path: str
    file_name: str
    file_extension: str
    file_size: Decimal = Field(decimal_places=6)
    upload_date: datetime = Field(default_factory=datetime.now)
