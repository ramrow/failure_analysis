import json
import re
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict

ROOT = Path(r"C:\Users\Peijing Xu\projects\yue_research\error_analysis")
BASIC = ROOT / "Basic"
RUN_ROOTS = {
    "benchmark": ROOT / "qwen-benchmark_runs",
    "standard": ROOT / "qwen-standard_runs",
}
OUT_MD = ROOT / "summary_pass_fail_analysis.md"
OUT_JSON = ROOT / "summary_pass_fail_analysis.json"

CASE_IDS = ["1", "2", "3"]
ERROR_PATTERNS = [
    re.compile(r"\bERROR:\b", re.IGNORECASE),
    re.compile(r"\bFoam::error\b", re.IGNORECASE),
    re.compile(r"\bTraceback\b", re.IGNORECASE),
    re.compile(r"\bFATAL\b", re.IGNORECASE),
]


def strip_comments(text: str) -> str:
    out = []
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("//") or s.startswith("#") or s.startswith("/*") or s.startswith("*"):
            continue
        out.append(line)
    return "\n".join(out)


def read_text(path: Path, strip=False):
    if not path.exists() or not path.is_file():
        return None
    t = path.read_text(encoding="utf-8", errors="ignore")
    return strip_comments(t) if strip else t


def sim(a: str, b: str) -> float:
    if a is None or b is None:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


def gt_files(case_name: str):
    gt_root = BASIC / case_name / "1" / "GT_files"
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
            files.append(rel)
    return sorted(files)


def has_success_time_dir(run_case_dir: Path) -> bool:
    if not run_case_dir.exists():
        return False
    for p in run_case_dir.iterdir():
        if p.is_dir() and p.name != "0":
            try:
                float(p.name)
                return True
            except Exception:
                pass
    return False


def collect_errors(run_case_dir: Path):
    errs = []
    for p in run_case_dir.rglob("*"):
        if not p.is_file():
            continue
        n = p.name.lower()
        if not (n.startswith("log") or n.endswith(".err") or n.endswith(".out")):
            continue
        t = read_text(p)
        if not t:
            continue
        for pat in ERROR_PATTERNS:
            m = pat.search(t)
            if m:
                snippet = t[max(0, m.start()-120):m.start()+220].replace("\n", " ")
                errs.append({"file": str(p), "pattern": pat.pattern, "snippet": snippet})
                break
    return errs


def analyze_case(run_root: Path, case_name: str, case_id: str):
    run_case = run_root / case_name / case_id
    rels = gt_files(case_name)

    file_scores = []
    missing = []
    for rel in rels:
        gt_path = BASIC / case_name / "1" / "GT_files" / rel
        run_path = run_case / rel
        g = read_text(gt_path, strip=True)
        r = read_text(run_path, strip=True)
        if r is None:
            missing.append(rel)
            continue
        s = sim(g, r)
        file_scores.append({"rel": rel, "sim": s})

    avg_sim = sum(x["sim"] for x in file_scores) / len(file_scores) if file_scores else 0.0
    high_sim = sum(1 for x in file_scores if x["sim"] >= 0.95)
    coverage = len(file_scores) / len(rels) if rels else 0.0

    success_time = has_success_time_dir(run_case)
    errs = collect_errors(run_case)

    # decision heuristics
    if success_time and not errs:
        status = "PASS_EXECUTED"
        reason = "Found numeric time directory and no detected error signatures."
    elif success_time and errs:
        status = "UNSTABLE_EXECUTED"
        reason = "Execution artifacts exist, but error signatures detected in logs."
    elif coverage >= 0.9 and avg_sim >= 0.9 and not errs:
        status = "GOOD_FILES_NO_EXECUTION_PROOF"
        reason = "Generated files closely match GT; no explicit execution success artifact found."
    else:
        status = "FAIL_OR_POOR"
        reason = "Insufficient GT alignment and/or explicit errors and/or no execution artifact."

    return {
        "case": case_name,
        "case_id": case_id,
        "status": status,
        "reason": reason,
        "coverage": coverage,
        "avg_similarity": avg_sim,
        "high_similarity_files": high_sim,
        "compared_files": len(file_scores),
        "gt_files_total": len(rels),
        "missing_files": missing[:40],
        "top_mismatches": sorted(file_scores, key=lambda x: x["sim"])[:8],
        "error_hits": errs[:8],
        "has_time_dir": success_time,
        "run_path": str(run_case),
    }


def main():
    all_results = {}
    status_counts = {}

    case_names = sorted([d.name for d in BASIC.iterdir() if d.is_dir() and d.name.lower() != "dambreakwithobstacle"])

    for run_name, run_root in RUN_ROOTS.items():
        rows = []
        for c in case_names:
            for cid in CASE_IDS:
                rows.append(analyze_case(run_root, c, cid))
        all_results[run_name] = rows
        cnt = defaultdict(int)
        for r in rows:
            cnt[r["status"]] += 1
        status_counts[run_name] = dict(cnt)

    payload = {
        "cases": case_names,
        "case_ids": CASE_IDS,
        "status_counts": status_counts,
        "results": all_results,
    }
    OUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    lines = []
    lines.append("# OpenFOAM10 Pass/Fail Error Analysis (Cases 1/2/3)")
    lines.append("")
    lines.append("Reference: Basic/<case>/1/GT_files (comments ignored).")
    lines.append("Exclusions: damBreakWithObstacle and Allrun.")
    lines.append("")

    for run_name in RUN_ROOTS:
        lines.append(f"## {run_name}")
        for k, v in sorted(status_counts[run_name].items()):
            lines.append(f"- {k}: **{v}**")
        lines.append("")

        bad = [r for r in all_results[run_name] if r["status"] in {"FAIL_OR_POOR", "UNSTABLE_EXECUTED"}]
        good = [r for r in all_results[run_name] if r["status"] in {"PASS_EXECUTED", "GOOD_FILES_NO_EXECUTION_PROOF"}]

        lines.append("### Good / potentially pass examples")
        for r in good[:20]:
            lines.append(f"- {r['case']}/{r['case_id']} | {r['status']} | coverage={r['coverage']:.2%} avg_sim={r['avg_similarity']:.3f}")
        lines.append("")

        lines.append("### Fail / error-analysis examples")
        for r in bad[:25]:
            lines.append(f"- {r['case']}/{r['case_id']} | {r['status']} | {r['reason']}")
            if r["error_hits"]:
                eh = r["error_hits"][0]
                lines.append(f"  - error file: {Path(eh['file']).name} | snippet: {eh['snippet'][:180]}")
            elif r["top_mismatches"]:
                tm = r["top_mismatches"][0]
                lines.append(f"  - worst file mismatch: {tm['rel']} (sim={tm['sim']:.3f})")
        lines.append("")

    # simple winner by avg similarity across all case-id combinations
    avg_run = {}
    for rn, rows in all_results.items():
        avg_run[rn] = sum(r["avg_similarity"] for r in rows) / len(rows) if rows else 0.0
    winner = max(avg_run, key=avg_run.get)

    lines.append("## Overall alignment winner")
    for rn, v in avg_run.items():
        lines.append(f"- {rn}: mean avg_similarity={v:.4f}")
    lines.append(f"- Winner: **{winner}**")

    OUT_MD.write_text("\n".join(lines), encoding="utf-8")
    print("WROTE", OUT_MD)
    print("WROTE", OUT_JSON)


if __name__ == "__main__":
    main()
