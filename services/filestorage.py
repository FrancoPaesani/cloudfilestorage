from fastapi import HTTPException, UploadFile

from models.filestorage import CloudProvider, UserFiles
from schemas.filestorage import FileInfo
from services.azure import AzureService
from services.cloudProvider import CloudProviderService
from services.dropbox import DropboxService


class FileService:
    def parse_file(self, file_path, file_name, file: UploadFile) -> FileInfo:
        file_content = file.file.read()
        file_size = (file.size / (1<<20))

        file_extension = file_name.split(".")
        file_extension = file_extension[len(file_extension) - 1]

        try:
            file_info = FileInfo(
                file_path=file_path,
                file_name=file_name,
                file_size=file_size,
                file_extension=file_extension,
                file_content=file_content,
            )
        except Exception as e:
            raise HTTPException(status_code=422, detail=str(e))
    
        return file_info 


class StorageService:
    cloud_providers: list[CloudProviderService] = [DropboxService(), AzureService()]

    def __init__(self, providers: CloudProvider):
        self.providers = providers    

    def upload_file(self, file: FileInfo, user_id: int):
        intentos = []
        cloud_provider_id = None
        file_full_path = file.file_path + file.file_name

        for cloud_provider in self.cloud_providers:
            if cloud_provider not in intentos:
                try:
                    cloud_provider_name = cloud_provider.upload_file(
                        file_path=file_full_path, file_content=file.file_content
                    )
                    cloud_provider_id = list(filter(lambda x: x.name == cloud_provider_name,self.providers))[0].id
                    break
                except Exception as e:
                    intentos.append(cloud_provider)
            if len(intentos) == len(self.cloud_providers):
                raise HTTPException(
                    status_code=500, detail="Clouds providers unavailable"
                )

        user_file = UserFiles(
            user_id=user_id,
            cloud_provider_id=cloud_provider_id,
            file_path=file.file_path,
            file_name=file.file_name,
            file_size=file.file_size,
            file_extension=file.file_extension,
        )

        return user_file
