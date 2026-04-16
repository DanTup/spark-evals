# DGX Spark Evals

Some basic evals run on various models that fit on a single DGX Spark.

## Leaderboard

<!-- LEADERBOARD -->
| name | AgentBench | ARC Challenge | IfEvalCode | MBPP |
| --- | ---: | ---: | ---: | ---: |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-fp8/README.md) | <u>**31.2%**</u><br>*4h 45m* | **97.5%**<br>*2h 52m* |  | **93.8%**<br>*2h 6m* |
| [Qwen3.5 35B-A3B FP8](results/qwen35-35b-fp8/README.md) | **28.0%**<br>*2h 19m* | <u>**98.0%**</u><br>*4h 10m* |  | **94.9%**<br>*2h 13m* |
| [Qwen3 Coder Next FP8](results/qwen3-coder-next/README.md) | **29.6%**<br>*1h 27m* | **96.2%**<br>*1h 10m* | <u>**11.0%**</u><br>*8h 11m*<br>ts: <u>**0.0%**</u> / <u>**30.0%**</u><br>c#: <u>**24.3%**</u> / <u>**3.9%**</u><br>py: <u>**54.3%**</u> / <u>**36.2%**</u><br>sh: <u>**35.0%**</u> / <u>**52.0%**</u> | **87.5%**<br>*1h 13m* |
| [Nemotron 3 Super 120B-A12B NVFP4](results/nemotron-super-nvfp4-fp8kv/README.md)<br>quantization=fp4 kv-cache-dtype=fp8 | **27.2%**<br>*11h 44m* | **97.2%**<br>*5h 41m* |  | <u>**95.7%**</u><br>*2h 14m* |
| [Gemma4 26B-A4B](results/gemma4-26b/README.md) | **25.6%**<br>*9h 12m* | **97.4%**<br>*2h 48m* |  | **90.7%**<br>*1h 8m* |
| [Gemma4 E2B](results/gemma4-e2b/README.md) |  | **86.4%**<br>*22m 44s* |  | **72.8%**<br>*4m 31s* |
<!-- /LEADERBOARD -->

## Running Evals

Because some of these evals require installing packages and also spawn Docker containers, I recommend running everything inside a VM to avoid changing anything on your host. This does not need to run on the DGX Spark (an if you're running a large model, it might be better to run it on another machine).

On Ubuntu you can use [multipass](https://canonical.com/multipass) to create a VM and mount a folder into it to collect the results:

### Create the VM

```bash
multipass launch -n inspect-ai-evals --cpus 4 --disk 100gb --memory 20gb --mount /home/danny/inspect-evals

# I'd recommend doing this in tmux so you can detach and come back later
multipass shell inspect-ai-evals
```

### Set up the VM

Once inside the VM, install the dependencies and Docker:

```bash
export PATH=$PATH:~/.local/bin
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
python3 -m pip install --break-system-packages openai inspect-evals inspect-evals[ifevalcode] inspect-evals[swe_bench] inspect-evals[swe_lancer]

curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x get-docker.sh
./get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
rm get-docker.sh
```

### Configure the LLM Endpoint

Now, each time you want to run evals, set some env vars with the details of the LLM endpoint:

```bash
export EVAL_BASE_URL="http://192.168.0.132:8111/v1"
export EVAL_MODEL="qwen36"
export EVAL_RESULTS_FOLDER="qwen36-35b-a3b-fp8"
export EVAL_MAX_CONNECTIONS="10"
```

### Start the Evals

```bash
# IMPORTANT: Change into the mounted folder if using the VM to ensure the results persist outside of the VM!
cd ~/inspect-evals

export OPENAI_BASE_URL="${EVAL_BASE_URL}"
export OPENAI_API_KEY="NONE"
export INSPECT_EVAL_MODEL="openai/$EVAL_MODEL"
export EVAL_RESULTS_FOLDER="${EVAL_RESULTS_FOLDER}"
export EVAL_MAX_CONNECTIONS="${EVAL_MAX_CONNECTIONS}"
export DEBIAN_FRONTEND="noninteractive"
export PATH=$PATH:~/.local/bin

mkdir -p "results/$EVAL_RESULTS_FOLDER"
inspect eval-set \
	--log-dir "results/$EVAL_RESULTS_FOLDER" --log-format json --log-dir-allow-dirty \
	--no-log-realtime --no-log-samples --no-log-images --log-buffer 200 --no-score-display --no-fail-on-error \
	--sandbox docker --epochs 3 --epochs-reducer median --time-limit 1800 --max-connections "$EVAL_MAX_CONNECTIONS" --max-samples "$EVAL_MAX_CONNECTIONS" --max-tasks 1 \
	--max-sandboxes 4 --max-subprocesses 4 \
	inspect_evals/agent_bench_os inspect_evals/mbpp inspect_evals/arc_challenge inspect_evals/ifevalcode inspect_evals/swe_lancer
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

## Clean up the VM

When you've finished running, you can stop the VM:

```bash
multipass stop inspect-ai-evals
```

If you're not running any more, you can also delete:

```bash
multipass delete inspect-ai-evals
multipass purge # actually delete the marked VMs
```
