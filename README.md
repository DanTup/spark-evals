# DGX Spark Evals

Some basic evals run on various models that fit on a single DGX Spark.

## Leaderboard

`Overall` is the sample-weighted pass rate across all benchmarks so every scored sample counts equally.

<!-- LEADERBOARD -->
| name | bfcl | bigcodebench | IfEvalCode | Overall |
| --- | ---: | ---: | ---: | ---: |
| [Gemma4 31B](results/gemma4-31b-with-mtp/)<br>speculative-config=gemma-4-31B-it-assistant(4)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>2h 30m, 504k in, 613k out</nobr> | <nobr>76.0%</nobr> | ***<nobr>72.0%</nobr>*** | ***<nobr>20.0%</nobr>***<br>ts: <nobr>38.0%</nobr> / <nobr>38.0%</nobr> | ***<nobr>48.8%</nobr>*** |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-a3b-fp8-fp8kv/)<br>kv-cache-dtype=fp8<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>10h 40m, 569k in, 5,229k out</nobr> | <nobr>76.0%</nobr> | <nobr>60.0%</nobr> | ***<nobr>20.0%</nobr>***<br>ts: <nobr>38.0%</nobr> / ***<nobr>50.0%</nobr>*** | ***<nobr>48.8%</nobr>*** |
| [Gemma4 31B](results/gemma4-31b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>9h 44m, 495k in, 550k out</nobr> | <nobr>78.0%</nobr> | ***<nobr>72.0%</nobr>*** | <nobr>18.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>38.0%</nobr> | <nobr>48.4%</nobr> |
| [Qwen3.6 35B-A3B FP8](results/qwen36-35b-a3b-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>9h 42m, 569k in, 5,247k out</nobr> | <nobr>78.0%</nobr> | <nobr>64.0%</nobr> | <nobr>18.0%</nobr><br>ts: <nobr>38.0%</nobr> / <nobr>44.0%</nobr> | <nobr>48.4%</nobr> |
| [Qwen3.6 35B-A3B NVFP4](results/qwen36-35b-a3b-nvfp4/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>8h 47m, 571k in, 5,334k out</nobr> | ***<nobr>80.0%</nobr>*** | <nobr>64.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>36.0%</nobr> / <nobr>44.0%</nobr> | <nobr>47.2%</nobr> |
| [Gemma4 26B-A4B](results/gemma4-26b-a4b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>3h 43m, 503k in, 752k out</nobr> | ***<nobr>80.0%</nobr>*** | <nobr>62.0%</nobr> | <nobr>18.0%</nobr><br>ts: <nobr>30.0%</nobr> / <nobr>44.0%</nobr> | <nobr>46.8%</nobr> |
| [Qwen3.6 27B FP8](results/qwen36-27b-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>19h 58m, 507k in, 3,112k out</nobr> | <nobr>78.0%</nobr> | <nobr>66.0%</nobr> | <nobr>18.0%</nobr><br>ts: ***<nobr>42.0%</nobr>*** / <nobr>30.0%</nobr> | <nobr>46.8%</nobr> |
| [Gemma4 31B](results/gemma4-31b-qat-with-mtp/)<br>qat-w4a16-ct speculative-config=gemma-4-31B-it-qat-q4_0-unquantized-assistant(4)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>1h 15m, 504k in, 631k out</nobr> | <nobr>78.0%</nobr> | <nobr>70.0%</nobr> | <nobr>16.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>32.0%</nobr> | <nobr>45.6%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b-nothink/)<br>enable_thinking=False<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>4h 14m, 569k in, 702k out</nobr> | <nobr>78.0%</nobr> | <nobr>64.0%</nobr> | <nobr>16.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>36.0%</nobr> | <nobr>45.2%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b-dflash/)<br>speculative-config=dflash(15)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>25h 11m, 478k in, 2,706k out</nobr> | <nobr>78.0%</nobr> | <nobr>68.0%</nobr> | <nobr>16.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>26.0%</nobr> | <nobr>44.0%</nobr> |
| [Qwen3.6 35B-A3B](results/qwen36-35b-a3b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>19h 51m, 508k in, 4,037k out</nobr> | <nobr>76.0%</nobr> | <nobr>62.0%</nobr> | <nobr>10.0%</nobr><br>ts: <nobr>28.0%</nobr> / <nobr>38.0%</nobr> | <nobr>42.8%</nobr> |
| [Qwen3 Coder Next FP8](results/qwen3-coder-next-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>2h 14m, 567k in, 681k out</nobr> | <nobr>78.0%</nobr> | <nobr>62.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>24.0%</nobr> / <nobr>34.0%</nobr> | <nobr>42.0%</nobr> |
| [Intern S2 Preview](results/intern-s2-preview/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>12h 17m, 547k in, 2,815k out</nobr> | <nobr>72.0%</nobr> | <nobr>64.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>20.0%</nobr> / <nobr>28.0%</nobr> | <nobr>38.4%</nobr> |
| [Qwen3.6 27B](results/qwen36-27b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>34h 19m, 422k in, 1,986k out</nobr> | <nobr>78.0%</nobr> | <nobr>62.0%</nobr> | <nobr>12.0%</nobr><br>ts: <nobr>22.0%</nobr> / <nobr>14.0%</nobr> | <nobr>37.6%</nobr> |
| [North Mini Code](results/north-mini-code/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>31h 31m, 441k in, 1,742k out</nobr> | <nobr>68.0%</nobr> | <nobr>54.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>26.0%</nobr> / <nobr>14.0%</nobr> | <nobr>34.0%</nobr> |
| [Nemotron3 Nano Omni 30B-A3B BF16](results/nemo-nano-omni-bf16/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>15h 35m, 537k in, 1,719k out</nobr> | <nobr>76.0%</nobr> | <nobr>54.0%</nobr> | <nobr>4.0%</nobr><br>ts: <nobr>10.0%</nobr> / <nobr>18.0%</nobr> | <nobr>32.4%</nobr> |
| [Qwen AgentWorld 35B A3B](results/qwen-agentworld-35b-a3b/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>48h 27m, 287k in, 1,869k out</nobr> | <nobr>74.0%</nobr> | <nobr>58.0%</nobr> | <nobr>4.0%</nobr><br>ts: <nobr>10.0%</nobr> / <nobr>6.0%</nobr> | <nobr>30.4%</nobr> |
| [Laguna S.2](results/laguna-s2/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>21h 7m, 480k in, 1,818k out</nobr> | <nobr>30.0%</nobr> | <nobr>52.0%</nobr> | <nobr>10.0%</nobr><br>ts: <nobr>24.0%</nobr> / <nobr>28.0%</nobr> | <nobr>28.8%</nobr> |
| [Laguna XS.2](results/laguna-xs2/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>6h 35m, 573k in, 1,783k out</nobr> | <nobr>16.0%</nobr> | <nobr>54.0%</nobr> | <nobr>14.0%</nobr><br>ts: <nobr>22.0%</nobr> / <nobr>24.0%</nobr> | <nobr>26.0%</nobr> |
| [Nemotron3 Super 120B-A12B NVFP4](results/nemo-super-nvfp4/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>14h 37m, 535k in, 1,595k out</nobr> | <nobr>12.0%</nobr> | <nobr>60.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>32.0%</nobr> / <nobr>18.0%</nobr> | <nobr>26.0%</nobr> |
| [Ornith 35B FP8](results/ornith-35b-fp8/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>48h 24m, 329k in, 1,124k out</nobr> | ***<nobr>80.0%</nobr>*** | <nobr>0.0%</nobr> | <nobr>8.0%</nobr><br>ts: <nobr>18.0%</nobr> / <nobr>12.0%</nobr> | <nobr>23.6%</nobr> |
| [Deepseek v4 Flash](results/deepseek-v4-flash/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>31h 48m, 222k in, 103k out</nobr> | <nobr>70.0%</nobr> |  | <nobr>0.0%</nobr><br>ts: <nobr>0.0%</nobr> / <nobr>0.0%</nobr> | <nobr>17.5%</nobr> |
| [Gemma4 Diffusion](results/gemma4-diffusion/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>20m 24s, 504k in, 208k out</nobr> | <nobr>78.0%</nobr> | <nobr>0.0%</nobr> | <nobr>2.0%</nobr><br>ts: <nobr>2.0%</nobr> / <nobr>4.0%</nobr> | <nobr>17.2%</nobr> |
| [Orion GRM 2.6 Plus](results/orion-grm-2-6/)<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr>88h 58m</nobr> | <nobr>20.0%</nobr> | <nobr>0.0%</nobr> | <nobr>0.0%</nobr><br>ts: <nobr>0.0%</nobr> / <nobr>0.0%</nobr> | <nobr>4.0%</nobr> |
| [Jackrong Qwopus 3.6 27B](results/qwen36-qwopus-preview/)<br>v1-preview<br>&nbsp;&nbsp;&nbsp;&nbsp;<nobr></nobr> |  |  |  | <nobr>0.0%</nobr> |
<!-- /LEADERBOARD -->

## Running Evals

Because some of these evals require installing packages and also spawn Docker containers, I recommend running everything inside a VM or on a spare machine. This does not need to run on the DGX Spark (and if you're running a large model, it might be better to run it on another machine). The instructions below assume a clean Ubuntu installation (I used `multipass launch --cpus 12 --disk 50G --memory 32G --name inspect-evals --mount ~/inspect-eval-results:/home/ubuntu/inspect-evals/results` to create a VM for this).

### Set up Dependencies

```bash
export PATH=$PATH:~/.local/bin
sudo apt-get update
sudo apt-get install -y --no-install-recommends ca-certificates curl jq python3 python3-pip python-is-python3
python3 -m pip install --break-system-packages openai anyio==4.13.0 textual==8.2.5 inspect-ai==0.3.220 inspect-evals==0.11.0 inspect-evals[ifevalcode]

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
export EVAL_MODEL="gemma4"
export EVAL_RESULTS_FOLDER="gemma4-31b-with-mtp"

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
  inspect_evals/bfcl inspect_evals/ifevalcode inspect_evals/bigcodebench \
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
