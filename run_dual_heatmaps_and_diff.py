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
exclude = {"dambreakwithobstacle"}


def strip_comments(t):
    o = []
    for ln in t.splitlines():
        s = ln.strip()
        if s.startswith("//") or s.startswith("#") or s.startswith("/*") or s.startswith("*"):
            continue
        o.append(ln)
    return "\n".join(o)


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
for case_dir in B.iterdir():
    if not case_dir.is_dir():
        continue
    case = case_dir.name
    if case.lower() in exclude:
        continue
    gt = case_dir / "1" / "GT_files"
    if not gt.exists():
        continue
    for p in gt.rglob("*"):
        if not p.is_file():
            continue
        rel = p.relative_to(gt).as_posix()
        top = rel.split("/", 1)[0]
        if top not in {"0", "constant", "system"}:
            continue
        g = read(p, strip=True)
        fname = Path(rel).name
        rec = {"case": case, "relpath": rel, "file_name": fname}
        for rn, rr in runs.items():
            rp = rr / case / "1" / rel
            rt = read(rp, strip=False)
            rec[f"{rn}_exists"] = rp.exists()
            rec[f"{rn}_sim"] = sim(g, rt)
        rows.append(rec)


df = pd.DataFrame(rows)
df.to_json(out / "detailed_records.json", orient="records", indent=2)

cases = sorted(df["case"].unique().tolist())
files = sorted(df["file_name"].unique().tolist())


def heat(run_name, fname, cmap, title):
    mat = np.full((len(cases), len(files)), np.nan)
    for i, c in enumerate(cases):
        for j, f in enumerate(files):
            sub = df[(df.case == c) & (df.file_name == f)]
            if len(sub) > 0:
                mat[i, j] = sub[f"{run_name}_sim"].mean() * 100.0
    fig = plt.figure(figsize=(max(10, len(files) * 0.55), max(7, len(cases) * 0.4)))
    ax = fig.add_subplot(111)
    im = ax.imshow(mat, aspect="auto", vmin=0, vmax=100, cmap=cmap)
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


heat("benchmark", "heatmap_benchmark_only.png", "viridis", "Benchmark only: Case x FileName match (%)")
heat("standard", "heatmap_standard_only.png", "plasma", "Standard only: Case x FileName match (%)")

# Difference chart 1: file-wise delta (standard-benchmark)
file_grp = df.groupby("file_name")[["benchmark_sim", "standard_sim"]].mean().reset_index()
file_grp["delta_std_minus_bench"] = file_grp["standard_sim"] - file_grp["benchmark_sim"]
file_grp = file_grp.sort_values("delta_std_minus_bench", ascending=False)
file_grp.to_csv(out / "file_level_difference.csv", index=False)

fig = plt.figure(figsize=(max(10, len(file_grp) * 0.45), 4.5))
ax = fig.add_subplot(111)
ax.bar(
    file_grp["file_name"],
    file_grp["delta_std_minus_bench"] * 100.0,
    color=["#2ca02c" if x >= 0 else "#d62728" for x in file_grp["delta_std_minus_bench"]],
)
ax.axhline(0, color="black", linewidth=1)
ax.set_ylabel("Standard - Benchmark (percentage points)")
ax.set_title("File-level match difference vs Basic")
ax.tick_params(axis="x", rotation=50)
fig.tight_layout()
fig.savefig(out / "file_level_delta_bar.png", dpi=220)
plt.close(fig)

# Difference chart 2: case-wise side-by-side
case_grp = df.groupby("case")[["benchmark_sim", "standard_sim"]].mean().reset_index().sort_values("case")
case_grp.to_csv(out / "case_level_comparison.csv", index=False)
x = np.arange(len(case_grp))
w = 0.38
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

summary = []
summary.append("# Dual heatmaps + difference analysis")
summary.append("")
summary.append("Included files: 0/, constant/, system/ (Allrun copy applied in standard runs source; analysis scope is OpenFOAM dict trees).")
summary.append("Excluded case: damBreakWithObstacle")
summary.append("")
summary.append("## Outputs")
for p in [
    "heatmap_benchmark_only.png",
    "heatmap_standard_only.png",
    "file_level_delta_bar.png",
    "case_level_comparison_bars.png",
    "file_level_difference.csv",
    "case_level_comparison.csv",
]:
    summary.append(f"- {out / p}")
summary.append("")
summary.append("## Overall means")
summary.append(f"- Benchmark mean: {df['benchmark_sim'].mean() * 100:.2f}%")
summary.append(f"- Standard mean: {df['standard_sim'].mean() * 100:.2f}%")
(root / "summary_dual_heatmaps_and_differences.md").write_text("\n".join(summary), encoding="utf-8")
print("WROTE", root / "summary_dual_heatmaps_and_differences.md")
print("WROTE_DIR", out)
