---
name: Intern S2 Preview
params:
  total: 35
  active: 3
---

```bash
docker run \
  --name intern-s2-preview \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  vllm/vllm-openai:nightly \
    internlm/Intern-S2-Preview \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name qwen36 \
    --max-model-len 256K \
    --language-model-only \
    --reasoning-parser qwen3 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code \
    --speculative-config '{"method":"mtp","num_speculative_tokens":4}'
```
