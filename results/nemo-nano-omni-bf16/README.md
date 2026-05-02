---
name: Nemotron3 Nano Omni 30B-A3B BF16
params:
  total: 30
  active: 3
---

```bash
docker run \
  --name nemo-nano-omni \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:v0.20.0 \
    nvidia/Nemotron-3-Nano-Omni-30B-A3B-Reasoning-BF16 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name nemo-nano-omni \
    --max-model-len 128K \
    --reasoning-parser nemotron_v3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code
```
