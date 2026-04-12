---
name: Gemma4 E2B
params: 2
---

```bash
docker run \
  --name gemma4 \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:gemma4-cu130 \
  google/gemma-4-E2B-it \
    --port 8000 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.8 \
    --served-model-name gemma4 \
    --max-model-len 128k \
    --reasoning-parser gemma4 \
    --enable-auto-tool-choice \
    --tool-call-parser gemma4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 65536 \
    --max-num-seqs 15 \
    --enable-prefix-caching \
    --trust-remote-code
```
