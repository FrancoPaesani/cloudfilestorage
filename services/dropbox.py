import dropbox

from config.utils import DROPBOX_ACCESS_TOKEN, DROPBOX_APP_KEY, DROPBOX_APP_SECRET, DROPBOX_REFRESH_TOKEN
from services.cloudProvider import CloudProviderService

class DropboxService(CloudProviderService):
    app_key = DROPBOX_APP_KEY
    app_secret = DROPBOX_APP_SECRET
    access_token = DROPBOX_ACCESS_TOKEN
    refresh_token = DROPBOX_REFRESH_TOKEN
    dbx_connection = None
           
    def upload_file(self, file_path: str, file_content: bytes):
        new_access_token = self.refresh_access_token(self.app_key, self.app_secret, self.refresh_token)
        self.dbx_connection = dropbox.Dropbox(oauth2_access_token=new_access_token)
        result = self.dbx_connection.files_upload(file_content, file_path)

        return 1 #TODO: traer de la DB el codigo del CP
    
    #TODO: check function
    def refresh_access_token(self, app_key, app_secret, refresh_token):
        try:
            dbx = dropbox.Dropbox(
                oauth2_refresh_token=refresh_token,
                app_key=app_key,
                app_secret=app_secret,
            )
            
            dbx.users_get_current_account()

            new_access_token = dbx._oauth2_access_token
            return new_access_token
        except Exception as e:
            print(f"Error refreshing access token: {e}")
            return None