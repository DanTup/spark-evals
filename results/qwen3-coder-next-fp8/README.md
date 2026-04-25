---
name: Qwen3 Coder Next FP8
params:
  total: 80
  active: 3
---

```bash
docker run \
  --name qwen3-coder \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:v0.19.1-cu130 \
    Qwen/Qwen3-Coder-Next-FP8 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.8 \
    --served-model-name qwen3-coder \
    --max-model-len 256K \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code
```
