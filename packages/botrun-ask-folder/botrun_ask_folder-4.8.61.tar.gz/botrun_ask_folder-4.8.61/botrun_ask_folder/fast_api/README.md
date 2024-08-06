# 使用方式
- 安裝 FastAPI
```shell
pip install fastapi
```
- 執行測試的 server，在這個 folder下執行
```shell
fastapi dev main.py
```
## 本地測試
 - 如果在 local 測試: http://127.0.0.1:8000/api/botrun/botrun_ask_folder/這裡接自己的 api 名稱
 - 線上測試：/api/botrun/botrun_ask_folder/這裡接自己的 api 名稱
```shell
curl -X POST -N --no-buffer "http://127.0.0.1:8000/api/botrun/botrun_ask_folder/query_qdrant_and_llm" \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "collection_name": "1qk5maEqbxtTcr1tsAHawVduonPedpHV0",
    "user_input": "青創貸款怎麼樣申請最快速？",
    "qdrant_port": 6333,
    "embedding_model": "openai/text-embedding-3-large",
    "top_k": 6,
    "notice_prompt": "",
    "chat_model": "openai/gpt-4o-mini",
    "hnsw_ef": 256
  }'
curl -X POST "http://127.0.0.1:8000/api/botrun/botrun_ask_folder/query_qdrant_and_llm" \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "collection_name": "1qk5maEqbxtTcr1tsAHawVduonPedpHV0",
    "user_input": "青創貸款怎麼樣申請最快速？",
    "qdrant_port": 6333,
    "embedding_model": "openai/text-embedding-3-large",
    "top_k": 6,
    "notice_prompt": "",
    "chat_model": "openai/gpt-4o-mini",
    "hnsw_ef": 256,
    "stream":false
  }'
curl -X POST -N --no-buffer http://127.0.0.1:8000/api/botrun/botrun_ask_folder/query_qdrant_and_llm_from_botrun \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "botrun_name": "波創價學會",
    "folder_id": "1dqIGPK-hbyfrKbetQiWy3JW_jXGKG2YF",
    "user_input": "創價學會的宗指為何？"
  }'
curl -X POST -N --no-buffer https://dev.botrun.ai/api/botrun/botrun_ask_folder/query_qdrant_and_llm_from_botrun \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "botrun_name": "波創價學會",
    "folder_id": "1dqIGPK-hbyfrKbetQiWy3JW_jXGKG2YF",
    "user_input": "創價學會的宗指為何？"
  }'

curl -X POST http://127.0.0.1:8000/api/botrun/botrun_ask_folder/query_qdrant_and_llm_from_botrun \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "botrun_name": "波創價學會",
    "user_input": "創價學會的宗指為何？",
    "stream":false
  }'

curl -X POST http://127.0.0.1:8000/api/botrun/botrun_ask_folder/get_latest_timestamp \
  -H "Content-Type: application/json" \
  -d '{
    "botrun_name": "波創價學會"
  }'
```

## dev測試
```shell
curl -X POST -N --no-buffer https://dev.botrun.ai/api/botrun/botrun_ask_folder/query_qdrant_and_llm_from_botrun \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "botrun_name": "波創價學會",
    "folder_id": "1dqIGPK-hbyfrKbetQiWy3JW_jXGKG2YF",
    "user_input": "創價學會的宗指為何？"
  }'
curl -X POST https://dev.botrun.ai/api/botrun/botrun_ask_folder/query_qdrant_and_llm_from_botrun \
  -H "Content-Type: application/json" \
  -d '{
    "qdrant_host": "dev.botrun.ai",
    "botrun_name": "波創價學會",
    "folder_id": "1dqIGPK-hbyfrKbetQiWy3JW_jXGKG2YF",
    "user_input": "創價學會的宗指為何？",
    "stream":false
  }'
curl -X POST https://dev.botrun.ai/api/botrun/botrun_ask_folder/get_latest_timestamp \
  -H "Content-Type: application/json" \
  -d '{
    "botrun_name": "波創價學會",
    "folder_id": "1dqIGPK-hbyfrKbetQiWy3JW_jXGKG2YF"
  }'
```
