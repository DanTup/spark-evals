# DGX Spark Evals

Some basic evals run on various models that fit on a single DGX Spark.

## Leaderboard

<!-- LEADERBOARD -->
| name | AgentBench | bfcl |
| --- | ---: | ---: |
| [Qwen3.6 27B](results/qwen36-27b/README.md) | <u>**59.3%**</u><br>*2h 41m* | **77.3%**<br>*1h 13m* |
| [Qwen3.6 27B](results/qwen36-27b-dflash/README.md)<br>speculative-config=dflash(15) | **58.0%**<br>*2h 42m* | **77.3%**<br>*48m 58s* |
| [Qwen3.6 27B FP8](results/qwen36-27b-fp8/README.md) | **58.7%**<br>*1h 44m* | **75.3%**<br>*37m 26s* |
| [Qwen3.6 27B](results/qwen36-27b-nothink/README.md)<br>enable_thinking=False | **56.0%**<br>*1h 40m* | <u>**78.0%**</u><br>*11m 52s* |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-a3b-fp8/README.md) | **55.3%**<br>*2h 9m* | <u>**78.0%**</u><br>*17m 3s* |
| [Qwen3.6 35B-A3B](results/qwen36-35b-a3b/README.md) | **52.7%**<br>*2h 34m* | <u>**78.0%**</u><br>*25m 5s* |
| [Qwen3.6 35B-A3B NVFP4](results/qwen36-35b-a3b-nvfp4/README.md) | **52.7%**<br>*2h 0m* | **77.3%**<br>*18m 32s* |
| [Gemma4 31B](results/gemma4-31b/README.md) | **45.3%**<br>*2h 4m* | **77.3%**<br>*19m 49s* |
| [Qwen3 Coder Next FP8](results/qwen3-coder-next-fp8/README.md) | **46.0%**<br>*32m 49s* |  |
| [Gemma4 26B-A4B](results/gemma4-26b-a4b/README.md) | **44.0%**<br>*2h 16m* |  |
<!-- /LEADERBOARD -->

## Running Evals

Because some of these evals require installing packages and also spawn Docker containers, I recommend running everything inside a VM or on a spare machine. This does not need to run on the DGX Spark (and if you're running a large model, it might be better to run it on another machine). The instructions below assume a clean Ubuntu installation.

### Set up Dependencies

```bash
export PATH=$PATH:~/.local/bin
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
python3 -m pip install --break-system-packages openai inspect-evals

curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x get-docker.sh
./get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
rm get-docker.sh
```

### Configure the LLM Endpoint

Each time you want to run evals, set some env vars with the details of the LLM endpoint:

```bash
export EVAL_BASE_URL="http://192.168.0.132:8111/v1"
export EVAL_MODEL="gemma4"
export EVAL_RESULTS_FOLDER="gemma4-26b-a4b"
```

### Start the Evals

```bash
mkdir -p ~/inspect-evals
cd ~/inspect-evals

export OPENAI_BASE_URL="${EVAL_BASE_URL}"
export OPENAI_API_KEY="NONE"
export INSPECT_EVAL_MODEL="openai/$EVAL_MODEL"
export DEBIAN_FRONTEND="noninteractive"
export PATH=$PATH:~/.local/bin

mkdir -p "results/$EVAL_RESULTS_FOLDER"
inspect eval-set \
  --log-dir "results/$EVAL_RESULTS_FOLDER" --log-format json --log-dir-allow-dirty \
  --no-log-realtime --no-log-samples --no-log-images --log-buffer 100 --no-score-display --no-fail-on-error \
  --time-limit 900 --max-tasks 1 --max-connections 4 --max-subprocesses 4 --max-sandboxes 4 --limit 1-50 --epochs 3 \
  inspect_evals/bfcl inspect_evals/agent_bench_os \
  -T "categories=['exec_parallel_multiple','irrelevance']"
```

### Create a PR

The JSON results will be available in the `results` folder. Copy them into a clone of this repo in the `results/` folder with a new folder for the model/variation you tested. Include the individual results JSON files (but not the full logs json or other metadata files), and a `README.md` containing the exact command used to launch the LLM inference engine with all flags, and some YAML frontmatter:

```
---
name: Nvidia Nemotron Super NVFP8
# Params in billions. For dense models, use `params: 100`
params:
  total: 120
  active: 12
# Any flags used that may affect accuracy
flags:
  quantization: fp4
  kv-cache-dtype: fp8
  mamba-ssm-cache-dtype: float32
---
```

Run `python3 tool/update_leaderboard.py` to update the leaderboard at the top of this readme.

Finally, open a PR to share the results!
