---
name: Laguna XS.2
params:
  total: 33
  active: 3
---

```bash
docker run \
  --name laguna \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:latest \
    poolside/Laguna-XS.2 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name laguna \
    --max-model-len 256K \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --default-chat-template-kwargs '{"enable_thinking": true}'
```
