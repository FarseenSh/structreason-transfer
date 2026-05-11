"""
Phase 3: Pilot validation — run ALL questions × 5 formats on DeepSeek V3.2 via OpenRouter.
Validates: API calls, scoring pipeline, output parsing, ground truth.
Checks for ceiling effect (>95% on any Q type → flag).
"""

import asyncio
import json
import os
import re
import time
import base64
import random
from pathlib import Path
from dotenv import load_dotenv
import aiohttp
import numpy as np
import pandas as pd

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # surgellm-2026-structreason/
load_dotenv(BASE_DIR / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = "deepseek/deepseek-v3.2"  # DeepSeek V3.2 on OpenRouter
API_URL = "https://openrouter.ai/api/v1/chat/completions"

QUESTION_DIR = BASE_DIR / "experiments" / "data" / "questions"
FORMAT_DIR = BASE_DIR / "experiments" / "data" / "formats"
RESULTS_DIR = BASE_DIR / "experiments" / "results"
RESULTS_DIR.mkdir(parents=True, exist_ok=True)
PILOT_DIR = RESULTS_DIR / "pilot"
PILOT_DIR.mkdir(parents=True, exist_ok=True)

FORMATS = ["table", "chart_text", "graph", "timeseries"]
# chart_image requires vision — DeepSeek V3.2 may not support it, run text formats first
# We'll test chart_image separately

PROMPT_TEMPLATE = """You are given data in the following format. Answer the question precisely.

{data}

Question: {question}

Answer with ONLY the answer value, no explanation."""

# Rate limiting
MAX_CONCURRENT = 40
RATE_LIMIT_DELAY = 0.05  # seconds between requests
RETRY_DELAYS = [2, 5, 15]  # backoff for retries


def load_questions():
    questions = []
    with open(QUESTION_DIR / "questions.jsonl") as f:
        for line in f:
            questions.append(json.loads(line))
    return questions


def load_format_data(sub_id, fmt):
    """Load formatted data for a sub-table."""
    if fmt == "chart_image":
        img_path = FORMAT_DIR / "chart_image" / f"{sub_id}.png"
        if img_path.exists():
            with open(img_path, "rb") as f:
                return base64.b64encode(f.read()).decode("utf-8")
        return None
    else:
        txt_path = FORMAT_DIR / fmt / f"{sub_id}.txt"
        if txt_path.exists():
            return txt_path.read_text()
        return None


async def call_api(session, data_content, question_text, fmt, semaphore,
                   is_image=False, retry=0):
    """Call OpenRouter API with rate limiting and retries."""
    async with semaphore:
        await asyncio.sleep(RATE_LIMIT_DELAY)

        if is_image:
            messages = [
                {"role": "user", "content": [
                    {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data_content}"}},
                    {"type": "text", "text": f"Answer the question precisely based on this chart.\n\nQuestion: {question_text}\n\nAnswer with ONLY the answer value, no explanation."}
                ]}
            ]
        else:
            prompt = PROMPT_TEMPLATE.format(data=data_content, question=question_text)
            messages = [{"role": "user", "content": prompt}]

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://structreason-transfer.research",
            "X-Title": "StructReason-Transfer Pilot"
        }
        payload = {
            "model": MODEL,
            "messages": messages,
            "max_tokens": 100,
            "temperature": 0,
        }

        try:
            async with session.post(API_URL, json=payload, headers=headers, timeout=60) as resp:
                if resp.status == 429:
                    if retry < len(RETRY_DELAYS):
                        await asyncio.sleep(RETRY_DELAYS[retry])
                        return await call_api(session, data_content, question_text,
                                            fmt, semaphore, is_image, retry+1)
                    return {"error": "rate_limited", "status": 429}
                elif resp.status != 200:
                    body = await resp.text()
                    if retry < len(RETRY_DELAYS):
                        await asyncio.sleep(RETRY_DELAYS[retry])
                        return await call_api(session, data_content, question_text,
                                            fmt, semaphore, is_image, retry+1)
                    return {"error": body, "status": resp.status}

                result = await resp.json()
                answer_text = result["choices"][0]["message"]["content"].strip()
                usage = result.get("usage", {})
                return {
                    "answer": answer_text,
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                    "model": result.get("model", MODEL),
                }
        except asyncio.TimeoutError:
            if retry < len(RETRY_DELAYS):
                await asyncio.sleep(RETRY_DELAYS[retry])
                return await call_api(session, data_content, question_text,
                                    fmt, semaphore, is_image, retry+1)
            return {"error": "timeout", "status": 0}
        except Exception as e:
            return {"error": str(e), "status": 0}


def parse_answer(raw_answer, answer_type):
    """Parse model's raw text answer into comparable format."""
    if raw_answer is None:
        return None

    text = raw_answer.strip().strip('"').strip("'").strip()
    # Remove common prefixes
    for prefix in ["The answer is ", "Answer: ", "answer: ", "The ", "It is "]:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()

    if answer_type == "number":
        # Extract number from text
        text = text.replace(",", "").replace("$", "").replace("%", "")
        # If verbose response (multi-line / long), grab the LAST number
        # as models tend to show work then give final answer at the end
        if '\n' in text or len(text) > 60:
            matches = re.findall(r'-?\d+\.?\d*', text)
            if matches:
                return float(matches[-1])
            return None
        match = re.search(r'-?\d+\.?\d*', text)
        if match:
            return float(match.group())
        return None
    elif answer_type == "entity":
        return text.strip().rstrip(".")
    elif answer_type == "direction":
        text_lower = text.lower().strip().rstrip(".")
        if "increase" in text_lower:
            return "increase"
        elif "decrease" in text_lower:
            return "decrease"
        return text_lower
    return text


def score_answer(predicted, expected, answer_type, tolerance):
    """Score a prediction against ground truth."""
    if predicted is None:
        return 0

    if answer_type == "number":
        try:
            pred_num = float(predicted)
            exp_num = float(expected)
            if exp_num == 0:
                return 1 if abs(pred_num) < 0.01 else 0
            relative_error = abs(pred_num - exp_num) / abs(exp_num)
            return 1 if relative_error <= tolerance else 0
        except (ValueError, TypeError):
            return 0
    elif answer_type == "entity":
        return 1 if str(predicted).lower().strip() == str(expected).lower().strip() else 0
    elif answer_type == "direction":
        return 1 if str(predicted).lower().strip() == str(expected).lower().strip() else 0
    return 0


async def run_pilot():
    """Run pilot on all questions × 4 text formats + chart_image test."""
    questions = load_questions()
    print(f"Loaded {len(questions)} questions")
    print(f"Model: {MODEL}")
    print(f"Text formats: {FORMATS}")
    print(f"Max concurrent: {MAX_CONCURRENT}")

    # First, test with a single question to verify API connectivity
    print("\n--- API Connectivity Test ---")
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        test_q = questions[0]
        test_data = load_format_data(test_q["sub_id"], "table")
        test_result = await call_api(session, test_data, test_q["question"],
                                     "table", semaphore)
        if "error" in test_result:
            print(f"API FAILED: {test_result}")
            return None
        print(f"API OK — response: {test_result['answer'][:80]}")
        print(f"Expected: {test_q['answer']}")
        parsed = parse_answer(test_result["answer"], test_q["answer_type"])
        score = score_answer(parsed, test_q["answer"], test_q["answer_type"], test_q["tolerance"])
        print(f"Parsed: {parsed}, Score: {score}")

    # Run all text formats
    print(f"\n--- Running {len(questions)} questions × {len(FORMATS)} formats ---")
    all_results = []
    total_calls = len(questions) * len(FORMATS)
    completed = 0
    errors = 0
    total_input_tokens = 0
    total_output_tokens = 0
    start_time = time.time()

    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Process in batches to show progress
        batch_size = 50
        for batch_start in range(0, len(questions), batch_size):
            batch_questions = questions[batch_start:batch_start + batch_size]
            tasks = []

            for q in batch_questions:
                for fmt in FORMATS:
                    data = load_format_data(q["sub_id"], fmt)
                    if data is None:
                        continue
                    tasks.append((q, fmt, call_api(session, data, q["question"],
                                                    fmt, semaphore)))

            # Run batch
            results = await asyncio.gather(*[t[2] for t in tasks], return_exceptions=True)

            for (q, fmt, _), result in zip(tasks, results):
                completed += 1
                if isinstance(result, Exception):
                    errors += 1
                    all_results.append({
                        "sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                        "question": q["question"], "expected": q["answer"],
                        "raw_answer": None, "parsed_answer": None, "score": 0,
                        "error": str(result),
                    })
                    continue

                if "error" in result:
                    errors += 1
                    all_results.append({
                        "sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                        "question": q["question"], "expected": q["answer"],
                        "raw_answer": None, "parsed_answer": None, "score": 0,
                        "error": result["error"],
                    })
                    continue

                total_input_tokens += result.get("prompt_tokens", 0)
                total_output_tokens += result.get("completion_tokens", 0)

                parsed = parse_answer(result["answer"], q["answer_type"])
                score = score_answer(parsed, q["answer"], q["answer_type"], q["tolerance"])
                all_results.append({
                    "sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                    "question": q["question"], "expected": q["answer"],
                    "expected_type": q["answer_type"],
                    "raw_answer": result["answer"], "parsed_answer": parsed,
                    "score": score,
                })

            elapsed = time.time() - start_time
            rate = completed / elapsed if elapsed > 0 else 0
            print(f"  Progress: {completed}/{total_calls} ({errors} errors) "
                  f"| {rate:.1f} calls/sec | "
                  f"tokens: {total_input_tokens:,} in / {total_output_tokens:,} out")

            # Incremental save every 200 calls
            if completed % 200 < batch_size * len(FORMATS):
                with open(PILOT_DIR / "pilot_raw_results.jsonl", 'w') as f:
                    for r in all_results:
                        f.write(json.dumps(r, default=str) + "\n")
                with open(PILOT_DIR / "pilot_progress.json", 'w') as f:
                    json.dump({"completed": completed, "total": total_calls,
                               "errors": errors, "elapsed": round(elapsed, 1)}, f)

    # Now test chart_image (may fail if DeepSeek doesn't support vision)
    print("\n--- Testing chart_image format ---")
    chart_image_results = []
    connector = aiohttp.TCPConnector(limit=5, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        test_qs = questions[:5]  # Test 5 only
        for q in test_qs:
            img_data = load_format_data(q["sub_id"], "chart_image")
            if img_data is None:
                continue
            result = await call_api(session, img_data, q["question"],
                                   "chart_image", semaphore, is_image=True)
            if "error" in result:
                print(f"  chart_image FAILED: {result.get('error', '')[:100]}")
                chart_image_results.append({"supported": False, "error": result.get("error", "")})
                break
            else:
                parsed = parse_answer(result["answer"], q["answer_type"])
                score = score_answer(parsed, q["answer"], q["answer_type"], q["tolerance"])
                chart_image_results.append({"supported": True, "score": score})
                print(f"  chart_image OK — score: {score}")

    vision_supported = any(r.get("supported", False) for r in chart_image_results)
    print(f"  Vision supported: {vision_supported}")

    # Save raw results
    with open(PILOT_DIR / "pilot_raw_results.jsonl", 'w') as f:
        for r in all_results:
            f.write(json.dumps(r, default=str) + "\n")

    # Analyze and report
    elapsed = time.time() - start_time
    df_results = pd.DataFrame(all_results)

    print(f"\n{'='*70}")
    print("PILOT RESULTS — DeepSeek V3.2")
    print(f"{'='*70}")
    print(f"Total calls: {completed} | Errors: {errors} ({errors/max(completed,1)*100:.1f}%)")
    print(f"Time: {elapsed:.0f}s | Rate: {completed/elapsed:.1f} calls/sec")
    print(f"Tokens: {total_input_tokens:,} input / {total_output_tokens:,} output")

    # Estimate cost (DeepSeek V3.2 on OpenRouter)
    # ~$0.14/M input, ~$0.28/M output
    est_cost = (total_input_tokens * 0.14 / 1e6) + (total_output_tokens * 0.28 / 1e6)
    print(f"Estimated cost: ${est_cost:.2f}")

    # Per-format accuracy
    print(f"\n--- Accuracy by Format ---")
    valid = df_results[~df_results["score"].isna()]
    for fmt in FORMATS:
        fmt_data = valid[valid["format"] == fmt]
        if len(fmt_data) > 0:
            acc = fmt_data["score"].mean()
            print(f"  {fmt:<15} {acc:.3f} ({fmt_data['score'].sum():.0f}/{len(fmt_data)})")

    # Per-question-type accuracy
    print(f"\n--- Accuracy by Question Type ---")
    for qtype in sorted(valid["type"].unique()):
        qdata = valid[valid["type"] == qtype]
        acc = qdata["score"].mean()
        print(f"  {qtype:<30} {acc:.3f} ({qdata['score'].sum():.0f}/{len(qdata)})")

    # Per format × question type
    print(f"\n--- Accuracy by Format × Question Type ---")
    pivot = valid.pivot_table(values="score", index="type", columns="format", aggfunc="mean")
    print(pivot.round(3).to_string())

    # Ceiling effect check
    print(f"\n--- Ceiling Effect Check ---")
    ceiling_flag = False
    for qtype in sorted(valid["type"].unique()):
        qdata = valid[valid["type"] == qtype]
        acc = qdata["score"].mean()
        if acc > 0.95:
            print(f"  ⚠ CEILING: {qtype} overall accuracy = {acc:.3f}")
            ceiling_flag = True
    for fmt in FORMATS:
        for qtype in sorted(valid["type"].unique()):
            subset = valid[(valid["format"] == fmt) & (valid["type"] == qtype)]
            if len(subset) > 0:
                acc = subset["score"].mean()
                if acc > 0.95:
                    print(f"  ⚠ CEILING: {fmt} × {qtype} = {acc:.3f}")
                    ceiling_flag = True

    if not ceiling_flag:
        print("  ✓ No ceiling effect detected (all < 95%)")

    # Save summary
    summary = {
        "model": MODEL,
        "total_calls": completed,
        "errors": errors,
        "elapsed_seconds": round(elapsed, 1),
        "estimated_cost_usd": round(est_cost, 2),
        "total_input_tokens": total_input_tokens,
        "total_output_tokens": total_output_tokens,
        "vision_supported": vision_supported,
        "accuracy_by_format": {fmt: round(valid[valid["format"]==fmt]["score"].mean(), 4)
                               for fmt in FORMATS if len(valid[valid["format"]==fmt]) > 0},
        "accuracy_by_qtype": {qt: round(valid[valid["type"]==qt]["score"].mean(), 4)
                              for qt in sorted(valid["type"].unique())},
        "ceiling_detected": ceiling_flag,
    }

    with open(PILOT_DIR / "pilot_summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print(f"\nResults saved to: {PILOT_DIR}")
    return summary


if __name__ == "__main__":
    import sys
    # Force unbuffered output
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    asyncio.run(run_pilot())
