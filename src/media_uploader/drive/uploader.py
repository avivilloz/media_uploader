import os
import logging
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow


__all__ = ["DriveUploader"]

LOG = logging.getLogger(__name__)


class DriveUploader:
    def __init__(
        self,
        client_secrets_file="client_secrets.json",
        token_file_path="drive_token.json",
        local_server_port: int = 8081,
    ):
        self.token_file_path = token_file_path
        self.client_secrets_file = client_secrets_file
        self.service = self.get_drive_service()
        self.local_server_port = local_server_port
        self.scopes = ["https://www.googleapis.com/auth/drive"]

    def get_credentials(self):
        """
        Get the Google Drive API credentials from the token file or via the OAuth flow.
        """
        creds = None
        if os.path.exists(self.token_file_path):
            LOG.info(f"Loading credentials from {self.token_file_path}")
            creds = Credentials.from_authorized_user_file(
                self.token_file_path, self.scopes
            )
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                LOG.info("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                LOG.info("Fetching new credentials using OAuth flow")
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secrets_file, self.scopes
                )
                creds = flow.run_local_server(port=0)
            with open(self.token_file_path, "w") as token:
                LOG.info(f"Saving credentials to {self.token_file_path}")
                token.write(creds.to_json())
        return creds

    def get_drive_service(self):
        """
        Build and return the Google Drive service object.
        """
        creds = self.get_credentials()
        LOG.info("Building Google Drive service")
        return build("drive", "v3", credentials=creds)

    def find_or_create_folder(self, folder_path, parent_id=None):
        """
        Recursively find or create folders in Google Drive.

        :param folder_path: Path of folders to create in Drive (e.g., 'Folder1/Subfolder2')
        :param parent_id: Optional parent folder ID in Drive
        :return: ID of the last folder created or found
        """
        folders = folder_path.split("/")
        current_parent = parent_id

        for folder in folders:
            query = f"name='{folder}' and mimeType='application/vnd.google-apps.folder'"
            if current_parent:
                query += f" and '{current_parent}' in parents"

            LOG.info(f"Searching for folder: {folder} in Drive")
            results = (
                self.service.files()
                .list(q=query, spaces="drive", fields="files(id, name)")
                .execute()
            )
            items = results.get("files", [])

            if not items:
                LOG.info(f"Folder '{folder}' not found, creating it")
                file_metadata = {
                    "name": folder,
                    "mimeType": "application/vnd.google-apps.folder",
                }
                if current_parent:
                    file_metadata["parents"] = [current_parent]
                current_parent = (
                    self.service.files()
                    .create(body=file_metadata, fields="id")
                    .execute()
                    .get("id")
                )
                LOG.info(f"Created folder '{folder}' with ID: {current_parent}")
            else:
                current_parent = items[0]["id"]
                LOG.info(f"Found folder '{folder}' with ID: {current_parent}")

        return current_parent

    def upload_file(self, file_path, parent_id):
        """
        Upload a file to Google Drive.

        :param file_path: Local file path to upload
        :param parent_id: Google Drive folder ID where the file will be uploaded
        """
        file_name = os.path.basename(file_path)
        LOG.info(f"Uploading file: {file_name}")
        file_metadata = {"name": file_name, "parents": [parent_id]}
        media = MediaFileUpload(file_path, resumable=True)
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )

        LOG.info(f'Uploaded file: {file_name} (ID: {file.get("id")})')

    def upload_folder(self, local_folder, drive_folder_id):
        """
        Upload a local folder recursively to Google Drive.

        :param local_folder: Local folder path to upload
        :param drive_folder_id: Google Drive folder ID where the folder will be uploaded
        """
        LOG.info(f"Uploading folder: {local_folder}")
        for item in os.listdir(local_folder):
            item_path = os.path.join(local_folder, item)
            if os.path.isfile(item_path):
                self.upload_file(item_path, drive_folder_id)
            elif os.path.isdir(item_path):
                LOG.info(
                    f"Creating folder '{item}' inside Drive folder ID: {drive_folder_id}"
                )
                new_folder_metadata = {
                    "name": item,
                    "mimeType": "application/vnd.google-apps.folder",
                    "parents": [drive_folder_id],
                }
                new_folder = (
                    self.service.files()
                    .create(body=new_folder_metadata, fields="id")
                    .execute()
                )
                self.upload_folder(item_path, new_folder.get("id"))

    def upload(self, src_path, dst_path):
        """
        Upload a file or folder to Google Drive.

        :param src_path: Local path of the file or folder to upload
        :param dst_path: Destination path in Google Drive (e.g., 'Folder1/Subfolder2')
        :return: ID of the uploaded file or folder
        """
        LOG.info(f"Starting upload of {src_path} to Drive at {dst_path}")
        drive_folder_id = self.find_or_create_folder(dst_path)

        if os.path.isfile(src_path):
            self.upload_file(src_path, drive_folder_id)
        elif os.path.isdir(src_path):
            self.upload_folder(src_path, drive_folder_id)
        else:
            LOG.error(f"The source path {src_path} is neither a file nor a directory.")
            raise ValueError(
                f"The source path {src_path} is neither a file nor a directory."
            )

        LOG.info(f"Finished upload to folder ID: {drive_folder_id}")
        return drive_folder_id
