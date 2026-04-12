---
name: Qwen3.5 35B-A3B FP8
params:
  total: 35
  active: 3
---

```bash
docker run \
  --name qwen35 \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:cu130-nightly \
    Qwen/Qwen3.5-35B-A3B-FP8 \
    --port 8000 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name qwen35 \
    --max-model-len 256k \
    --language-model-only \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --enable-chunked-prefill \
    --max-num-batched-tokens 65536 \
    --max-num-seqs 15 \
    --enable-prefix-caching \
    --speculative-config '{"method": "mtp", "num_speculative_tokens": 1}'

```
