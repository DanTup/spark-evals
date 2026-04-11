# DGX Spark Evals

## Running Evals

First clone this repo and `cd` into the repository root.

```
git clone https://github.com/DanTup/spark-evals
cd spark-evals
```

Set env variables for the URL, model name, and results folder name.

```bash
export EVAL_BASE_URL="http://host.docker.internal:8111/v1"
export EVAL_MODEL="qwen35"
export EVAL_RESULTS_FOLDER="qwen35_35b_a3b_fp8"
```

Run the evals in a container. The `./results` folder will be mounted into the container to record the results.

The evals can take a long time, so you might want to run them inside `tmux` or something :)

You can add `--limit 2` after `inspect eval-set` if you want to verify everything works on a smaller set of tasks before running the entire batch.

You might need to play around with `--max-connections`, `--max-samples`, `--max-tasks` to balance throughput and errors (for example set `--max-connections` and `--max-samples` to match `--max-num-seqs` with `--max-tasks=1`).

```bash
docker run --rm -it \
	--add-host host.docker.internal:host-gateway \
	-v "$(pwd)/results:/results" \
	-e OPENAI_BASE_URL="${EVAL_BASE_URL}" \
	-e OPENAI_API_KEY="NONE" \
	-e INSPECT_EVAL_MODEL="openai/$SERVER_MODEL_NAME" \
	-e EVAL_RESULTS_FOLDER="${EVAL_RESULTS_FOLDER}" \
	-e DEBIAN_FRONTEND="noninteractive" \
	ubuntu \
	bash -lc '
		set -euo pipefail
		apt-get update
		apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
		python3 -m pip install --break-system-packages openai inspect-evals
		mkdir -p "/results/$EVAL_RESULTS_FOLDER"
		inspect eval-set \
			--log-dir "/results/$EVAL_RESULTS_FOLDER" --log-format json --log-dir-allow-dirty \
			--no-log-realtime --no-log-samples --no-log-images --log-buffer 200 --no-score-display --no-fail-on-error \
			--sandbox local --epochs 3 --epochs-reducer median --time-limit 1800 --max-connections 15 --max-samples 15 --max-tasks 1 \
			inspect_evals/arc_challenge inspect_evals/mbpp
	'
```

When the run is complete, create a `README.md` inside your new results folder that includes the full command you used to run the model, along with some YAML frontmatter with a name and a list of any flags that may affect the accuracy.

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
