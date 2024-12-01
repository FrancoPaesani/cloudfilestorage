from decimal import Decimal
import re


from pydantic import BaseModel, field_validator


class FileInfo(BaseModel):
    file_path: str
    file_name: str
    file_size: Decimal
    file_extension: str
    file_content: bytes

    @field_validator("file_path")
    def validate_path(cls, v):
        if v == '':
            return v
        pattern = r'^(/[a-zA-Z0-9]+)+/$'        
        if bool(re.match(pattern, v)):
            return v
        else: 
            raise ValueError("Invalid path")
    
    @field_validator("file_name")
    def validate_name(cls, v):
        pattern = r'^[a-zA-Z0-9]+\.[a-zA-Z0-9]+$'
        if bool(re.match(pattern, v)):
            return v
        else:
            raise ValueError("Invalid name")


class UserStats(BaseModel):
    user_id: int
    cloud_provider_id: int
    cloud_provider_name: str
    occupied_size: Decimal
    year_month: int
