---
name: Ornith 35B FP8
params:
  total: 35
  active: 3
---

```bash
docker run \
  --name ornith \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:nightly \
    deepreinforce-ai/Ornith-1.0-35B-FP8 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name ornith \
    --max-model-len 120k \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_xml \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code
```
