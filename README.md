# DGX Spark Evals

Some basic evals run on various models that fit on a single DGX Spark.

## Leaderboard

`Overall` is the sample-weighted pass rate across all benchmarks so every scored sample counts equally.

<!-- LEADERBOARD -->
| name | bfcl | bigcodebench | IfEvalCode | The<br>Agent<br>Co | Overall |
| --- | ---: | ---: | ---: | ---: | ---: |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-a3b-fp8-fp8kv/)<br>kv-cache-dtype=fp8<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>13h 55m, 125,917k in, 6,129k out</nobr> | <nobr>76.0%</nobr> | <nobr>60.0%</nobr> | ***<nobr>20.0%</nobr>***<br>ts: ***<nobr>38.0%</nobr>*** / ***<nobr>50.0%</nobr>*** | ***<nobr>20.0%</nobr>*** | ***<nobr>47.7%</nobr>*** |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-a3b-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>13h 41m, 117,175k in, 6,095k out</nobr> | <nobr>78.0%</nobr> | <nobr>64.0%</nobr> | <nobr>18.0%</nobr><br>ts: ***<nobr>38.0%</nobr>*** / <nobr>44.0%</nobr> | <nobr>10.0%</nobr> | <nobr>46.9%</nobr> |
| [Gemma4 31B](results/gemma4-31b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>14h 57m, 37,212k in, 690k out</nobr> | <nobr>78.0%</nobr> | ***<nobr>72.0%</nobr>*** | <nobr>18.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>38.0%</nobr> | <nobr>0.0%</nobr> | <nobr>46.5%</nobr> |
| [Gemma4 31B](results/gemma4-31b-with-mtp/)<br>speculative-config=gemma-4-31B-it-assistant(4)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>8h 15m, 35,847k in, 722k out</nobr> | <nobr>78.0%</nobr> | <nobr>70.0%</nobr> | <nobr>18.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>40.0%</nobr> | <nobr>0.0%</nobr> | <nobr>46.5%</nobr> |
| [Qwen3.6 35B-A3B NVFP4](results/qwen36-35b-a3b-nvfp4/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>12h 42m, 118,842k in, 6,245k out</nobr> | ***<nobr>80.0%</nobr>*** | <nobr>64.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>44.0%</nobr> | <nobr>10.0%</nobr> | <nobr>45.8%</nobr> |
| [Gemma4 26B-A4B](results/gemma4-26b-a4b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>9h 10m, 469,371k in, 1,009k out</nobr> | ***<nobr>80.0%</nobr>*** | <nobr>62.0%</nobr> | <nobr>18.0%</nobr><br>ts: <nobr>30.0%</nobr> / <nobr>44.0%</nobr> | <nobr>0.0%</nobr> | <nobr>45.0%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b-nothink/)<br>enable_thinking=False<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>9h 23m, 44,522k in, 1,045k out</nobr> | <nobr>78.0%</nobr> | <nobr>64.0%</nobr> | <nobr>16.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>36.0%</nobr> | <nobr>10.0%</nobr> | <nobr>43.8%</nobr> |
| [Qwen3.6 27B FP8](results/qwen36-27b-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>26h 51m, 44,449k in, 3,554k out</nobr> | <nobr>78.0%</nobr> | <nobr>66.0%</nobr> | <nobr>14.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>26.0%</nobr> | <nobr>10.0%</nobr> | <nobr>42.7%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b-dflash/)<br>speculative-config=dflash(15)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>30h 52m, 23,543k in, 2,925k out</nobr> | <nobr>78.0%</nobr> | <nobr>68.0%</nobr> | <nobr>16.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>26.0%</nobr> | <nobr>0.0%</nobr> | <nobr>42.3%</nobr> |
| [Qwen3.6 35B-A3B](results/qwen36-35b-a3b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>24h 20m, 98,688k in, 4,815k out</nobr> | <nobr>76.0%</nobr> | <nobr>62.0%</nobr> | <nobr>10.0%</nobr><br>ts: <nobr>28.0%</nobr> / <nobr>38.0%</nobr> | ***<nobr>20.0%</nobr>*** | <nobr>41.9%</nobr> |
| [Qwen3 Coder Next FP8](results/qwen3-coder-next-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>5h 33m, 136,584k in, 1,253k out</nobr> | <nobr>78.0%</nobr> | <nobr>62.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>24.0%</nobr> / <nobr>34.0%</nobr> | ***<nobr>20.0%</nobr>*** | <nobr>41.2%</nobr> |
| [Intern S2 Preview](results/intern-s2-preview/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>17h 5m, 105,441k in, 3,930k out</nobr> | <nobr>72.0%</nobr> | <nobr>64.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>20.0%</nobr> / <nobr>28.0%</nobr> | <nobr>10.0%</nobr> | <nobr>37.3%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>39h 51m, 43,822k in, 2,398k out</nobr> | <nobr>78.0%</nobr> | <nobr>62.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>22.0%</nobr> / <nobr>14.0%</nobr> | <nobr>10.0%</nobr> | <nobr>36.5%</nobr> |
| [Nemotron3 Nano Omni 30B-A3B BF16](results/nemo-nano-omni-bf16/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>21h 37m, 20,238k in, 2,593k out</nobr> | <nobr>76.0%</nobr> | <nobr>54.0%</nobr> | <nobr>4.0%</nobr><br>ts: <nobr>10.0%</nobr> / <nobr>18.0%</nobr> | <nobr>0.0%</nobr> | <nobr>31.2%</nobr> |
| [Laguna XS.2](results/laguna-xs2/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>11h 8m, 75,649k in, 2,506k out</nobr> | <nobr>16.0%</nobr> | <nobr>54.0%</nobr> | <nobr>14.0%</nobr><br>ts: <nobr>22.0%</nobr> / <nobr>24.0%</nobr> | <nobr>10.0%</nobr> | <nobr>25.4%</nobr> |
| [Nemotron3 Super 120B-A12B NVFP4](results/nemo-super-nvfp4/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>20h 25m, 24,579k in, 1,973k out</nobr> | <nobr>12.0%</nobr> | <nobr>60.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>18.0%</nobr> | <nobr>10.0%</nobr> | <nobr>25.4%</nobr> |
| [Deepseek v4 Flash](results/deepseek-v4-flash/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>37h 50m, 5,271k in, 226k out</nobr> | <nobr>70.0%</nobr> |  | <nobr>0.0%</nobr><br>ts: <nobr>0.0%</nobr> / <nobr>0.0%</nobr> | <nobr>0.0%</nobr> | <nobr>16.7%</nobr> |
| [Jackrong Qwopus 3.6 27B](results/qwen36-qwopus-preview/)<br>v1-preview<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr></nobr> |  |  |  |  | <nobr>0.0%</nobr> |
<!-- /LEADERBOARD -->

## Running Evals

Because some of these evals require installing packages and also spawn Docker containers, I recommend running everything inside a VM or on a spare machine. This does not need to run on the DGX Spark (and if you're running a large model, it might be better to run it on another machine). The instructions below assume a clean Ubuntu installation (I used `multipass launch --cpus 12 --disk 50G --memory 32G --name inspect-evals --mount ~/inspect-eval-results:/home/ubuntu/inspect-evals/results` to create a VM for this).

### Set up Dependencies

```bash
export PATH=$PATH:~/.local/bin
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
python3 -m pip install --break-system-packages openai inspect-evals inspect-evals[theagentcompany] inspect-evals[ifevalcode]

curl -fsSL https://get.docker.com -o get-docker.sh
chmod +x get-docker.sh
./get-docker.sh
sudo usermod -aG docker $USER
newgrp docker
rm get-docker.sh
```

### Run the Evals

Each time you want to run evals, set some env vars with the details of the LLM endpoint:

```bash
# Set these env vars for the model
export EVAL_BASE_URL="http://192.168.0.132:8111/v1"
export EVAL_MODEL="laguna"
export EVAL_RESULTS_FOLDER="laguna-xs2"

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
  --time-limit 1800 --max-tasks 1 --max-connections 6 --max-subprocesses 8 --max-sandboxes 8 --message-limit 1000 \
  --limit 1-50 --epochs 7 --epochs-reducer median \
  inspect_evals/theagentcompany inspect_evals/bfcl inspect_evals/ifevalcode inspect_evals/bigcodebench \
  -T "categories=['exec_parallel_multiple','irrelevance']" -T "languages=typescript"
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
