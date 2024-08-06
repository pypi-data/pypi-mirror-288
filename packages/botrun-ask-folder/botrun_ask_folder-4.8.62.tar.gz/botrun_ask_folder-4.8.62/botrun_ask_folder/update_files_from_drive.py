import os

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from googleapiclient.discovery import Resource
from typing import List, Dict

from botrun_ask_folder.botrun_ask_folder import handle_downloaded_files_and_save_to_qdrant
from botrun_ask_folder.drive_download import download_file, truncate_filename, drive_download_items
from botrun_ask_folder.models.google_drive_file_update_info import (GoogleDriveFileUpdateInfo,
                                                                    GoogleDriveFileUpdateResponse)
from pathlib import Path


def update_files_from_drive(data_list: List[Dict], data_path: Path)->List[GoogleDriveFileUpdateResponse]:
    """
    :param data_list: List of dictionaries containing file information，可以轉成GoogleDriveFileUpdateInfo
    """
    file_info_list = GoogleDriveFileUpdateInfo.from_list(data_list)
    service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", './keys/google_service_account_key.json')
    print(Path(service_account_file).resolve())
    credentials = service_account.Credentials.from_service_account_file(service_account_file)
    service = build('drive', 'v3', credentials=credentials)
    lst_response = []
    for file_info in file_info_list:
        file_metadata = service.files().get(fileId=file_info.file_id,
                                            fields="id, name, size, mimeType, parents, modifiedTime").execute()
        output_folder = str(data_path / file_info.collection_id)
        # drive_download_items 有用到 path，它本來是要 base_path ＋　name
        # 可是因為 base_path 都是 ""，所以這裡先直接用 assign 的方式
        file_metadata['path'] = file_metadata['name']
        drive_download_items(service_account_file, [file_metadata], output_folder)
        handle_downloaded_files_and_save_to_qdrant(file_info.collection_id)
        lst_response.append(GoogleDriveFileUpdateResponse(file_id=file_info.file_id,
                                                          file_modified_time=file_metadata['modifiedTime']))
    return lst_response
