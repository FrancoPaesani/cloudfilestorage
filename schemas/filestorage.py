from decimal import Decimal
from pydantic import BaseModel


#TODO: validate file_path and file_name with regex
class FileInfo(BaseModel):
    file_path: str
    file_name: str
    file_size: float
    file_extension: str
    file_content: bytes

class UserStats(BaseModel):
    user_id: int
    cloud_provider_id: int
    cloud_provider_name: str
    occupied_size: Decimal