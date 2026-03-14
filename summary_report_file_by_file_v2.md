# File-by-file analysis (exact pair match: case folder name + file name)

Rule used:
- case_name = run folder name (e.g., BernardCells)
- file_name = basename (e.g., g)
- include only files under 0/, constant/, system/
- check whether (case_name,file_name) exists in train/test jsonl

## qwen-standard_runs
- scanned files (0/constant/system): **0**
- matched in jsonl: **0**
- NOT in jsonl: **0**
- sample not-in-jsonl (up to 60):

## qwen-benchmark_runs
- scanned files (0/constant/system): **0**
- matched in jsonl: **0**
- NOT in jsonl: **0**
- sample not-in-jsonl (up to 60):

## Cross-run comparison (only matched pairs)
- common pairs: **0**
- only in qwen-standard_runs: **0**
- only in qwen-benchmark_runs: **0**