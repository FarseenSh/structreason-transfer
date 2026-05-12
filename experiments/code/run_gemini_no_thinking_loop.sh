#!/bin/bash
# Run from repo root after activating your venv and exporting
# GOOGLE_APPLICATION_CREDENTIALS to point at your Vertex AI service-account JSON.
set -euo pipefail
: "${GOOGLE_APPLICATION_CREDENTIALS:?Set GOOGLE_APPLICATION_CREDENTIALS to your Vertex AI service-account JSON path}"

TARGET=8620
RESULTS="experiments/results/gemini-31-pro-nothinking/raw_results.jsonl"

while true; do
    VALID=$(python -c "
import json
v=0
try:
    with open('$RESULTS') as f:
        for l in f:
            if json.loads(l).get('raw_answer') is not None: v+=1
except: pass
print(v)
" 2>/dev/null)

    echo "============================================"
    echo "Valid: $VALID / $TARGET"
    echo "============================================"

    if [ "$VALID" -ge "$TARGET" ]; then
        echo "ALL DONE!"
        break
    fi

    python -c "
import json
path='$RESULTS'
try:
    results=[json.loads(l) for l in open(path) if json.loads(l).get('raw_answer') is not None]
    with open(path,'w') as f:
        for r in results: f.write(json.dumps(r,default=str)+'\n')
    print(f'Cleaned to {len(results)} valid')
except: print('No file yet')
"

    echo "Waiting 60s for rate limit reset..."
    sleep 60

    python -u experiments/code/run_gemini_no_thinking.py

    echo "Run finished. Looping..."
done
