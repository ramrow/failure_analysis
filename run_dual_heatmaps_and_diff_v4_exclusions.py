import re
import numpy as np
from pathlib import Path
from difflib import SequenceMatcher
import matplotlib.pyplot as plt
import pandas as pd

root = Path(r"C:\Users\Peijing Xu\projects\yue_research\error_analysis")
B = root / "Basic"
runs = {
    "benchmark": root / "qwen-benchmark_runs",
    "standard": root / "qwen-standard_runs",
}
out = root / "analysis_output_dual"
out.mkdir(exist_ok=True)


def strip_comments(t):
    out = []
    for ln in t.splitlines():
        # Remove only // comment suffix, keep left-side content.
        # Example: "foam // comment" -> "foam"
        if "//" in ln:
            ln = ln.split("//", 1)[0].rstrip()
        # Keep non-empty lines; if a line is only comment it becomes empty and is dropped.
        if ln.strip() == "":
            continue
        out.append(ln)
    return "\n".join(out)


def read(p, strip=False):
    if not p.exists() or not p.is_file():
        return None
    t = p.read_text(encoding="utf-8", errors="ignore")
    return strip_comments(t) if strip else t


def sim(a, b):
    if a is None or b is None:
        return 0.0
    return SequenceMatcher(None, a, b).ratio()


rows = []
missing_rows = []
for case_dir in B.iterdir():
    if not case_dir.is_dir():
        continue
    case = case_dir.name
    gt = case_dir / "1" / "GT_files"
    if not gt.exists():
        continue
    for p in gt.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(gt).as_posix()

        top = rel.split("/", 1)[0]
        if not (top in {"0", "constant", "system"} or rel == "Allrun"):
            continue
        if rel.startswith("constant/polyMesh/"):
            continue
        if Path(rel).name == "functions":
            continue

        g = read(p, strip=True)
        fname = Path(rel).name
        rec = {"case": case, "relpath": rel, "file_name": fname}
        for rn, rr in runs.items():
            rp = rr / case / "1" / rel
            exists = rp.exists()
            rt = read(rp, strip=False)
            rec[f"{rn}_exists"] = exists
            rec[f"{rn}_sim"] = sim(g, rt)
            if not exists:
                missing_rows.append({
                    "run": rn,
                    "case": case,
                    "relpath": rel,
                    "file_name": fname,
                    "basic_file": str(p),
                    "expected_run_file": str(rp),
                })
        rows.append(rec)


df = pd.DataFrame(rows)
miss_df = pd.DataFrame(missing_rows)

if len(df) == 0:
    raise SystemExit("No rows to compare after exclusions.")

df.to_json(out / "detailed_records.json", orient="records", indent=2)
miss_df.to_csv(out / "missing_files_vs_basic.csv", index=False)
if len(miss_df) > 0:
    miss_df[miss_df["run"] == "standard"].to_csv(out / "missing_files_standard_vs_basic.csv", index=False)
else:
    pd.DataFrame(columns=["run","case","relpath","file_name","basic_file","expected_run_file"]).to_csv(out / "missing_files_standard_vs_basic.csv", index=False)

cases = sorted(df["case"].unique().tolist())
files = sorted(df["file_name"].unique().tolist())


def heat(run_name, fname, title):
    mat = np.full((len(cases), len(files)), np.nan)
    for i, c in enumerate(cases):
        for j, f in enumerate(files):
            sub = df[(df.case == c) & (df.file_name == f)]
            if len(sub) > 0:
                mat[i, j] = sub[f"{run_name}_sim"].mean() * 100.0
    fig = plt.figure(figsize=(max(10, len(files) * 0.55), max(7, len(cases) * 0.4)))
    ax = fig.add_subplot(111)
    im = ax.imshow(mat, aspect="auto", vmin=0, vmax=100, cmap="plasma")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label(f"{run_name} match (%)")
    ax.set_xticks(np.arange(len(files)))
    ax.set_xticklabels(files, rotation=50, ha="right")
    ax.set_yticks(np.arange(len(cases)))
    ax.set_yticklabels(cases)
    ax.set_xlabel("file_name")
    ax.set_ylabel("case_name")
    ax.set_title(title)
    fig.tight_layout()
    fig.savefig(out / fname, dpi=220)
    plt.close(fig)

heat("benchmark", "heatmap_benchmark_only.png", "Benchmark only: Case x FileName match (%)")
heat("standard", "heatmap_standard_only.png", "Standard only: Case x FileName match (%)")

file_grp = df.groupby("file_name")[["benchmark_sim", "standard_sim"]].mean().reset_index()
file_grp["delta_std_minus_bench"] = file_grp["standard_sim"] - file_grp["benchmark_sim"]
file_grp = file_grp.sort_values("delta_std_minus_bench", ascending=False)
file_grp.to_csv(out / "file_level_difference.csv", index=False)

fig = plt.figure(figsize=(max(10, len(file_grp) * 0.45), 4.5))
ax = fig.add_subplot(111)
ax.bar(file_grp["file_name"], file_grp["delta_std_minus_bench"] * 100.0,
       color=["#2ca02c" if x >= 0 else "#d62728" for x in file_grp["delta_std_minus_bench"]])
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Standard - Benchmark (percentage points)")
ax.set_title("File-level match difference vs Basic")
ax.tick_params(axis="x", rotation=50)
fig.tight_layout()
fig.savefig(out / "file_level_delta_bar.png", dpi=220)
plt.close(fig)

case_grp = df.groupby("case")[["benchmark_sim", "standard_sim"]].mean().reset_index().sort_values("case")
case_grp.to_csv(out / "case_level_comparison.csv", index=False)
x = np.arange(len(case_grp)); w = 0.38
fig = plt.figure(figsize=(max(10, len(case_grp) * 0.65), 4.5))
ax = fig.add_subplot(111)
ax.bar(x - w / 2, case_grp["benchmark_sim"] * 100.0, width=w, label="benchmark")
ax.bar(x + w / 2, case_grp["standard_sim"] * 100.0, width=w, label="standard")
ax.set_xticks(x)
ax.set_xticklabels(case_grp["case"], rotation=45, ha="right")
ax.set_ylabel("Match to Basic (%)")
ax.set_title("Case-level comparison vs Basic")
ax.legend()
fig.tight_layout()
fig.savefig(out / "case_level_comparison_bars.png", dpi=220)
plt.close(fig)

miss_summary = miss_df.groupby(["run", "case"]).size().reset_index(name="missing_count") if len(miss_df) > 0 else pd.DataFrame(columns=["run", "case", "missing_count"])
miss_summary.to_csv(out / "missing_files_summary_by_case.csv", index=False)

summary = []
summary.append("# Dual heatmaps + overall summary (v4, inline comments stripped)")
summary.append("")
summary.append("Comparison scope includes Allrun + 0/ + constant/ + system/.")
summary.append("Exclusions applied: constant/polyMesh/** and any file named functions.")
summary.append("Basic comments stripped before compare (inline // comments only).")
summary.append("")
summary.append(f"Total file comparisons: {len(df)}")
summary.append(f"Benchmark mean match: {df['benchmark_sim'].mean() * 100:.2f}%")
summary.append(f"Standard mean match: {df['standard_sim'].mean() * 100:.2f}%")

(root / "summary_dual_heatmaps_and_differences.md").write_text("\n".join(summary), encoding="utf-8")
print("UPDATED_WITH_INLINE_COMMENT_STRIP")

