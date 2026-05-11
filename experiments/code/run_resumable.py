"""
Resumable runner — saves after EVERY batch, resumes from last checkpoint.
No credits wasted if process dies.
"""
import asyncio
import json
import os
import re
import time
import base64
import random
import sys
from pathlib import Path
from dotenv import load_dotenv
import aiohttp
import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
API_URL = "https://openrouter.ai/api/v1/chat/completions"

QUESTION_DIR = BASE_DIR / "experiments" / "data" / "questions"
FORMAT_DIR = BASE_DIR / "experiments" / "data" / "formats"
RESULTS_DIR = BASE_DIR / "experiments" / "results"

TEXT_FORMATS = ["table", "chart_text", "graph", "timeseries"]
ALL_FORMATS = ["table", "chart_text", "graph", "timeseries", "chart_image"]

MAX_CONCURRENT = 5  # Low concurrency for remaining heavy vision calls
RATE_LIMIT_DELAY = 0.1
RETRY_DELAYS = [5, 15, 30]

PROMPT_TEMPLATE = """You are given data in the following format. Answer the question precisely.

{data}

Question: {question}

Answer with ONLY the answer value, no explanation."""


def load_questions():
    questions = []
    with open(QUESTION_DIR / "questions.jsonl") as f:
        for line in f:
            questions.append(json.loads(line))
    return questions


def load_format_data(sub_id, fmt):
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


async def call_api(session, model_id, data_content, question_text, fmt, semaphore,
                   is_image=False, reasoning_effort=None):
    if is_image:
        messages = [{"role": "user", "content": [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data_content}"}},
            {"type": "text", "text": f"Answer the question precisely based on this chart.\n\nQuestion: {question_text}\n\nAnswer with ONLY the answer value, no explanation."}
        ]}]
    else:
        prompt = PROMPT_TEMPLATE.format(data=data_content, question=question_text)
        messages = [{"role": "user", "content": prompt}]
    headers = {"Authorization": f"Bearer {OPENROUTER_API_KEY}", "Content-Type": "application/json",
                "HTTP-Referer": "https://structreason-transfer.research", "X-Title": "StructReason-Transfer"}
    payload = {"model": model_id, "messages": messages, "max_tokens": 2000, "temperature": 0}
    if reasoning_effort:
        payload["reasoning"] = {"effort": reasoning_effort}

    for attempt in range(4):  # 1 try + 3 retries
        async with semaphore:  # Release semaphore between retries
            await asyncio.sleep(RATE_LIMIT_DELAY)
            try:
                async with session.post(API_URL, json=payload, headers=headers, timeout=300) as resp:
                    if resp.status == 429:
                        pass  # Fall through to retry
                    elif resp.status != 200:
                        pass  # Fall through to retry
                    else:
                        result = await resp.json()
                        msg = result["choices"][0]["message"]
                        answer_text = msg.get("content") or ""
                        if not answer_text.strip() and msg.get("reasoning"):
                            reasoning_lines = msg["reasoning"].strip().split("\n")
                            answer_text = reasoning_lines[-1].strip()
                        answer_text = answer_text.strip()
                        usage = result.get("usage", {})
                        return {"answer": answer_text, "prompt_tokens": usage.get("prompt_tokens", 0),
                                "completion_tokens": usage.get("completion_tokens", 0)}
            except (asyncio.TimeoutError, Exception):
                pass  # Fall through to retry
        # Semaphore released — sleep before retry without holding a slot
        if attempt < 3:
            await asyncio.sleep(RETRY_DELAYS[attempt])

    return {"error": "failed_after_retries", "status": 0}


def parse_answer(raw_answer, answer_type):
    if raw_answer is None:
        return None
    text = raw_answer.strip().strip('"').strip("'").strip()
    for prefix in ["The answer is ", "Answer: ", "answer: ", "The ", "It is "]:
        if text.lower().startswith(prefix.lower()):
            text = text[len(prefix):].strip()
    if answer_type == "number":
        text = text.replace(",", "").replace("$", "").replace("%", "")
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
        if "increase" in text_lower: return "increase"
        elif "decrease" in text_lower: return "decrease"
        return text_lower
    return text


def score_answer(predicted, expected, answer_type, tolerance):
    if predicted is None:
        return 0
    if answer_type == "number":
        try:
            pred_num = float(predicted)
            exp_num = float(expected)
            if exp_num == 0:
                return 1 if abs(pred_num) < 0.01 else 0
            return 1 if abs(pred_num - exp_num) / abs(exp_num) <= tolerance else 0
        except (ValueError, TypeError):
            return 0
    elif answer_type in ("entity", "direction"):
        return 1 if str(predicted).lower().strip() == str(expected).lower().strip() else 0
    return 0


def load_completed(results_file):
    """Load already-completed (sub_id, type, format) tuples."""
    completed = set()
    if results_file.exists():
        with open(results_file) as f:
            for line in f:
                r = json.loads(line)
                completed.add((r["sub_id"], r["type"], r["format"]))
    return completed


async def run_model(model_id, model_name, has_vision, questions, reasoning_effort=None):
    formats = ALL_FORMATS if has_vision else TEXT_FORMATS
    model_dir = RESULTS_DIR / model_name.lower().replace(" ", "_")
    model_dir.mkdir(parents=True, exist_ok=True)
    results_file = model_dir / "raw_results.jsonl"

    # Resume: load already-completed calls
    completed_keys = load_completed(results_file)
    total_expected = len(questions) * len(formats)

    if len(completed_keys) >= total_expected * 0.99:
        print(f"[{model_name}] Already complete ({len(completed_keys)}/{total_expected}). Skipping.")
        return

    print(f"\n{'='*70}")
    print(f"[{model_name}] {model_id}")
    print(f"  Formats: {formats} | Vision: {has_vision} | Reasoning: {reasoning_effort or 'default'}")
    print(f"  Total: {total_expected} | Already done: {len(completed_keys)} | Remaining: {total_expected - len(completed_keys)}")
    print(f"{'='*70}")

    # Build task list skipping completed
    all_tasks = []
    for q in questions:
        for fmt in formats:
            key = (q["sub_id"], q["type"], fmt)
            if key not in completed_keys:
                all_tasks.append((q, fmt))

    print(f"  {len(all_tasks)} calls to make")

    # Connectivity test
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        test_q = questions[0]
        test_data = load_format_data(test_q["sub_id"], "table")
        test_result = await call_api(session, model_id, test_data, test_q["question"],
                                     "table", semaphore, reasoning_effort=reasoning_effort)
        if "error" in test_result:
            print(f"  API FAILED: {test_result}")
            return
        print(f"  API OK — {test_result['answer'][:40]}")

    # Process in batches, save after EVERY batch
    completed = len(completed_keys)
    errors = 0
    total_in = 0
    total_out = 0
    start_time = time.time()
    batch_size = 200  # Same as MiniMax/Kimi runs that worked at 2-3/s

    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        # Fire all calls as individual tasks, save each result immediately
        async def process_one(q, fmt):
            is_image = (fmt == "chart_image")
            data = load_format_data(q["sub_id"], fmt)
            if data is None:
                return None
            result = await call_api(session, model_id, data, q["question"],
                                     fmt, semaphore, is_image=is_image,
                                     reasoning_effort=reasoning_effort)
            if "error" in result:
                return {"sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                    "question": q["question"], "expected": q["answer"], "expected_type": q["answer_type"],
                    "raw_answer": None, "parsed_answer": None, "score": 0, "error": result["error"][:200]}
            parsed = parse_answer(result["answer"], q["answer_type"])
            score = score_answer(parsed, q["answer"], q["answer_type"], q["tolerance"])
            return {"sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                "question": q["question"], "expected": q["answer"], "expected_type": q["answer_type"],
                "raw_answer": result["answer"], "parsed_answer": parsed, "score": score,
                "prompt_tokens": result.get("prompt_tokens", 0),
                "completion_tokens": result.get("completion_tokens", 0)}

        # Create all tasks
        tasks = []
        for q, fmt in all_tasks:
            tasks.append(asyncio.create_task(process_one(q, fmt)))

        # Process results as they complete — save each one immediately
        results_file_handle = open(results_file, 'a')
        last_print = time.time()
        for coro in asyncio.as_completed(tasks):
            try:
                result = await coro
            except Exception as e:
                errors += 1
                continue
            if result is None:
                continue
            completed += 1
            if result.get("error"):
                errors += 1
            total_in += result.pop("prompt_tokens", 0)
            total_out += result.pop("completion_tokens", 0)
            # Save immediately
            results_file_handle.write(json.dumps(result, default=str) + "\n")
            results_file_handle.flush()
            # Print progress every 5 seconds
            now = time.time()
            if now - last_print >= 5:
                elapsed = now - start_time
                rate = (completed - len(completed_keys)) / elapsed if elapsed > 0 else 0
                print(f"  [{model_name}] {completed}/{total_expected} ({errors} err) | {rate:.1f}/s", flush=True)
                last_print = now

        results_file_handle.close()
        elapsed = time.time() - start_time
        rate = (completed - len(completed_keys)) / elapsed if elapsed > 0 else 0
        print(f"  [{model_name}] {completed}/{total_expected} ({errors} err) | {rate:.1f}/s | DONE", flush=True)

    # Final summary
    elapsed = time.time() - start_time
    all_results = []
    with open(results_file) as f:
        for line in f:
            all_results.append(json.loads(line))
    df = pd.DataFrame(all_results)
    valid = df[df["raw_answer"].notna()]

    print(f"\n  [{model_name}] DONE — {len(all_results)} total, {errors} errors, {elapsed:.0f}s")
    print(f"  Accuracy by format:")
    for fmt in formats:
        d = valid[valid["format"] == fmt]
        if len(d) > 0:
            print(f"    {fmt:<15} {d['score'].mean():.3f} ({d['score'].sum():.0f}/{len(d)})")
    print(f"  Accuracy by question type:")
    for qt in sorted(valid["type"].unique()):
        d = valid[valid["type"] == qt]
        print(f"    {qt:<30} {d['score'].mean():.3f}")

    summary = {
        "model_id": model_id, "model_name": model_name, "vision": has_vision,
        "reasoning_effort": reasoning_effort,
        "total_results": len(all_results), "errors": errors,
        "accuracy_by_format": {fmt: round(float(valid[valid["format"]==fmt]["score"].mean()), 4)
                               for fmt in formats if len(valid[valid["format"]==fmt]) > 0},
        "accuracy_by_qtype": {qt: round(float(valid[valid["type"]==qt]["score"].mean()), 4)
                              for qt in sorted(valid["type"].unique())},
    }
    with open(model_dir / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)


async def main():
    questions = load_questions()
    print(f"Loaded {len(questions)} questions")

    # Model 1: DeepSeek V3.2 with reasoning
    await run_model("deepseek/deepseek-v3.2", "DeepSeek-V3.2", False, questions, reasoning_effort="medium")

    # Model 2: Qwen 3.5 Plus
    await run_model("qwen/qwen3.5-plus-02-15", "Qwen3.5-Plus", True, questions)

    print("\nALL DONE")


if __name__ == "__main__":
    import traceback
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        traceback.print_exc()
        print("\nRestart with: python -u experiments/code/run_resumable.py")
    except KeyboardInterrupt:
        print("\n\nInterrupted by user. Progress saved. Restart to resume.")
