import asyncio
import os
import shutil
import json

# from .botrun_ask_folder_logger import BotrunAskFolderLogger
from .botrun_drive_manager import botrun_drive_manager
from .drive_download import drive_download, drive_download_items
from .drive_download_metadata import get_drive_download_metadata, save_drive_download_metadata
from .drive_list_files import drive_list_files
from .embeddings_to_qdrant import embeddings_to_qdrant, has_collection_in_qdrant
from .run_split_txts import run_split_txts
from .run_pdf_to_img import run_pdf_to_img


def botrun_ask_folder(google_drive_folder_id: str,
                      force=False,
                      gen_page_imgs=False
                      ) -> None:
    """
    @param google_drive_folder_id: Google Drive folder ID
    @param force: If True, 所有的資料 (qdrant collection, downloaded files...) 會刪掉重新建立
    """

    if force:
        if os.path.exists(f"./data/{google_drive_folder_id}"):
            # logger.info(f"Removing existing data directory for folder ID: {google_drive_folder_id}")
            shutil.rmtree(f"./data/{google_drive_folder_id}")

    google_service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS",
                                                "/app/keys/google_service_account_key.json")

    drive_download(
        google_service_account_key_path,
        google_drive_folder_id,
        9999999,
        output_folder=f"./data/{google_drive_folder_id}",
        force=force,
    )

    run_split_txts(
        f"./data/{google_drive_folder_id}",
        2000,
        force,
        gen_page_imgs)

    if gen_page_imgs:
        run_pdf_to_img(google_drive_folder_id, force)

    qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
    qdrant_port = os.getenv("QDRANT_PORT", 6333)

    collection_existed = asyncio.run(has_collection_in_qdrant(
        f"{google_drive_folder_id}",
        qdrant_host,
        qdrant_port,
    ))

    asyncio.run(embeddings_to_qdrant(
        f"./data/{google_drive_folder_id}",
        "openai/text-embedding-3-large",
        3072,
        30,
        f"{google_drive_folder_id}",
        qdrant_host,
        qdrant_port,
        force=force
    ))

    if not collection_existed:
        botrun_drive_manager(
            f"波{google_drive_folder_id}",
            f"{google_drive_folder_id}",
            force=force)
    elif force:
        botrun_drive_manager(
            f"波{google_drive_folder_id}",
            f"{google_drive_folder_id}",
            force=force)
    else:
        print("\n已更新完畢，可以開始使用。")


def botrun_ask_folder_separately(google_drive_folder_id: str,
                                 force=False,
                                 gen_page_imgs=False,
                                 start_index=0,
                                 batch_size=50,
                                 ) -> None:
    """
    這支 function 主要是讓 local 在執行時可以分開執行，不會一次執行太多，debug 比較好知道哪些檔案有問題
    """

    # if force:
    #     if os.path.exists(f"./data/{google_drive_folder_id}"):
    #         # logger.info(f"Removing existing data directory for folder ID: {google_drive_folder_id}")
    #         shutil.rmtree(f"./data/{google_drive_folder_id}")

    google_service_account_key_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS",
                                                "/app/keys/google_service_account_key.json")

    output_folder = f"./data/{google_drive_folder_id}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    ori_metadata_name = '{folder_id}-ori-metadata.json'.format(folder_id=google_drive_folder_id)
    metadata_name = '{folder_id}-metadata.json'.format(folder_id=google_drive_folder_id)
    files_to_keep = [ori_metadata_name]
    ori_metadata_path = os.path.join(output_folder, ori_metadata_name)
    metadata_path = os.path.join(output_folder, metadata_name)
    dic_metadata = {}
    if os.path.exists(ori_metadata_path):
        # load json, utf-8
        with open(ori_metadata_path, "r", encoding="utf-8") as f:
            dic_metadata = json.load(f)

    if not dic_metadata:
        print("== Begin listing files in Google Drive ==")
        dic_metadata = drive_list_files(google_service_account_key_path, google_drive_folder_id, 9999999)
        with open(ori_metadata_path, "w", encoding="utf-8") as f:
            json.dump(dic_metadata, f, ensure_ascii=False, indent=4)

    total_items = len(dic_metadata['items'])
    print(f"總共有 {total_items} 個檔案要處理")
    current_index = start_index
    all_items = dic_metadata['items']
    while current_index < total_items:
        if force:
            # 每次將子目錄刪除，節省本地端的空間
            remove_contents_except(output_folder, files_to_keep)
            shutil.copy2(ori_metadata_path, metadata_path)

        end_index = min(current_index + batch_size, total_items)
        batch_items = all_items[current_index:end_index]
        # 在這裡處理當前批次
        print(f"處理從索引 {current_index} 到 {end_index - 1} 的項目")
        drive_download_items(google_service_account_key_path, batch_items, output_folder, force)

        run_split_txts(
            f"./data/{google_drive_folder_id}",
            5000,
            force,
            gen_page_imgs)

        if gen_page_imgs:
            run_pdf_to_img(google_drive_folder_id, force)

        qdrant_host = os.getenv("QDRANT_HOST", "qdrant")
        qdrant_port = os.getenv("QDRANT_PORT", 6333)

        asyncio.run(embeddings_to_qdrant(
            f"./data/{google_drive_folder_id}",
            "openai/text-embedding-3-large",
            3072,
            30,
            f"{google_drive_folder_id}",
            qdrant_host,
            qdrant_port,
            force=force
        ))

        # logger.info(f"Running botrun_drive_manager for folder ID: {google_drive_folder_id}")
        botrun_drive_manager(
            f"波{google_drive_folder_id}",
            f"{google_drive_folder_id}",
            force=force)

        # 更新索引以處理下一批
        current_index = end_index


def remove_contents_except(directory, files_to_keep):
    # 確保目錄路徑存在
    if not os.path.exists(directory):
        print(f"目錄 '{directory}' 不存在。")
        return

    # 將 files_to_keep 轉換為集合，以提高查找效率
    files_to_keep_set = set(files_to_keep)

    # 遍歷目錄中的所有項目
    for item in os.listdir(directory):
        item_path = os.path.join(directory, item)

        # 如果項目不在 files_to_keep 中，則刪除
        if item not in files_to_keep_set:
            try:
                if os.path.isdir(item_path):
                    shutil.rmtree(item_path)
                    print(f"已刪除目錄: {item_path}")
                else:
                    os.remove(item_path)
                    print(f"已刪除文件: {item_path}")
            except Exception as e:
                print(f"刪除 {item_path} 時出錯: {e}")
