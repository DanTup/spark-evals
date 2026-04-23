---
name: Gemma4 26B-A4B
params:
  total: 26
  active: 4
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
  vllm/vllm-openai:v0.19.1-cu130 \
    google/gemma-4-26B-A4B-IT \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name gemma4 \
    --max-model-len 256k \
    --reasoning-parser gemma4 \
    --enable-auto-tool-choice \
    --tool-call-parser gemma4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code
```
