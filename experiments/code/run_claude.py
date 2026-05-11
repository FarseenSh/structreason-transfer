"""
Claude Sonnet 4.6 runner using Claude Code CLI (Max plan, no API costs).
Uses `claude --print --model sonnet --effort high` for each question.
Resumable — saves each result immediately.
"""
import json
import os
import re
import subprocess
import sys
import time
import base64
from pathlib import Path

sys.stdout.reconfigure(line_buffering=True)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
QUESTION_DIR = BASE_DIR / "experiments" / "data" / "questions"
FORMAT_DIR = BASE_DIR / "experiments" / "data" / "formats"
RESULTS_DIR = BASE_DIR / "experiments" / "results"

ALL_FORMATS = ["table", "chart_text", "graph", "timeseries", "chart_image"]

PROMPT_TEMPLATE = """You are given data in the following format. Answer the question precisely.

{data}

Question: {question}

Answer with ONLY the answer value, no explanation."""

VISION_PROMPT = """Answer the question precisely based on this chart image at: {image_path}

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
            return str(img_path)
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
                if r.get("raw_answer") is not None:
                    completed.add((r["sub_id"], r["type"], r["format"]))
    return completed


def call_claude(prompt, is_image=False, image_path=None):
    """Call claude CLI with --print --model sonnet --effort high"""
    try:
        if is_image and image_path:
            # For images, tell Claude to read the image file
            full_prompt = f"Look at the chart image at {image_path} and answer precisely.\n\nQuestion: {prompt}\n\nAnswer with ONLY the answer value, no explanation."
            result = subprocess.run(
                ["claude", "--print", "--model", "sonnet", "--effort", "high",
                 "--allowedTools", "Read", "--add-dir", str(FORMAT_DIR / "chart_image"),
                 full_prompt],
                capture_output=True, text=True, timeout=120
            )
        else:
            result = subprocess.run(
                ["claude", "--print", "--model", "sonnet", "--effort", "high", prompt],
                capture_output=True, text=True, timeout=120
            )

        if result.returncode == 0:
            return {"answer": result.stdout.strip()}
        else:
            return {"error": result.stderr[:200]}
    except subprocess.TimeoutExpired:
        return {"error": "timeout"}
    except Exception as e:
        return {"error": str(e)[:200]}


def main():
    questions = load_questions()
    print(f"Loaded {len(questions)} questions")

    model_name = "Claude-Sonnet-4.6"
    model_dir = RESULTS_DIR / model_name.lower().replace(" ", "_").replace(".", "")
    model_dir.mkdir(parents=True, exist_ok=True)
    results_file = model_dir / "raw_results.jsonl"

    completed_keys = load_completed(results_file)
    total_expected = len(questions) * len(ALL_FORMATS)

    print(f"\n{'='*70}")
    print(f"[{model_name}] via Claude Code CLI")
    print(f"  Formats: {ALL_FORMATS} | Vision: True | Effort: high")
    print(f"  Total: {total_expected} | Already done: {len(completed_keys)} | Remaining: {total_expected - len(completed_keys)}")
    print(f"{'='*70}")

    # Build task list
    all_tasks = []
    for q in questions:
        for fmt in ALL_FORMATS:
            key = (q["sub_id"], q["type"], fmt)
            if key not in completed_keys:
                all_tasks.append((q, fmt))

    print(f"  {len(all_tasks)} calls to make")

    # Connectivity test
    result = call_claude("What is 2+2? Answer ONLY the number.")
    if "error" in result:
        print(f"  CLI FAILED: {result}")
        return
    print(f"  CLI OK — {result['answer']}")

    completed = len(completed_keys)
    errors = 0
    start_time = time.time()

    results_fh = open(results_file, 'a')

    for i, (q, fmt) in enumerate(all_tasks):
        is_image = (fmt == "chart_image")
        data = load_format_data(q["sub_id"], fmt)
        if data is None:
            continue

        if is_image:
            prompt = q["question"]
            result = call_claude(prompt, is_image=True, image_path=data)
        else:
            prompt = PROMPT_TEMPLATE.format(data=data, question=q["question"])
            result = call_claude(prompt)

        completed += 1

        if "error" in result:
            errors += 1
            entry = {"sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                "question": q["question"], "expected": q["answer"], "expected_type": q["answer_type"],
                "raw_answer": None, "parsed_answer": None, "score": 0, "error": result["error"][:200]}
        else:
            parsed = parse_answer(result["answer"], q["answer_type"])
            score = score_answer(parsed, q["answer"], q["answer_type"], q["tolerance"])
            entry = {"sub_id": q["sub_id"], "type": q["type"], "format": fmt,
                "question": q["question"], "expected": q["answer"], "expected_type": q["answer_type"],
                "raw_answer": result["answer"], "parsed_answer": parsed, "score": score}

        results_fh.write(json.dumps(entry, default=str) + "\n")
        results_fh.flush()

        # Progress every 10 calls
        if completed % 10 == 0:
            elapsed = time.time() - start_time
            rate = (completed - len(completed_keys)) / elapsed if elapsed > 0 else 0
            print(f"  [{model_name}] {completed}/{total_expected} ({errors} err) | {rate:.2f}/s")

    results_fh.close()
    elapsed = time.time() - start_time
    print(f"\n  [{model_name}] DONE — {completed}/{total_expected}, {errors} errors, {elapsed:.0f}s")

    # Summary
    all_results = []
    with open(results_file) as f:
        for line in f:
            all_results.append(json.loads(line))
    import pandas as pd
    df = pd.DataFrame(all_results)
    valid = df[df["raw_answer"].notna()]

    print(f"  Accuracy by format:")
    for fmt in ALL_FORMATS:
        d = valid[valid["format"] == fmt]
        if len(d) > 0:
            print(f"    {fmt:<15} {d['score'].mean():.3f} ({d['score'].sum():.0f}/{len(d)})")

    summary = {
        "model_id": "claude-sonnet-4-6", "model_name": model_name, "vision": True,
        "thinking": True, "effort": "high",
        "total_results": len(all_results), "errors": errors,
        "accuracy_by_format": {fmt: round(float(valid[valid["format"]==fmt]["score"].mean()), 4)
                               for fmt in ALL_FORMATS if len(valid[valid["format"]==fmt]) > 0},
    }
    with open(model_dir / "summary.json", 'w') as f:
        json.dump(summary, f, indent=2)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInterrupted. Progress saved. Restart to resume.")
