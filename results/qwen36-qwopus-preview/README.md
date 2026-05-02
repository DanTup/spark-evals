---
name: Jackrong Qwopus 3.6 27B
params: 27
flags:
  - v1-preview
---

```bash
docker run \
  --name qwen36-qwopus \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:latest \
    Jackrong/Qwopus3.6-27B-v1-preview \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name qwen36-qwopus \
    --max-model-len 256K \
    --language-model-only \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --speculative-config '{"method": "mtp", "num_speculative_tokens": 2}'
```
