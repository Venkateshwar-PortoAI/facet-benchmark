#!/bin/bash
# Run the weighted-rank probe on the two new adversarial instances across all 8
# models. cf-002-adv is already done (run 2026-04-13); this script covers
# cf-001-adv and cf-003-adv. 16 API calls total.
set -e
cd "$(dirname "$0")/.."

INSTANCES="facet-neg-cf-001-adv facet-neg-cf-003-adv"

# Claude
for inst in $INSTANCES; do
  for model in opus sonnet; do
    if ls results/weighted-probe/${inst}-claude-${model}-*.json 2>/dev/null | head -1 > /dev/null; then
      echo "[skip] $inst $model (already done)"
      continue
    fi
    echo "=== claude $model $inst ==="
    python3 eval/run_weighted_probe.py --instance $inst --backend claude --model $model 2>&1 | tail -3
  done
done

# Bedrock
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

# Codex (GPT-5.4)
for inst in $INSTANCES; do
  echo "=== codex gpt-5.4 $inst ==="
  python3 eval/run_weighted_probe.py --instance $inst --backend codex --model gpt-5.4 2>&1 | tail -3
done

echo ""
echo "=== BATCH COMPLETE ==="
ls results/weighted-probe/ | wc -l | xargs echo "Total files:"
