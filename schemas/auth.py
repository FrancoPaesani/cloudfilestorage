from datetime import datetime
from decimal import Decimal

from email_validator import EmailNotValidError, validate_email
from pydantic import BaseModel, field_validator
from sqlmodel import Field


class UserRegister(BaseModel):
    user: str = Field(max_length=30, min_length=3)
    name: str = Field(max_length=50)
    email: str = Field(max_length=350)
    password: str

    @field_validator("email")
    def valid_mail(cls, v):
        try:
            validate_email(v, check_deliverability=True)
            return v
        except EmailNotValidError as e:
            raise ValueError("email field: " + str(e))

    @field_validator("password")
    def valid_password(cls, v):
        if len(v) < 8 :
            raise ValueError("password length must have at least 8 characters")
        return v


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
