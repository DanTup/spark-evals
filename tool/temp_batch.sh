# Set these env vars for the model
export EVAL_BASE_URL="http://192.168.0.132:8111/v1"
export EVAL_MODEL="qwen3-coder"

mkdir -p ~/inspect-evals
cd ~/inspect-evals

export OPENAI_BASE_URL="${EVAL_BASE_URL}"
export OPENAI_API_KEY="NONE"
export INSPECT_EVAL_MODEL="openai/$EVAL_MODEL"
export DEBIAN_FRONTEND="noninteractive"
export PATH=$PATH:~/.local/bin


for run_number in $(seq 1 10); do
  export EVAL_RESULTS_FOLDER="qwen3-coder-next-fp8-5epochs-run${run_number}"
  mkdir -p "results/$EVAL_RESULTS_FOLDER"
  inspect eval-set \
    --log-dir "results/$EVAL_RESULTS_FOLDER" --no-fail-on-error \
    --time-limit 1800 --max-tasks 1 --max-connections 6 --max-subprocesses 8 --max-sandboxes 8 --message-limit 1000 \
    --limit 1-20 --epochs 5 --epochs-reducer median \
  inspect_evals/theagentcompany inspect_evals/bfcl inspect_evals/ifevalcode inspect_evals/bigcodebench \
  -T "categories=['exec_parallel_multiple','irrelevance']" -T "languages=typescript"
done
