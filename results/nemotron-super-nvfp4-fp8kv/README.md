---
name: Nemotron 3 Super 120B-A12B NVFP4
params:
  total: 120
  active: 12
flags:
  quantization: fp4
  kv-cache-dtype: fp8
---

Adapted from https://github.com/NVIDIA-NeMo/Nemotron/tree/main/usage-cookbook/Nemotron-3-Super/SparkDeploymentGuide.

Requires the reasoning parser to be downloaded and mounted.

```bash
docker run \
  --name nemo-super \
  -d --gpus all -p 8111:8000 \
  -v ~/ext/cache/huggingface:/root/.cache/huggingface \
  -e VLLM_NO_USAGE_STATS=1 \
  -e VLLM_NVFP4_GEMM_BACKEND=marlin \
  -e VLLM_ALLOW_LONG_MAX_MODEL_LEN=1 \
  -e VLLM_FLASHINFER_ALLREDUCE_BACKEND=trtllm \
  -e VLLM_USE_FLASHINFER_MOE_FP4=0 \
  --ulimit memlock=-1 --ulimit stack=67108864 --shm-size=64gb \
  vllm/vllm-openai:gemma4-cu130 \
  nvidia/NVIDIA-Nemotron-3-Super-120B-A12B-NVFP4 \
    --served-model-name nemo-super \
    --gpu-memory-utilization 0.90 \
    --async-scheduling \
    --dtype auto \
    --kv-cache-dtype fp8 \
    --tensor-parallel-size 1 \
    --pipeline-parallel-size 1 \
    --data-parallel-size 1 \
    --trust-remote-code \
    --enable-chunked-prefill \
    --max-num-seqs 10 \
    --max-model-len 1000000 \
    --moe-backend marlin \
    --mamba_ssm_cache_dtype float32 \
    --quantization fp4 \
    --enable-auto-tool-choice \
    --tool-call-parser qwen3_coder \
    --reasoning-parser-plugin "/root/.cache/huggingface/downloaded_parsers/nemo_super_v3_reasoning_parser.py" \
    --reasoning-parser super_v3 \
    --speculative_config '{"method":"mtp","num_speculative_tokens":3,"moe_backend":"triton"}'
```
