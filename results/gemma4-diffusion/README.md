---
name: Gemma4 Diffusion
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
  vllm/vllm-openai:gemma \
    google/diffusiongemma-26B-A4B-it \
    --host 0.0.0.0 \
    --gpu-memory-utilization 0.85 \
    --served-model-name gemma4 \
    --max-model-len 256k \
    --reasoning-parser gemma4 \
    --enable-auto-tool-choice \
    --tool-call-parser gemma4 \
    --enable-chunked-prefill \
    --max-num-batched-tokens 32768 \
    --max-num-seqs 4 \
    --enable-prefix-caching \
    --trust-remote-code \
    --hf-overrides '{"diffusion_sampler":"entropy_bound","diffusion_entropy_bound":0.1}' \
    --diffusion-config '{"canvas_length": 256}' \
    --chat-template examples/tool_chat_template_gemma4.jinja
```
