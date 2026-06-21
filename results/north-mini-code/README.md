---
name: North Mini Code
params:
  total: 30
  active: 3
---

```bash
docker run \
  --name north-mini-code \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -e VLLM_NO_USAGE_STATS=1 \
  --entrypoint /bin/bash \
  vllm/vllm-openai:nightly \
  -c "pip install cohere_melody && python3 -m vllm.entrypoints.openai.api_server \
    --model CohereLabs/North-Mini-Code-1.0 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name north-mini-code \
    --max-model-len 256K \
    --reasoning-parser cohere_command4 \
    --enable-auto-tool-choice \
    --tool-call-parser cohere_command4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --trust-remote-code"
```
