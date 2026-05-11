"""
Gemini 3.1 Pro runner — resumable, vision + thinking enabled.
"""
import asyncio
import json
import os
import re
import time
import random
import sys
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types
import numpy as np
import pandas as pd

sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

SEED = 42
random.seed(SEED)
np.random.seed(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")

MODEL = "gemini-3.1-pro-preview"
USE_VERTEX = True

QUESTION_DIR = BASE_DIR / "experiments" / "data" / "questions"
FORMAT_DIR = BASE_DIR / "experiments" / "data" / "formats"
RESULTS_DIR = BASE_DIR / "experiments" / "results"

ALL_FORMATS = ["table", "chart_text", "graph", "timeseries", "chart_image"]

PROMPT_TEMPLATE = """You are given data in the following format. Answer the question precisely.

{data}

Question: {question}

Answer with ONLY the answer value, no explanation."""

MAX_CONCURRENT = 15  # Vertex AI — moderate concurrency
RETRY_DELAYS = [5, 15, 30]


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
            return img_path.read_bytes()
        return None
    else:
        txt_path = FORMAT_DIR / fmt / f"{sub_id}.txt"
        if txt_path.exists():
            return txt_path.read_text()
        return None


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
    completed = set()
    if results_file.exists():
        with open(results_file) as f:
            for line in f:
                r = json.loads(line)
                completed.add((r["sub_id"], r["type"], r["format"]))
    return completed


async def call_gemini(client, data_content, question_text, fmt, semaphore, is_image=False):
    for attempt in range(4):
        async with semaphore:
            try:
                if is_image:
                    contents = [
                        types.Part.from_bytes(data=data_content, mime_type="image/png"),
                        f"Answer the question precisely based on this chart.\n\nQuestion: {question_text}\n\nAnswer with ONLY the answer value, no explanation."
                    ]
                else:
                    contents = PROMPT_TEMPLATE.format(data=data_content, question=question_text)

                config = types.GenerateContentConfig(
                    temperature=0,
                    max_output_tokens=2000,
                )

                resp = await asyncio.to_thread(
                    client.models.generate_content,
                    model=MODEL,
                    contents=contents,
                    config=config,
                )

                answer_text = resp.text or ""
                answer_text = answer_text.strip()
                usage = resp.usage_metadata
                return {
                    "answer": answer_text,
                    "prompt_tokens": usage.prompt_token_count if usage else 0,
                    "completion_tokens": usage.candidates_token_count if usage else 0,
                }
            except Exception as e:
                last_err = str(e)[:300]
                pass  # Retry all errors
        if attempt < 3:
            await asyncio.sleep(RETRY_DELAYS[attempt])

    return {"error": f"failed_after_retries: {last_err}", "status": 0}


async def main():
    questions = load_questions()
    print(f"Loaded {len(questions)} questions")

    model_name = "Gemini-3.1-Pro-NoThinking"
    model_dir = RESULTS_DIR / model_name.lower().replace(" ", "_").replace(".", "")
    model_dir.mkdir(parents=True, exist_ok=True)
    results_file = model_dir / "raw_results.jsonl"

    completed_keys = load_completed(results_file)
    total_expected = len(questions) * len(ALL_FORMATS)

    if len(completed_keys) >= total_expected:
        print(f"[{model_name}] Already complete ({len(completed_keys)}/{total_expected}). Skipping.")
        return

    print(f"\n{'='*70}")
    print(f"[{model_name}] {MODEL}")
    print(f"  Formats: {ALL_FORMATS} | Vision: True | Thinking: disabled")
    print(f"  Total: {total_expected} | Already done: {len(completed_keys)} | Remaining: {total_expected - len(completed_keys)}")
    print(f"{'='*70}")

    all_tasks_list = []
    for q in questions:
        for fmt in ALL_FORMATS:
            key = (q["sub_id"], q["type"], fmt)
            if key not in completed_keys:
                all_tasks_list.append((q, fmt))

    print(f"  {len(all_tasks_list)} calls to make")

    client = genai.Client(
        vertexai=True,
        project=os.getenv("GCP_PROJECT_ID"),
        location="global"
    )

    # Connectivity test with retry
    for i in range(5):
        try:
            resp = client.models.generate_content(model=MODEL, contents="What is 2+2? ONLY the number.", config=types.GenerateContentConfig(temperature=0, max_output_tokens=10))
            print(f"  API OK — {resp.text}")
            break
        except Exception as e:
            print(f"  API test attempt {i+1} failed: {str(e)[:80]}. Waiting 30s...")
            import time as _t; _t.sleep(30)

    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    completed = len(completed_keys)
    errors = 0
    total_in = 0
    total_out = 0
    start_time = time.time()

    async def process_one(q, fmt):
        is_image = (fmt == "chart_image")
        data = load_format_data(q["sub_id"], fmt)
        if data is None:
            return None
        result = await call_gemini(client, data, q["question"], fmt, semaphore, is_image=is_image)
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

    tasks = []
    for q, fmt in all_tasks_list:
        tasks.append(asyncio.create_task(process_one(q, fmt)))

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
        total_in += result.pop("prompt_tokens", 0) or 0
        total_out += result.pop("completion_tokens", 0) or 0
        results_file_handle.write(json.dumps(result, default=str) + "\n")
        results_file_handle.flush()
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

    # Summary
    all_results = []
    with open(results_file) as f:
        for line in f:
            all_results.append(json.loads(line))
    df = pd.DataFrame(all_results)
    valid = df[df["raw_answer"].notna()]

    print(f"\n  [{model_name}] {len(all_results)} total, {errors} errors, {elapsed:.0f}s")
    print(f"  Accuracy by format:")
    for fmt in ALL_FORMATS:
        d = valid[valid["format"] == fmt]
        if len(d) > 0:
            print(f"    {fmt:<15} {d['score'].mean():.3f} ({d['score'].sum():.0f}/{len(d)})")
    print(f"  Accuracy by question type:")
    for qt in sorted(valid["type"].unique()):
        d = valid[valid["type"] == qt]
        print(f"    {qt:<30} {d['score'].mean():.3f}")

    summary = {
        "model_id": MODEL, "model_name": model_name, "vision": True,
        "thinking": False, "thinking_budget": 0,
        "total_results": len(all_results), "errors": errors,
        "accuracy_by_format": {fmt: round(float(valid[valid["format"]==fmt]["score"].mean()), 4)
                               for fmt in ALL_FORMATS if len(valid[valid["format"]==fmt]) > 0},
        "accuracy_by_qtype": {qt: round(float(valid[valid["type"]==qt]["score"].mean()), 4)
                              for qt in sorted(valid["type"].unique())},
    }
    with open(model_dir / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    print("\nDONE")


if __name__ == "__main__":
    import traceback
    try:
        asyncio.run(main())
    except Exception as e:
        print(f"\n\nFATAL ERROR: {e}")
        traceback.print_exc()
        print("\nRestart with: python -u experiments/code/run_gemini.py")
    except KeyboardInterrupt:
        print("\n\nInterrupted. Progress saved. Restart to resume.")
