"""
Full experiment run for all 5 OpenRouter models.
DeepSeek V3.2 already done (pilot) — runs GLM-5, MiniMax M2.5, Kimi K2.5, Qwen 3.5.
Kimi and Qwen get chart_image (vision); GLM-5 and MiniMax get text formats only.
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

MODELS = [
    {"id": "z-ai/glm-5",                "name": "GLM-5",          "vision": False},
    {"id": "qwen/qwen3.5-plus-02-15",     "name": "Qwen3.5-Plus",    "vision": True},
]

MAX_CONCURRENT = 80
RATE_LIMIT_DELAY = 0.02
RETRY_DELAYS = [3, 8, 20]

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
                   is_image=False, retry=0):
    async with semaphore:
        await asyncio.sleep(RATE_LIMIT_DELAY)

        if is_image:
            messages = [{"role": "user", "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{data_content}"}},
                {"type": "text", "text": f"Answer the question precisely based on this chart.\n\nQuestion: {question_text}\n\nAnswer with ONLY the answer value, no explanation."}
            ]}]
        else:
            prompt = PROMPT_TEMPLATE.format(data=data_content, question=question_text)
            messages = [{"role": "user", "content": prompt}]

        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://structreason-transfer.research",
            "X-Title": "StructReason-Transfer"
        }
        payload = {
            "model": model_id,
            "messages": messages,
            "max_tokens": 2000,
            "temperature": 0,
        }

        try:
            async with session.post(API_URL, json=payload, headers=headers, timeout=90) as resp:
                if resp.status == 429:
                    if retry < len(RETRY_DELAYS):
                        await asyncio.sleep(RETRY_DELAYS[retry])
                        return await call_api(session, model_id, data_content, question_text,
                                            fmt, semaphore, is_image, retry+1)
                    return {"error": "rate_limited", "status": 429}
                elif resp.status != 200:
                    body = await resp.text()
                    if retry < len(RETRY_DELAYS):
                        await asyncio.sleep(RETRY_DELAYS[retry])
                        return await call_api(session, model_id, data_content, question_text,
                                            fmt, semaphore, is_image, retry+1)
                    return {"error": body[:300], "status": resp.status}

                result = await resp.json()
                msg = result["choices"][0]["message"]
                answer_text = msg.get("content") or ""
                # If content is empty/None, model may have used all tokens on reasoning
                if not answer_text.strip() and msg.get("reasoning"):
                    # Extract last line of reasoning as likely answer
                    reasoning_lines = msg["reasoning"].strip().split("\n")
                    answer_text = reasoning_lines[-1].strip()
                answer_text = answer_text.strip()
                usage = result.get("usage", {})
                return {
                    "answer": answer_text,
                    "prompt_tokens": usage.get("prompt_tokens", 0),
                    "completion_tokens": usage.get("completion_tokens", 0),
                }
        except asyncio.TimeoutError:
            if retry < len(RETRY_DELAYS):
                await asyncio.sleep(RETRY_DELAYS[retry])
                return await call_api(session, model_id, data_content, question_text,
                                    fmt, semaphore, is_image, retry+1)
            return {"error": "timeout", "status": 0}
        except Exception as e:
            if retry < len(RETRY_DELAYS):
                await asyncio.sleep(RETRY_DELAYS[retry])
                return await call_api(session, model_id, data_content, question_text,
                                    fmt, semaphore, is_image, retry+1)
            return {"error": str(e)[:300], "status": 0}


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


async def run_model(model_info, questions):
    model_id = model_info["id"]
    model_name = model_info["name"]
    has_vision = model_info["vision"]
    formats = ALL_FORMATS if has_vision else TEXT_FORMATS

    model_dir = RESULTS_DIR / model_name.lower().replace(" ", "_")
    model_dir.mkdir(parents=True, exist_ok=True)

    # Check if already completed
    results_file = model_dir / "raw_results.jsonl"
    if results_file.exists():
        with open(results_file) as f:
            existing = sum(1 for _ in f)
        expected = len(questions) * len(formats)
        if existing >= expected * 0.95:
            print(f"\n[{model_name}] Already completed ({existing} results). Skipping.")
            return model_name, existing

    print(f"\n{'='*70}")
    print(f"[{model_name}] Starting — {model_id}")
    print(f"  Formats: {formats} | Vision: {has_vision}")
    print(f"  Questions: {len(questions)} | Total calls: {len(questions) * len(formats)}")
    print(f"{'='*70}")

    # Connectivity test
    semaphore = asyncio.Semaphore(MAX_CONCURRENT)
    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        test_q = questions[0]
        test_data = load_format_data(test_q["sub_id"], "table")
        test_result = await call_api(session, model_id, test_data, test_q["question"],
                                     "table", semaphore)
        if "error" in test_result:
            print(f"  API FAILED: {test_result}")
            return model_name, 0
        print(f"  API OK — test response: {test_result['answer'][:60]}")

    # Run all formats
    all_results = []
    total_calls = len(questions) * len(formats)
    completed = 0
    errors = 0
    total_in = 0
    total_out = 0
    start_time = time.time()

    connector = aiohttp.TCPConnector(limit=MAX_CONCURRENT, force_close=True)
    async with aiohttp.ClientSession(connector=connector) as session:
        batch_size = 200  # Large batches to keep 80 connections saturated
        for batch_start in range(0, len(questions), batch_size):
            batch_questions = questions[batch_start:batch_start + batch_size]
            tasks = []

            for q in batch_questions:
                for fmt in formats:
                    is_image = (fmt == "chart_image")
                    data = load_format_data(q["sub_id"], fmt)
                    if data is None:
                        continue
                    tasks.append((q, fmt, call_api(session, model_id, data, q["question"],
                                                   fmt, semaphore, is_image=is_image)))

            results = await asyncio.gather(*[t[2] for t in tasks], return_exceptions=True)

            for (q, fmt, _), result in zip(tasks, results):
                completed += 1
                if isinstance(result, Exception):
                    errors += 1
                    all_results.append({
                        "sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                        "question": q["question"], "expected": q["answer"],
                        "expected_type": q["answer_type"],
                        "raw_answer": None, "parsed_answer": None, "score": 0,
                        "error": str(result)[:200],
                    })
                    continue

                if "error" in result:
                    errors += 1
                    all_results.append({
                        "sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                        "question": q["question"], "expected": q["answer"],
                        "expected_type": q["answer_type"],
                        "raw_answer": None, "parsed_answer": None, "score": 0,
                        "error": result["error"][:200],
                    })
                    continue

                total_in += result.get("prompt_tokens", 0)
                total_out += result.get("completion_tokens", 0)

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
            print(f"  [{model_name}] {completed}/{total_calls} ({errors} err) "
                  f"| {rate:.1f}/s | {total_in:,} in / {total_out:,} out")

            # Incremental save every 200 calls
            if completed % 200 < batch_size * len(formats):
                with open(results_file, 'w') as f:
                    for r in all_results:
                        f.write(json.dumps(r, default=str) + "\n")

    # Final save
    with open(results_file, 'w') as f:
        for r in all_results:
            f.write(json.dumps(r, default=str) + "\n")

    elapsed = time.time() - start_time

    # Quick accuracy report
    df = pd.DataFrame(all_results)
    valid = df[df["raw_answer"].notna()]

    print(f"\n  [{model_name}] DONE — {completed} calls, {errors} errors, {elapsed:.0f}s")
    print(f"  Tokens: {total_in:,} in / {total_out:,} out")

    print(f"  Accuracy by format:")
    for fmt in formats:
        d = valid[valid["format"] == fmt]
        if len(d) > 0:
            print(f"    {fmt:<15} {d['score'].mean():.3f} ({d['score'].sum():.0f}/{len(d)})")

    print(f"  Accuracy by question type:")
    for qt in sorted(valid["type"].unique()):
        d = valid[valid["type"] == qt]
        print(f"    {qt:<30} {d['score'].mean():.3f}")

    # Save summary
    summary = {
        "model_id": model_id,
        "model_name": model_name,
        "vision": has_vision,
        "total_calls": completed,
        "errors": errors,
        "elapsed_seconds": round(elapsed, 1),
        "total_input_tokens": total_in,
        "total_output_tokens": total_out,
        "accuracy_by_format": {fmt: round(float(valid[valid["format"]==fmt]["score"].mean()), 4)
                               for fmt in formats if len(valid[valid["format"]==fmt]) > 0},
        "accuracy_by_qtype": {qt: round(float(valid[valid["type"]==qt]["score"].mean()), 4)
                              for qt in sorted(valid["type"].unique())},
    }
    with open(model_dir / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)

    return model_name, completed


async def main():
    questions = load_questions()
    print(f"Loaded {len(questions)} questions")
    print(f"Models to run: {[m['name'] for m in MODELS]}")

    for model_info in MODELS:
        await run_model(model_info, questions)

    print(f"\n{'='*70}")
    print("ALL OPENROUTER MODELS COMPLETE")
    print(f"{'='*70}")


if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
    asyncio.run(main())
