from fastapi import FastAPI, HTTPException, Query, APIRouter
from fastapi.responses import StreamingResponse, Response, JSONResponse
from urllib.parse import quote

import functions_framework
from flask import jsonify, Request, Response, stream_with_context
from pydantic import BaseModel, Field
import io
import os
import json
from googleapiclient.errors import HttpError
from google.cloud.exceptions import NotFound
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

from botrun_ask_folder.fast_api.util.pdf_util import pdf_page_to_image, DEFAULT_DPI
from botrun_ask_folder.query_qdrant import query_qdrant_and_llm
from botrun_ask_folder.util import get_latest_timestamp
import asyncio

router = APIRouter(
    prefix='/botrun_ask_folder',
    tags=["botrun_ask_folder"]
)

@router.get("/download_file/{file_id}")
def download_file(file_id: str):
    service_account_file = "keys/google_service_account_key.json"
    credentials = service_account.Credentials.from_service_account_file(
        service_account_file,
        scopes=['https://www.googleapis.com/auth/drive']
    )
    drive_service = build('drive', 'v3', credentials=credentials)

    try:
        file = drive_service.files().get(fileId=file_id, fields='name, mimeType').execute()
        file_name = file.get('name')
        file_mime_type = file.get('mimeType')

        request = drive_service.files().get_media(fileId=file_id)

        def file_stream():
            fh = io.BytesIO()
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
                yield fh.getvalue()
                fh.seek(0)
                fh.truncate(0)

        # Encode the filename for Content-Disposition
        encoded_filename = quote(file_name)

        headers = {
            "Content-Disposition": f"attachment; filename*=UTF-8''{encoded_filename}",
            "Content-Type": file_mime_type
        }

        return StreamingResponse(file_stream(), headers=headers, media_type=file_mime_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/get_pdf_page/{file_id}")
def get_pdf_page(
        file_id: str,
        page: int = Query(1, ge=1, description="Page number to retrieve"),
        dpi: int = Query(DEFAULT_DPI, ge=72, le=600, description="DPI for rendering"),
        scale: float = Query(1.0, ge=0.1, le=2.0, description="Scaling factor"),
        color: bool = Query(True, description="Render in color if True, else grayscale")
):
    try:
        img_byte_arr = pdf_page_to_image(
            file_id=file_id,
            page=page,
            dpi=dpi,
            scale=scale,
            color=color
        )

        return Response(content=img_byte_arr, media_type="image/png")
    except ValueError as e:
        return Response(content=str(e), media_type="text/plain")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



class GetLatestTimestampInput(BaseModel):
    botrun_name: str
    folder_id: str

class GetLatestTimestampOutput(BaseModel):
    latest_timestamp: str

@router.post("/get_latest_timestamp", response_model=GetLatestTimestampOutput)
async def fa_get_latest_timestamp(input_data: GetLatestTimestampInput):
    """
    這個端點用於獲取指定 collection 的最新時間戳
    """
    try:
        # 使用現有函數獲取 collection_name
        _, collection_name = read_notice_prompt_and_collection_from_botrun(input_data.botrun_name, input_data.folder_id)
        print(f"collection_name: {collection_name}")

        # 調用 get_latest_timestamp 函數
        latest_timestamp = await get_latest_timestamp(collection_name)
        print(f"latest_timestamp: {latest_timestamp}")

        return {"latest_timestamp": latest_timestamp}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class QueryQdrantAndLlmFromBotrunInput(BaseModel):
    qdrant_host: str
    botrun_name: str
    folder_id: str
    stream: bool = True
    user_input: str = ""
    embedding_model: str = 'openai/text-embedding-3-large'
    top_k: int = 6
    chat_model: str = "openai/gpt-4o-mini"
    hnsw_ef: int = 256

@router.post("/query_qdrant_and_llm_from_botrun")
async def fa_query_qdrant_and_llm_from_botrun(query_input: QueryQdrantAndLlmFromBotrunInput):
    """
    這個是可以從 botrun 的檔案，讀取 notice_prompt 的內容，然後透過 qdrant 和 LLM 來查詢相關的文件
    """
    # 固定字段名稱
    file_path_field = "file_path"
    text_content_field = "text_content"
    google_file_id_field = "google_file_id"
    page_number_field = "page_number"
    gen_page_imgs_field = "gen_page_imgs"
    ori_file_name_field = "ori_file_name"
    sheet_name_field = "sheet_name"
    file_upload_date_field = "file-upload-date"

    # 從 botrun 檔案讀取 notice_prompt
    try:
        notice_prompt, collection_name = read_notice_prompt_and_collection_from_botrun(query_input.botrun_name, query_input.folder_id)
        print(f"notice_prompt: {notice_prompt}")
        print(f"collection_name: {collection_name}")
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    if query_input.stream:
        async def generate():
            for fragment in query_qdrant_and_llm(
                query_input.qdrant_host, 6333, collection_name, query_input.user_input,
                query_input.embedding_model, query_input.top_k, notice_prompt,
                query_input.chat_model, query_input.hnsw_ef, file_path_field, text_content_field,
                google_file_id_field, page_number_field, gen_page_imgs_field,
                ori_file_name_field, sheet_name_field, file_upload_date_field
            ):
                print(fragment, end="")
                yield fragment

        return StreamingResponse(generate())
    else:
        result = ""
        for fragment in query_qdrant_and_llm(
            query_input.qdrant_host, 6333, collection_name, query_input.user_input,
            query_input.embedding_model, query_input.top_k, notice_prompt,
            query_input.chat_model, query_input.hnsw_ef, file_path_field, text_content_field,
            google_file_id_field, page_number_field, gen_page_imgs_field,
            ori_file_name_field, sheet_name_field, file_upload_date_field
        ):
            result += fragment
        return JSONResponse(content={"result": result})

def read_botrun_content(botrun_name: str, folder_id: str) -> str:
    """
    從 Google Drive 的指定資料夾中讀取 .botrun 檔案的內容
    """
    try:
        # 建立 Google Drive API 客戶端
        service_account_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS", "")
        if not service_account_file:
            raise Exception("GOOGLE_APPLICATION_CREDENTIALS environment variable is not set")
        credentials = service_account.Credentials.from_service_account_file(service_account_file)
        service = build('drive', 'v3', credentials=credentials)

        # 搜尋 .botrun 檔案
        file_query = f"'{folder_id}' in parents and name='{botrun_name}.botrun'"
        file_results = service.files().list(q=file_query, spaces='drive', fields='files(id, mimeType)').execute()
        files = file_results.get('files', [])

        if not files:
            raise Exception(f"File '{botrun_name}.botrun' not found in the specified folder")

        file_id = files[0]['id']
        mime_type = files[0]['mimeType']

        # 讀取檔案內容
        if mime_type == 'application/vnd.google-apps.document':
            # 如果是 Google Docs 文件，使用 export 方法
            request = service.files().export_media(fileId=file_id, mimeType='text/plain')
            file_content = request.execute()
            return file_content.decode('utf-8')
        else:
            # 對於其他類型的文件，使用 get_media 方法
            request = service.files().get_media(fileId=file_id)
            file_content = io.BytesIO()
            downloader = MediaIoBaseDownload(file_content, request)
            done = False
            while done is False:
                _, done = downloader.next_chunk()
            return file_content.getvalue().decode('utf-8')

    except HttpError as error:
        raise Exception(f"An error occurred: {error}")


def read_notice_prompt_and_collection_from_botrun(botrun_name, folder_id):
    """
    從 botrun 檔案讀取 notice_prompt 和 collection_name
    """
    # 這裡需要實現從 botrun 檔案讀取內容的邏輯
    # 以下是示例邏輯，您需要根據實際情況修改
    file_content = read_botrun_content(botrun_name, folder_id)

    # 分割內容
    parts = file_content.split("@begin import_rag_plus")

    if len(parts) < 2:
        raise ValueError("無法找到 @begin import_rag_plus 標記")

    notice_prompt = parts[0].strip()

    # 解析 JSON 部分以獲取 collection_name
    import json
    try:
        rag_config = json.loads(parts[1].split("@end")[0])
        collection_name = rag_config.get("collection_name")
        if not collection_name:
            raise ValueError("無法在 JSON 中找到 collection_name")
    except json.JSONDecodeError:
        raise ValueError("無法解析 JSON 配置")

    return notice_prompt, collection_name


class QueryQdrantAndLlmInput(BaseModel):
    qdrant_host: str
    collection_name: str
    stream: bool = True
    qdrant_port: int = 6333
    user_input: str = ""
    embedding_model: str = "openai/text-embedding-3-large"
    top_k: int = 6
    notice_prompt: str = ""
    chat_model: str = "openai/gpt-4-mini"
    hnsw_ef: int = 256

@router.post("/query_qdrant_and_llm")
async def fa_query_qdrant_and_llm(query_input: QueryQdrantAndLlmInput):
    # 固定字段名稱
    file_path_field = "file_path"
    text_content_field = "text_content"
    google_file_id_field = "google_file_id"
    page_number_field = "page_number"
    gen_page_imgs_field = "gen_page_imgs"
    ori_file_name_field = "ori_file_name"
    sheet_name_field = "sheet_name"
    file_upload_date_field = "file-upload-date"

    if query_input.stream:
        async def generate():
            for fragment in query_qdrant_and_llm(
                query_input.qdrant_host,
                query_input.qdrant_port,
                query_input.collection_name,
                query_input.user_input,
                query_input.embedding_model,
                query_input.top_k,
                query_input.notice_prompt,
                query_input.chat_model,
                query_input.hnsw_ef,
                file_path_field,
                text_content_field,
                google_file_id_field,
                page_number_field,
                gen_page_imgs_field,
                ori_file_name_field,
                sheet_name_field,
                file_upload_date_field
            ):
                yield fragment

        return StreamingResponse(generate())
    else:
        result = ""
        for fragment in query_qdrant_and_llm(
            query_input.qdrant_host,
            query_input.qdrant_port,
            query_input.collection_name,
            query_input.user_input,
            query_input.embedding_model,
            query_input.top_k,
            query_input.notice_prompt,
            query_input.chat_model,
            query_input.hnsw_ef,
            file_path_field,
            text_content_field,
            google_file_id_field,
            page_number_field,
            gen_page_imgs_field,
            ori_file_name_field,
            sheet_name_field,
            file_upload_date_field
        ):
            result += fragment
        return JSONResponse(content={"result": result})
