import json
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
import matplotlib.pyplot as plt

ROOT = Path(r"C:\Users\Peijing Xu\projects\yue_research\error_analysis")
BASIC = ROOT / "Basic"
RUNS = {
    "qwen-benchmark_runs": ROOT / "qwen-benchmark_runs",
    "qwen-standard_runs": ROOT / "qwen-standard_runs",
}
OUT_DIR = ROOT / "analysis_output"
OUT_DIR.mkdir(parents=True, exist_ok=True)

def strip_basic_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("//") or s.startswith("#") or s.startswith("/*") or s.startswith("*"):
            continue
        out.append(line)
    return "\n".join(out)

def read_text(p: Path, strip_comments=False):
    try:
        t = p.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return None
    return strip_basic_comments(t) if strip_comments else t

def char_accuracy(a: str, b: str) -> float:
    if a is None or b is None:
        return 0.0
    n = max(len(a), len(b))
    if n == 0:
        return 1.0
    m = sum(1 for x, y in zip(a, b) if x == y)
    return m / n

def similarity(a: str, b: str) -> float:
    if a is None or b is None:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()

def gt_files_for_case(case_dir: Path):
    gt_root = case_dir / "1" / "GT_files"
    files = []
    if not gt_root.exists():
        return files
    for p in gt_root.rglob("*"):
        if p.is_file():
            rel = p.relative_to(gt_root).as_posix()
            parts = rel.split("/")
            if parts[0] not in {"0", "constant", "system"}:
                continue
            if p.name == "Allrun":
                continue
            files.append((rel, p))
    return sorted(files)

def run_file_path(run_root: Path, case: str, rel: str):
    return run_root / case / "1" / rel

records = []
case_scores = defaultdict(lambda: {"qwen-benchmark_runs": [], "qwen-standard_runs": []})

for case_dir in BASIC.iterdir():
    if not case_dir.is_dir():
        continue
    case = case_dir.name
    if case.lower() == "dambreakwithobstacle":
        continue
    gt_files = gt_files_for_case(case_dir)
    for rel, gt_path in gt_files:
        gt_text = read_text(gt_path, strip_comments=True)
        rec = {"case": case, "relpath": rel}
        for run_name, run_root in RUNS.items():
            rp = run_file_path(run_root, case, rel)
            exists = rp.exists()
            run_text = read_text(rp) if exists else None
            sim = similarity(gt_text, run_text)
            acc = char_accuracy(gt_text, run_text)
            rec[f"{run_name}_exists"] = exists
            rec[f"{run_name}_sim"] = sim
            rec[f"{run_name}_char_acc"] = acc
            case_scores[case][run_name].append(sim)
        records.append(rec)

winner_counts = {"qwen-benchmark_runs": 0, "qwen-standard_runs": 0, "tie": 0}
for r in records:
    a = r["qwen-benchmark_runs_sim"]
    b = r["qwen-standard_runs_sim"]
    if abs(a - b) < 1e-12:
        winner_counts["tie"] += 1
    elif a > b:
        winner_counts["qwen-benchmark_runs"] += 1
    else:
        winner_counts["qwen-standard_runs"] += 1

agg = {}
for run_name in RUNS:
    sims = [r[f"{run_name}_sim"] for r in records]
    accs = [r[f"{run_name}_char_acc"] for r in records]
    exists = [r[f"{run_name}_exists"] for r in records]
    agg[run_name] = {
        "mean_similarity": sum(sims) / len(sims) if sims else 0,
        "mean_char_accuracy": sum(accs) / len(accs) if accs else 0,
        "coverage": sum(1 for x in exists if x) / len(exists) if exists else 0,
    }

labels = list(RUNS.keys())
plt.figure(figsize=(6, 4))
plt.bar(labels, [agg[k]["mean_similarity"] for k in labels])
plt.ylabel("Mean similarity to Basic GT")
plt.title("Overall similarity (excluding Allrun + damBreakWithObstacle)")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(OUT_DIR / "overall_similarity.png", dpi=160)
plt.close()

plt.figure(figsize=(6, 4))
plt.bar(labels, [agg[k]["coverage"] for k in labels])
plt.ylabel("Coverage of GT files")
plt.title("File presence vs Basic GT")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(OUT_DIR / "coverage.png", dpi=160)
plt.close()

cases = sorted(case_scores.keys())
bench_case = [sum(case_scores[c]["qwen-benchmark_runs"]) / len(case_scores[c]["qwen-benchmark_runs"]) if case_scores[c]["qwen-benchmark_runs"] else 0 for c in cases]
std_case = [sum(case_scores[c]["qwen-standard_runs"]) / len(case_scores[c]["qwen-standard_runs"]) if case_scores[c]["qwen-standard_runs"] else 0 for c in cases]

x = list(range(len(cases)))
w = 0.4
plt.figure(figsize=(max(10, len(cases) * 0.7), 4))
plt.bar([i - w / 2 for i in x], bench_case, width=w, label="benchmark")
plt.bar([i + w / 2 for i in x], std_case, width=w, label="standard")
plt.xticks(x, cases, rotation=45, ha="right")
plt.ylim(0, 1)
plt.ylabel("Mean similarity")
plt.title("Case-wise similarity")
plt.legend()
plt.tight_layout()
plt.savefig(OUT_DIR / "casewise_similarity.png", dpi=160)
plt.close()

(OUT_DIR / "detailed_records.json").write_text(json.dumps(records, indent=2), encoding="utf-8")

lines = []
lines.append("# Comparison to Basic GT (updated)")
lines.append("")
lines.append("Exclusions: Allrun + damBreakWithObstacle")
lines.append("Comments removed from Basic GT before compare: //, #, /*, *")
lines.append("")
lines.append(f"Total comparable GT files: **{len(records)}**")
lines.append("")
for run_name in RUNS:
    a = agg[run_name]
    lines.append(f"## {run_name}")
    lines.append(f"- mean similarity: **{a['mean_similarity']:.4f}**")
    lines.append(f"- mean char accuracy: **{a['mean_char_accuracy']:.4f}**")
    lines.append(f"- coverage: **{a['coverage']:.2%}**")
    lines.append("")
lines.append("## Winner count by file")
lines.append(f"- benchmark wins: **{winner_counts['qwen-benchmark_runs']}**")
lines.append(f"- standard wins: **{winner_counts['qwen-standard_runs']}**")
lines.append(f"- ties: **{winner_counts['tie']}**")

better = "qwen-benchmark_runs" if agg['qwen-benchmark_runs']['mean_similarity'] > agg['qwen-standard_runs']['mean_similarity'] else "qwen-standard_runs"
lines.append("")
lines.append(f"## Overall closer to Basic GT: **{better}**")

(ROOT / "summary_report_basic_compare.md").write_text("\n".join(lines), encoding="utf-8")
print("done")
