#!/bin/bash
# Run weighted-probe experiment across all models × all counterfactuals.
set -e
cd "$(dirname "$0")/.."

INSTANCES="facet-neg-cf-001 facet-neg-cf-002 facet-neg-cf-003"

# Claude: already ran Opus + Sonnet on CF-002; need to complete the matrix
for inst in $INSTANCES; do
  for model in opus sonnet; do
    # Skip already-run combinations
    if ls results/weighted-probe/${inst}-claude-${model}-*.json 2>/dev/null | head -1 > /dev/null; then
      echo "[skip] $inst $model (already done)"
      continue
    fi
    echo "=== claude $model $inst ==="
    python3 eval/run_weighted_probe.py --instance $inst --backend claude --model $model 2>&1 | tail -3
  done
done

# Bedrock models
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
