import io
import logging
import os
import datetime

from django.conf import settings
from django.core.cache import cache
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.http import MediaFileUpload, MediaIoBaseUpload

client_file = 'ttsgenerator-service-key.json'
API_NAME = "drive"
API_VERSION = "v3"
SCOPES = ["https://www.googleapis.com/auth/drive"]

logging.getLogger('googleapicliet.discovery_cache').setLevel(logging.ERROR)


def create_service_user(client_secret_file, api_name, api_version, *scopes, prefix=''):
    scopes = [scope for scope in scopes[0]]

    creds = None
    working_dir = os.getcwd()
    token_dir = 'token files'
    token_file = f'token_{api_name}_{api_version}{prefix}.json'

    ### Check if token dir exists first, if not, create the folder
    if not os.path.exists(os.path.join(working_dir, token_dir)):
        os.mkdir(os.path.join(working_dir, token_dir))

    if os.path.exists(os.path.join(working_dir, token_dir, token_file)):
        creds = Credentials.from_authorized_user_file(os.path.join(working_dir, token_dir, token_file), SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(client_file, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(os.path.join(working_dir, token_dir, token_file), 'w') as token:
            token.write(creds.to_json())

    try:
        service = build(api_name, API_VERSION, credentials=creds, cache_discovery=False)
        logging.info(f"{api_name}, {API_VERSION}, 'service created successfully")
        return service
    except Exception as e:
        logging.error(f'Failed to create service instance for {api_name}: {e}')
        os.remove(os.path.join(working_dir, token_dir, token_file))
        return None


def create_service(api_name, api_version, scopes, key_file_location):
    """Get a service that communicates to a Google API.

    Args:
        api_name: The name of the api to connect to.
        api_version: The api version to connect to.
        scopes: A list auth scopes to authorize for the application.
        key_file_location: The path to a valid service account JSON key file.

    Returns:
        A service that is connected to the specified API.
    """

    credentials = service_account.Credentials.from_service_account_file(key_file_location)
    scoped_credentials = credentials.with_scopes(scopes)

    # Build the service object.
    try:
        service = build(api_name, api_version, credentials=scoped_credentials, cache_discovery=False)
        logging.info(f"{api_name}, {API_VERSION}, 'service created successfully")
        return service
    except Exception as e:
        logging.error(f'Failed to create service instance for {api_name}: {e}')
        return None


def convert_to_rfc_datetime(year=1900, month=1, day=1, hour=0, minute=0):
    dt = datetime.datetime(year, month, day, hour, minute, 0).isoformat() + 'Z'
    return dt


class GoogleDriveApi:
    service = None
    directory_id = None

    def __init__(self):
        self.service = create_service(API_NAME, API_VERSION, SCOPES, client_file)
        self.directory_id = settings.DIRECTORY_ID

    def add_file_permissions(self, file_id: str, permission_type: str = "by_link") -> bool:
        if permission_type == "by_link":
            rules = dict(role="reader", type="anyone")
        else:
            return False

        try:
            response = self.service.permissions().create(
                fileId=file_id,
                sendNotificationEmail=False,
                # supportsAllDrives=True,
                # useDomainAdminAccess=True,
                body=rules
            ).execute()
            logging.info(f"GoogleDriveApi add_file_permissions: {response}")
        except Exception as ex:
            logging.error(f"GoogleDriveApi add_file_permissions fail: {ex}")
            return False

        return "kind" in response

    def __add_permissions_to_file__(self, file_data: dict) -> dict:
        if not file_data.get('id'):
            logging.error(f"Audio did n`t upload to google drive: {file_data}")
            return {"error": "can`t set permissions to file"}
        # response = {'kind': 'drive#file', 'id': '12-1DlP1aowOlpTxKcNrn9xZyVcokUtgl', 'name': 'e0544968-fba4-4c73-b69f-d0a8edb90c03.mp3', 'mimeType': 'audio/mpeg'}
        if not self.add_file_permissions(file_data.get('id')):
            return {"error": "can`t set permissions to file"}
        return {"url": f"https://drive.google.com/file/d/{file_data.get('id')}/view"}

    def __create_media_file_from_file__(self, file_path: str, mime_type: str):
        return MediaFileUpload(file_path, mime_type)

    def __create_media_file_from_cached_bytes__(self, cache_key: str, mime_type: str):
        bytes_data = cache.get(cache_key)
        return MediaIoBaseUpload(io.BytesIO(bytes_data), mime_type)

    def __upload_file__(self, media_content, file_name="unknown") -> dict:
        request_body = {
            "name": file_name,
            "shated": True,
            "parents": []
        }
        if self.directory_id:
            request_body["parents"].append(self.directory_id)

        logging.info(f"Starting upload file {file_name}")
        try:
            return self.service.files().create(
                body=request_body,
                media_body=media_content
            ).execute()
        except Exception as ex:
            logging.error(f"GoogleDriveApi load_to_disc fail: {ex}")
            return {"error": "can`t upload file"}

    def __from_file_to_disc(self, file_path, file_name="unknown", mime_type='audio/mpeg') -> dict:
        if not os.path.exists(file_path):
            logging.error(f"GoogleDriveApi load_to_disc fail: file not exists: {file_path}")
            return {"error": "server error"}

        if not self.service:
            logging.error(f"GoogleDriveApi load_to_disc fail: service doesn`t created")
            return {"error": "server error"}
        media_content = self.__create_media_file_from_file__(file_path, mime_type)
        return self.__upload_file__(media_content, file_name)

    def __from_cache_to_disc(self, tts_data, mime_type='audio/mpeg') -> dict:
        media_content = self.__create_media_file_from_cached_bytes__(tts_data.get("cache_key"), mime_type)
        return self.__upload_file__(media_content, tts_data.get("file_name"))

    def load_to_disc(self, tts_data, mime_type='audio/mpeg') -> dict:
        if not isinstance(tts_data, dict):
            logging.error(f"GoogleDriveApi load_to_disc fail: incorrect tts_data(1) {tts_data}")
            return {"error": "server error"}
        if tts_data.get("file_path") and tts_data.get("file_name"):
            file_data = self.__from_file_to_disc(tts_data.get("file_path"), tts_data.get("file_name"), mime_type)
        elif tts_data.get("file_name") and tts_data.get("cache_key"):
            file_data = self.__from_cache_to_disc(tts_data, mime_type)
        else:
            logging.error(f"GoogleDriveApi load_to_disc fail: incorrect tts_data(2) {tts_data}")
            return {"error": "server error"}

        return self.__add_permissions_to_file__(file_data)
