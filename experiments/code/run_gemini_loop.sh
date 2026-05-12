#!/bin/bash
# Auto-restart Gemini until all 8620 results are valid
# Cleans errors between runs, waits 60s for rate limit reset
#
# Run from repo root after activating your venv and exporting
# GOOGLE_APPLICATION_CREDENTIALS to point at your Vertex AI service-account JSON.
set -euo pipefail
: "${GOOGLE_APPLICATION_CREDENTIALS:?Set GOOGLE_APPLICATION_CREDENTIALS to your Vertex AI service-account JSON path}"

TARGET=8620
RESULTS="experiments/results/gemini-31-pro/raw_results.jsonl"

while true; do
    # Count valid results
    VALID=$(python -c "
import json
v=0
with open('$RESULTS') as f:
    for l in f:
        if json.loads(l).get('raw_answer') is not None: v+=1
print(v)
" 2>/dev/null || echo "0")

    echo "============================================"
    echo "Valid: $VALID / $TARGET"
    echo "============================================"

    if [ "$VALID" -ge "$TARGET" ]; then
        echo "ALL DONE!"
        break
    fi

    # Clean errors
    python -c "
import json
path='$RESULTS'
results=[json.loads(l) for l in open(path) if json.loads(l).get('raw_answer') is not None]
with open(path,'w') as f:
    for r in results: f.write(json.dumps(r,default=str)+'\n')
print(f'Cleaned to {len(results)} valid')
"

    # Wait for rate limit reset
    echo "Waiting 60s for rate limit reset..."
    sleep 60

    # Run
    python -u experiments/code/run_gemini.py

    echo "Run finished. Looping..."
done
