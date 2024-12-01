from datetime import datetime, timedelta

from azure.storage.blob import (
    AccountSasPermissions,
    BlobClient,
    ResourceTypes,
    generate_account_sas,
)

from config.utils import AZURE_ACCOUNT_KEY, AZURE_ACCOUNT_NAME, AZURE_CONTAINER_NAME
from services.cloudProvider import CloudProviderService


class AzureService(CloudProviderService):
    account_name = AZURE_ACCOUNT_NAME
    account_key = AZURE_ACCOUNT_KEY
    container_name = AZURE_CONTAINER_NAME
    sas_token: str

    def __init__(self):
        self.sas_token = generate_account_sas(
            account_name=self.account_name,
            account_key=self.account_key,
            resource_types=ResourceTypes(service=True, container=True, object=True),
            permission=AccountSasPermissions(
                read=True, write=True, update=True, list=True
            ),
            expiry=datetime.now() + timedelta(minutes=10),
        )

    def upload_file(self, file_path: str, file_content: bytes):
        blob = BlobClient(
            account_url="https://" + self.account_name + ".blob.core.windows.net/",
            container_name=self.container_name,
            blob_name=file_path,
            credential=self.sas_token,
        )

        result = blob.upload_blob(file_content)
        blob.close()
        return "AZURE"
