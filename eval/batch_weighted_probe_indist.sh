#!/bin/bash
# Run weighted-probe experiment on the 3 anchor IN-DISTRIBUTION instances.
# This validates whether the weighted probe produces sensible weights on real
# cases (as opposed to just handling the "neutralized factor" instruction).
set -e
cd "$(dirname "$0")/.."

INSTANCES="facet-neg-0002 facet-neg-0003 facet-neg-0004"

for inst in $INSTANCES; do
  for model in opus sonnet; do
    echo "=== claude $model $inst ==="
    python3 eval/run_weighted_probe.py --instance $inst --backend claude --model $model 2>&1 | tail -3
  done
done

BEDROCK_MODELS=(
  "deepseek.v3.2"
  "mistral.mistral-large-3-675b-instruct"
  "qwen.qwen3-next-80b-a3b"
  "us.meta.llama4-maverick-17b-instruct-v1:0"
  "us.meta.llama4-scout-17b-instruct-v1:0"
)

for inst in $INSTANCES; do
  for model in "${BEDROCK_MODELS[@]}"; do
    echo "=== bedrock $model $inst ==="
    python3 eval/run_weighted_probe.py --instance $inst --backend bedrock --model "$model" 2>&1 | tail -3
  done
done

for inst in $INSTANCES; do
  echo "=== codex gpt-5.4 $inst ==="
  python3 eval/run_weighted_probe.py --instance $inst --backend codex --model gpt-5.4 2>&1 | tail -3
done

echo ""
echo "=== IN-DIST BATCH COMPLETE ==="
