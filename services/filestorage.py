from fastapi import HTTPException, UploadFile

from models.filestorage import UserFiles
from schemas.filestorage import FileInfo
from services.azure import AzureService
from services.cloudProvider import CloudProviderService
from services.dropbox import DropboxService


class FileService:
    def parse_file(self, file_path, file: UploadFile) -> FileInfo:
        file_content = file.file.read()
        file_size = file.size
        file_name = file.filename

        file_extension = file_name.split(".")
        file_extension = file_extension[len(file_extension) - 1]

        return FileInfo(
            file_path=file_path,
            file_name=file_name,
            file_size=file_size,
            file_extension=file_extension,
            file_content=file_content,
        )


class StorageService:
    cloud_providers: list[CloudProviderService] = [DropboxService(), AzureService()]

    def upload_file(self, file: FileInfo, user_id: int):
        intentos = []
        cloud_provider_id = None
        file_full_path = file.file_path + file.file_name

        for cloud_provider in self.cloud_providers:
            if cloud_provider not in intentos:
                try:
                    cloud_provider_id = cloud_provider.upload_file(
                        file_path=file_full_path, file_content=file.file_content
                    )
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
