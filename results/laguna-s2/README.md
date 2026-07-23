---
name: Laguna S.2
params:
  total: 118
  active: 9
---

```bash
docker run \
  --name laguna \
  -d \
  --gpus all \
  --restart unless-stopped \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -v ~/ext/cache/vllm:/root/.cache/vllm \
  -v ~/ext/cache/triton:/root/.cache/triton \
  -v ~/ext/cache/cute:/root/.cache/cute \
  -e VLLM_NO_USAGE_STATS=1 \
  -e CUTE_DSL_ARCH=sm_121a \
  -e MAX_JOBS=4 \
  --entrypoint /bin/bash \
  vllm/vllm-openai:latest \
  -c "pip install \
        'flashinfer-python==0.6.15.dev20260712' \
        'flashinfer-cubin==0.6.15.dev20260712' \
        'flashinfer-jit-cache==0.6.15.dev20260712' \
        --extra-index-url https://flashinfer.ai/whl/nightly/ \
        --extra-index-url https://flashinfer.ai/whl/nightly/cu130/ \
    && vllm serve poolside/Laguna-S-2.1-NVFP4 \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name laguna \
    --max-model-len 256K \
    --tool-call-parser poolside_v1 \
    --reasoning-parser poolside_v1 \
    --enable-auto-tool-choice \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 10 \
    --enable-prefix-caching \
    --speculative-config '{\"model\":\"poolside/Laguna-S-2.1-DFlash-NVFP4\",\"num_speculative_tokens\":15,\"method\":\"dflash\"}'"
```
