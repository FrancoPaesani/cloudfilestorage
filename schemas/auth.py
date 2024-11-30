from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel
from sqlmodel import Field


class UserRegister(BaseModel):
    user: str
    name: str
    email: str
    password: str
    max_storage_size_mb: Decimal = Field(decimal_places=2)

class UserResponse(BaseModel):
    id: int
    user: str
    name: str
    email: str
    password: str
    max_storage_size_mb: Decimal = Field(decimal_places=2)

class UserLogin(BaseModel):
    user: str
    password: str

class UserSessionResponse(BaseModel):
    jwt: str
    expires_date: datetime