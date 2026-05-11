# DeepSeek V3.2 Deduplication Notes (2026-05-11)

## Problem

The original `raw_results.jsonl` had 7,896 rows but only 6,896 unique `(sub_id, type, format)` triples.
This means the model was called twice on the same question/format combination 1,000 times.

## Policy

Kept the **first occurrence** of each `(sub_id, type, format)` triple. Backed up the original to `raw_results.jsonl.bak-2026-05-11`.

## Inconsistent-score pairs

Of the 1,000 duplicates, **41** pairs had inconsistent scores (first run vs second run gave different correctness verdicts).

For these, the first-occurrence policy was applied. This is methodologically defensible because:
1. First-occurrence is order-independent of any sampling bias in the second run.
2. Since the duplicates were not by design, treating either run as canonical is acceptable.

Alternative: exclude these 41 as ambiguous. Effect on accuracy: at most 41/6896 = 0.59%.

## Inconsistent pairs (full log)

```
{'key': "('ember_electricity_small_004', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '31.1', 'second_answer': "I'll decide to compute the average and round to one decimal "}
{'key': "('ember_electricity_small_005', 'Q7_conditional_aggregation', 'chart_text')", 'first_score': 0, 'second_score': 1, 'first_answer': "Maybe the intended answer is 3851.0. However, let's see if t", 'second_answer': '3851.0'}
{'key': "('ember_electricity_small_005', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '3851.0'}
{'key': "('ember_electricity_small_006', 'Q7_conditional_aggregation', 'chart_text')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Perhaps the intended answer is simply the result of the calc', 'second_answer': '7472.1'}
{'key': "('epa_aqs_large_000', 'Q7_conditional_aggregation', 'graph')", 'first_score': 1, 'second_score': 0, 'first_answer': '128.1', 'second_answer': 'Maybe we should compute the average without rounding: 1793.8'}
{'key': "('epa_aqs_large_000', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '128.1'}
{'key': "('epa_aqs_large_001', 'Q7_conditional_aggregation', 'graph')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '2.414285714285714'}
{'key': "('epa_aqs_large_002', 'Q3_aggregation', 'table')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Now we sum these', 'second_answer': '28.93'}
{'key': "('epa_aqs_large_002', 'Q7_conditional_aggregation', 'graph')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '62.97'}
{'key': "('epa_aqs_large_002', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': 'Given typical problems, they expect a rounded number. Since '}
{'key': "('epa_aqs_large_004', 'Q7_conditional_aggregation', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': '46.8', 'second_answer': 'Now, compute average precisely: 654.8 / 14 = 46.7714285714. '}
{'key': "('epa_aqs_large_004', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '46.77'}
{'key': "('epa_aqs_large_005', 'Q3_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '31.665', 'second_answer': '633.3 / 20 = 31.665, which is 31.'}
{'key': "('epa_aqs_large_005', 'Q7_conditional_aggregation', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': '99.7', 'second_answer': 'None'}
{'key': "('epa_aqs_large_005', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '99.7', 'second_answer': 'None'}
{'key': "('epa_aqs_large_006', 'Q5_extremum', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': 'Station_S16', 'second_answer': 'Station_S16, Station_NW1'}
{'key': "('epa_aqs_large_006', 'Q5_extremum', 'chart_text')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Station_S16, Station_NW1', 'second_answer': 'Station_S16'}
{'key': "('epa_aqs_large_006', 'Q5_extremum', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': 'Station_S16', 'second_answer': 'Station_S16, Station_NW1'}
{'key': "('epa_aqs_large_006', 'Q7_conditional_aggregation', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': '10.43', 'second_answer': "Perhaps the expected answer is 10.4? But let's see the data:"}
{'key': "('epa_aqs_large_006', 'Q7_conditional_aggregation', 'graph')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '10.43'}
{'key': "('epa_aqs_large_006', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Let me see if I missed any index. I had indices: 2,4,5,7,8,9', 'second_answer': '10.43'}
{'key': "('epa_aqs_medium_002', 'Q2_comparison', 'chart_text')", 'first_score': 0, 'second_score': 1, 'first_answer': 'We are given data for seven stations: NW10, NE2, W18, N15, C', 'second_answer': 'Station_W18'}
{'key': "('epa_aqs_medium_003', 'Q2_comparison', 'chart_text')", 'first_score': 0, 'second_score': 1, 'first_answer': 'I think I should answer based on what is given. Since Statio', 'second_answer': 'Station_SW4'}
{'key': "('epa_aqs_small_002', 'Q3_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '52.08', 'second_answer': ''}
{'key': "('epa_aqs_small_002', 'Q4_trend', 'chart_text')", 'first_score': 1, 'second_score': 0, 'first_answer': 'decrease', 'second_answer': ''}
{'key': "('epa_aqs_small_003', 'Q5_extremum', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': 'Station_N6', 'second_answer': ''}
{'key': "('faostat_crops_large_000', 'Q5_extremum', 'table')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Nigeria, India', 'second_answer': 'Nigeria'}
{'key': "('faostat_crops_large_000', 'Q5_extremum', 'graph')", 'first_score': 1, 'second_score': 0, 'first_answer': 'Nigeria', 'second_answer': 'Nigeria, India'}
{'key': "('faostat_crops_large_000', 'Q5_extremum', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Nigeria, India', 'second_answer': 'Nigeria'}
{'key': "('faostat_crops_large_000', 'Q7_conditional_aggregation', 'graph')", 'first_score': 1, 'second_score': 0, 'first_answer': '159.5', 'second_answer': 'Australia: 6580.2 < 809'}
{'key': "('epa_aqs_medium_004', 'Q7_conditional_aggregation', 'graph')", 'first_score': 0, 'second_score': 1, 'first_answer': "But let's see if there's any", 'second_answer': '39.9'}
{'key': "('epa_aqs_medium_005', 'Q7_conditional_aggregation', 'graph')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '58.0'}
{'key': "('epa_aqs_medium_006', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'None', 'second_answer': '17.3'}
{'key': "('epa_aqs_medium_007', 'Q7_conditional_aggregation', 'table')", 'first_score': 1, 'second_score': 0, 'first_answer': '45.4', 'second_answer': 'None'}
{'key': "('epa_aqs_medium_007', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '45.4', 'second_answer': 'None'}
{'key': "('epa_aqs_small_001', 'Q5_extremum', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': '16.5', 'second_answer': 'Station_S16'}
{'key': "('epa_aqs_small_002', 'Q7_conditional_aggregation', 'timeseries')", 'first_score': 1, 'second_score': 0, 'first_answer': '50.6', 'second_answer': 'Maybe I\'ll output 50.6. But wait, the problem says "Answer w'}
{'key': "('epa_aqs_small_005', 'Q7_conditional_aggregation', 'graph')", 'first_score': 1, 'second_score': 0, 'first_answer': '14.73', 'second_answer': "However, to be safe, I'll output the exact fraction? No"}
{'key': "('epa_aqs_small_007', 'Q7_conditional_aggregation', 'table')", 'first_score': 0, 'second_score': 1, 'first_answer': "Let's think about the condition: PM25_ug_m3 above 31.1. That", 'second_answer': '4.23'}
{'key': "('faostat_crops_large_000', 'Q5_extremum', 'graph')", 'first_score': 1, 'second_score': 0, 'first_answer': 'Nigeria', 'second_answer': 'Nigeria, India'}
{'key': "('faostat_crops_large_000', 'Q5_extremum', 'timeseries')", 'first_score': 0, 'second_score': 1, 'first_answer': 'Nigeria, India', 'second_answer': 'Nigeria'}
```
