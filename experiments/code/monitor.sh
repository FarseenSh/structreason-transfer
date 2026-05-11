#!/bin/bash
LOG="/Users/farseenshaikh/surgellm-2026-structreason/experiments/results/monitor.log"
while true; do
    echo "$(date '+%H:%M:%S') | DS: $(wc -l < experiments/results/deepseek-v3.2/raw_results.jsonl 2>/dev/null || echo 0)/6896 | Qwen: $(wc -l < experiments/results/qwen3.5-plus/raw_results.jsonl 2>/dev/null || echo 0)/8620" >> "$LOG"
    # Check for errors in last 10 lines
    if [ -f experiments/results/qwen3.5-plus/raw_results.jsonl ]; then
        ERRS=$(tail -20 experiments/results/qwen3.5-plus/raw_results.jsonl | grep -c '"error"' 2>/dev/null || echo 0)
        if [ "$ERRS" -gt 5 ]; then
            echo "$(date '+%H:%M:%S') | WARNING: Qwen high error rate ($ERRS/20)" >> "$LOG"
        fi
    fi
    sleep 600
done
