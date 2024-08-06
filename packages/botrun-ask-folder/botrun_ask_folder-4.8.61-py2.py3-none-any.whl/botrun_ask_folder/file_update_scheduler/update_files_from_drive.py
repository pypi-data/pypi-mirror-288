from botrun_ask_folder.update_files_from_drive import update_files_from_drive
from pathlib import Path
from botrun_ask_folder.models.google_drive_file_update_info import GoogleDriveFileUpdateResponse

if __name__ == '__main__':
    lst_updated_files = [
        {
            "collection_id": "1qk5maEqbxtTcr1tsAHawVduonPedpHV0",
            "file_id": "1cxJwtlTefxCFZvkMwaCaEOQEdi928__D",
            "file_name": "青年創業及啟動金貸款補貼息請領作業承貸金融機構應行注意事項問與答11101V6(紅字).pdf",
            "updated_time": "2024-07-10T01:27:57.031Z"
        }
    ]

    lst_response = update_files_from_drive(lst_updated_files, Path("./data/"))
    for response in GoogleDriveFileUpdateResponse.to_list(lst_response):
        print(response)
