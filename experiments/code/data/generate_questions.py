"""
Generate 1,750 questions (7 types × 250 sub-tables) with programmatic ground truth.
All answers computed via pandas — zero LLM involvement.

Protocols:
- Q6 tie-breaking: exclude if gap between top-2 values < 5%
- Q7 threshold: select threshold for 30-70% pass rate, skip if impossible
"""

import json
import random
import numpy as np
import pandas as pd
from pathlib import Path

SEED = 42
random.seed(SEED)
np.random.seed(SEED)
rng = np.random.default_rng(SEED)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
SUBTABLE_DIR = BASE_DIR / "data" / "subtables"
QUESTION_DIR = BASE_DIR / "data" / "questions"
QUESTION_DIR.mkdir(parents=True, exist_ok=True)


def load_subtable(path):
    with open(path) as f:
        st = json.load(f)
    df = pd.DataFrame(st["data"])
    return st, df


def generate_q1_lookup(st, df):
    """Q1: Lookup — 'What is the {metric} for {entity} in row/position?'"""
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if not metric_cols:
        return None

    metric = random.choice(metric_cols)
    row_idx = random.randint(0, len(df) - 1)
    entity = str(df[index_col].iloc[row_idx])
    answer = df[metric].iloc[row_idx]

    if isinstance(answer, float) and answer == int(answer):
        answer = int(answer)

    return {
        "type": "Q1_lookup",
        "question": f"What is the {metric} for {entity}?",
        "answer": answer,
        "answer_type": "number",
        "scoring": "exact_match",
        "tolerance": 0.02,
        "meta": {"metric": metric, "entity": entity, "row_idx": row_idx}
    }


def generate_q2_comparison(st, df):
    """Q2: Comparison — 'Which has higher {metric}: {A} or {B}?'"""
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if not metric_cols or len(df) < 2:
        return None

    metric = random.choice(metric_cols)
    indices = random.sample(range(len(df)), 2)
    entity_a = str(df[index_col].iloc[indices[0]])
    entity_b = str(df[index_col].iloc[indices[1]])
    val_a = df[metric].iloc[indices[0]]
    val_b = df[metric].iloc[indices[1]]

    if val_a == val_b:
        return None  # Skip ties

    answer = entity_a if val_a > val_b else entity_b

    return {
        "type": "Q2_comparison",
        "question": f"Which has a higher {metric}: {entity_a} or {entity_b}?",
        "answer": answer,
        "answer_type": "entity",
        "scoring": "exact_match",
        "tolerance": 0,
        "meta": {"metric": metric, "entity_a": entity_a, "entity_b": entity_b,
                 "val_a": float(val_a), "val_b": float(val_b)}
    }


def generate_q3_aggregation(st, df):
    """Q3: Aggregation — 'What is the average {metric} across all entries?'"""
    metric_cols = st["metric_cols"]
    if not metric_cols:
        return None

    metric = random.choice(metric_cols)
    answer = float(df[metric].mean())
    answer = round(answer, 1)

    return {
        "type": "Q3_aggregation",
        "question": f"What is the average {metric} across all entries?",
        "answer": answer,
        "answer_type": "number",
        "scoring": "exact_match",
        "tolerance": 0.05,
        "meta": {"metric": metric, "n_values": len(df)}
    }


def generate_q4_trend(st, df):
    """Q4: Trend — 'Did {metric} increase or decrease between first and last entry?'"""
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if not metric_cols or len(df) < 2:
        return None

    metric = random.choice(metric_cols)
    first_entity = str(df[index_col].iloc[0])
    last_entity = str(df[index_col].iloc[-1])
    val_first = df[metric].iloc[0]
    val_last = df[metric].iloc[-1]

    if val_first == val_last:
        return None

    answer = "increase" if val_last > val_first else "decrease"

    return {
        "type": "Q4_trend",
        "question": f"Did {metric} increase or decrease from {first_entity} to {last_entity}?",
        "answer": answer,
        "answer_type": "direction",
        "scoring": "exact_match",
        "tolerance": 0,
        "meta": {"metric": metric, "first": first_entity, "last": last_entity,
                 "val_first": float(val_first), "val_last": float(val_last)}
    }


def generate_q5_extremum(st, df):
    """Q5: Extremum — 'Which entry has the highest/lowest {metric}?'"""
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if not metric_cols:
        return None

    metric = random.choice(metric_cols)
    direction = random.choice(["highest", "lowest"])

    if direction == "highest":
        idx = df[metric].idxmax()
    else:
        idx = df[metric].idxmin()

    answer = str(df[index_col].iloc[idx])

    return {
        "type": "Q5_extremum",
        "question": f"Which entry has the {direction} {metric}?",
        "answer": answer,
        "answer_type": "entity",
        "scoring": "exact_match",
        "tolerance": 0,
        "meta": {"metric": metric, "direction": direction, "value": float(df[metric].iloc[idx])}
    }


def generate_q6_multihop(st, df):
    """
    Q6: Multi-hop — 'What is {metric_B} for the entry with the highest {metric_A}?'
    Tie-breaking: exclude if gap between top-2 < 5% of top value.
    """
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if len(metric_cols) < 2 or len(df) < 2:
        return None

    metrics = random.sample(metric_cols, 2)
    metric_a, metric_b = metrics[0], metrics[1]

    # Find top-2 values for metric_a
    sorted_vals = df[metric_a].sort_values(ascending=False)
    if len(sorted_vals) < 2:
        return None

    top_val = sorted_vals.iloc[0]
    second_val = sorted_vals.iloc[1]

    # Tie-breaking protocol: gap must be >= 5% of top value
    if top_val == 0:
        return None
    gap = abs(top_val - second_val) / abs(top_val)
    if gap < 0.05:
        return None  # Ambiguous — exclude

    # Check no exact ties
    max_count = (df[metric_a] == top_val).sum()
    if max_count > 1:
        return None  # Multiple entities share max

    # Get the answer
    max_idx = df[metric_a].idxmax()
    max_entity = str(df[index_col].iloc[max_idx])
    answer = df[metric_b].iloc[max_idx]

    if isinstance(answer, float) and answer == int(answer):
        answer = int(answer)

    return {
        "type": "Q6_multi_hop",
        "question": f"What is the {metric_b} for the entry that has the highest {metric_a}?",
        "answer": answer,
        "answer_type": "number",
        "scoring": "exact_match",
        "tolerance": 0.02,
        "meta": {"metric_a": metric_a, "metric_b": metric_b,
                 "max_entity": max_entity, "gap_pct": round(gap * 100, 1)}
    }


def generate_q7_conditional_agg(st, df):
    """
    Q7: Conditional aggregation — 'Average {metric_A} where {metric_B} > threshold?'
    Threshold: 30-70% of rows must pass. Skip if impossible.
    """
    index_col = st["index_col"]
    metric_cols = st["metric_cols"]
    if len(metric_cols) < 2 or len(df) < 3:
        return None

    metrics = random.sample(metric_cols, 2)
    metric_a, metric_b = metrics[0], metrics[1]
    n = len(df)

    # Find threshold that gives 30-70% pass rate
    sorted_b = np.sort(df[metric_b].values)
    valid_threshold = None

    # Try percentiles from 30th to 70th
    for pct in range(30, 71, 5):
        threshold = np.percentile(sorted_b, pct)
        pass_count = (df[metric_b] > threshold).sum()
        pass_rate = pass_count / n
        if 0.3 <= pass_rate <= 0.7:
            valid_threshold = threshold
            break

    if valid_threshold is None:
        return None

    # Round threshold for cleaner question
    if abs(valid_threshold) >= 100:
        valid_threshold = round(valid_threshold, 0)
    elif abs(valid_threshold) >= 10:
        valid_threshold = round(valid_threshold, 1)
    else:
        valid_threshold = round(valid_threshold, 2)

    # Compute answer
    mask = df[metric_b] > valid_threshold
    filtered = df.loc[mask, metric_a]
    if len(filtered) == 0:
        return None

    answer = round(float(filtered.mean()), 1)
    pass_rate = float(mask.sum() / n)

    threshold_display = int(valid_threshold) if valid_threshold == int(valid_threshold) else valid_threshold

    return {
        "type": "Q7_conditional_aggregation",
        "question": f"What is the average {metric_a} for entries where {metric_b} is above {threshold_display}?",
        "answer": answer,
        "answer_type": "number",
        "scoring": "exact_match",
        "tolerance": 0.05,
        "meta": {"metric_a": metric_a, "metric_b": metric_b,
                 "threshold": float(valid_threshold),
                 "pass_rate": round(pass_rate, 2),
                 "n_filtered": int(mask.sum())}
    }


GENERATORS = [
    generate_q1_lookup,
    generate_q2_comparison,
    generate_q3_aggregation,
    generate_q4_trend,
    generate_q5_extremum,
    generate_q6_multihop,
    generate_q7_conditional_agg,
]


def generate_all_questions():
    """Generate 1,750 questions (7 × 250) with programmatic ground truth."""
    subtable_files = sorted(SUBTABLE_DIR.glob("*.json"))
    print(f"Found {len(subtable_files)} sub-tables")

    all_questions = []
    stats = {f"Q{i+1}": {"generated": 0, "skipped": 0} for i in range(7)}
    q6_exclusions = 0
    q7_skips = 0

    for path in subtable_files:
        st, df = load_subtable(path)
        sub_id = st["id"]

        for i, gen_fn in enumerate(GENERATORS):
            q_type = f"Q{i+1}"
            # Try up to 5 times with different random choices
            question = None
            for attempt in range(5):
                question = gen_fn(st, df)
                if question is not None:
                    break

            if question is not None:
                question["sub_id"] = sub_id
                question["dataset"] = st["dataset"]
                question["domain"] = st["domain"]
                question["tier"] = st["tier"]
                all_questions.append(question)
                stats[q_type]["generated"] += 1
            else:
                stats[q_type]["skipped"] += 1
                if q_type == "Q6":
                    q6_exclusions += 1
                elif q_type == "Q7":
                    q7_skips += 1

    # Save questions
    out_path = QUESTION_DIR / "questions.jsonl"
    with open(out_path, 'w') as f:
        for q in all_questions:
            f.write(json.dumps(q) + "\n")

    # Save answers separately (for scoring pipeline)
    answers_path = QUESTION_DIR / "answers.jsonl"
    with open(answers_path, 'w') as f:
        for q in all_questions:
            f.write(json.dumps({
                "sub_id": q["sub_id"],
                "type": q["type"],
                "answer": q["answer"],
                "answer_type": q["answer_type"],
                "tolerance": q["tolerance"],
            }) + "\n")

    # Report
    print(f"\n{'='*60}")
    print("QUESTION GENERATION REPORT")
    print(f"{'='*60}")
    print(f"Total questions generated: {len(all_questions)}")
    print(f"\nPer-type breakdown:")
    for q_type, s in stats.items():
        print(f"  {q_type}: {s['generated']} generated, {s['skipped']} skipped")
    print(f"\nQ6 exclusions (tie-break <5%): {q6_exclusions}")
    print(f"Q7 skips (no valid threshold): {q7_skips}")

    # Distribution by tier
    tier_counts = {}
    for q in all_questions:
        tier_counts[q["tier"]] = tier_counts.get(q["tier"], 0) + 1
    print(f"\nBy complexity tier:")
    for tier, count in sorted(tier_counts.items()):
        print(f"  {tier}: {count}")

    print(f"\nSaved to: {out_path}")
    return all_questions


if __name__ == "__main__":
    generate_all_questions()
