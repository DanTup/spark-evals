---
name: Gemma4 31B
params: 31
flags:
  speculative-config: gemma-4-31B-it-assistant(4)
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
  vllm/vllm-openai:nightly \
    google/gemma-4-31B-it \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name gemma4 \
    --limit-mm-per-prompt '{"image": 0, "audio": 0}' \
    --async-scheduling \
    --max-model-len 128K \
    --reasoning-parser gemma4 \
    --enable-auto-tool-choice \
    --tool-call-parser gemma4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 16384 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code \
    --speculative-config '{"model": "google/gemma-4-31B-it-assistant", "num_speculative_tokens": 4}'
```
