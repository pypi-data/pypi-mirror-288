# Proxy Server
- config.yaml 裡要有的 model，才能使用
## 安裝
- 需要安裝 litellm[proxy]

## 執行 server
目前改成 docker 方式，所以這一行可能無法執行了，但是還是留著參考
```shell
litellm --config botrun_ask_folder/litellm_proxy/config/config.yaml
```

## 執行 server docker
```shell
docker-compose up -d
```
## test
```shell
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer bo-7a51bc5d-d231-46cf-bd6f-f0a8ac6138f0' \
-d '{
    "model": "botrun-llm/botrun-波創價學會",
    "messages": [{"role": "user", "content": "創價學會的宗指為何？"}],
}'
curl -X POST 'http://0.0.0.0:4000/chat/completions' \
-H 'Content-Type: application/json' \
-H 'Authorization: Bearer bo-7a51bc5d-d231-46cf-bd6f-f0a8ac6138f0' \
-H "Accept: text/event-stream" \
-d '{
    "model": "botrun-llm/botrun-波創價學會",
    "messages": [{"role": "user", "content": "創價學會的宗指為何？"}],
    "stream":true
}'
```
