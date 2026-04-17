# DGX Spark Evals

Some basic evals run on various models that fit on a single DGX Spark.

## Leaderboard

<!-- LEADERBOARD -->
| name | AgentBench | IfEvalCode |
| --- | ---: | ---: |
| [Qwen3 Coder Next FP8](results/qwen3-coder-next/README.md) | **29.6%**<br>*1h 27m* | <u>**11.0%**</u><br>*8h 11m*<br>ts: <u>**0.0%**</u> / **30.0%**<br>c#: <u>**24.3%**</u> / **3.9%**<br>py: <u>**54.3%**</u> / <u>**36.2%**</u><br>sh: **35.0%** / **52.0%** |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-fp8/README.md) | <u>**34.4%**</u><br>*1h 0m* | **8.7%**<br>*4h 59m*<br>ts: <u>**0.0%**</u> / <u>**37.0%**</u><br>c#: **17.0%** / <u>**6.0%**</u><br>sh: <u>**40.0%**</u> / <u>**59.0%**</u> |
| [Qwen3.5 35B-A3B FP8](results/qwen35-35b-fp8/README.md) | **28.0%**<br>*2h 19m* |  |
| [Nemotron 3 Super 120B-A12B NVFP4](results/nemotron-super-nvfp4-fp8kv/README.md)<br>quantization=fp4 kv-cache-dtype=fp8 | **27.2%**<br>*11h 44m* |  |
| [Gemma4 26B-A4B](results/gemma4-26b/README.md) | **27.2%**<br>*1h 28m* | **6.3%**<br>*2h 19m*<br>ts: <u>**0.0%**</u> / **29.0%**<br>c#: **20.0%** / **5.0%**<br>sh: **38.0%** / **51.0%** |
| [Gemma4 E2B](results/gemma4-e2b/README.md) | **20.0%**<br>*12m 58s* | **2.0%**<br>*18m 28s*<br>ts: <u>**0.0%**</u> / **26.0%**<br>c#: **8.0%** / **4.0%**<br>sh: **14.0%** / **51.0%** |
<!-- /LEADERBOARD -->

## Running Evals

The commands below only run a subset (100 samples) of each and only two epochs (keeping the highest score). This might lead to some variance in scores but avoids the benchmarks taking too long.

Because some of these evals require installing packages and also spawn Docker containers, I recommend running everything inside a VM or on a spare machine. This does not need to run on the DGX Spark (and if you're running a large model, it might be better to run it on another machine). The instructions below assume a clean Ubuntu installation.

### Set up Dependencies

```bash
export PATH=$PATH:~/.local/bin
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
python3 -m pip install --break-system-packages openai inspect-evals inspect-evals[ifevalcode]

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
export EVAL_RESULTS_FOLDER="gemma4-26b"
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
	--no-log-realtime --no-log-samples --no-log-images --log-buffer 500 --no-score-display --no-fail-on-error \
	--time-limit 1800 --max-tasks 1 --limit 1-300 \
	inspect_evals/ifevalcode inspect_evals/agent_bench_os \
	-T languages=typescript,csharp,shell -T samples-per-language=100
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
