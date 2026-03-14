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

heat("benchmark", "heatmap_benchmark_only.png", "Benchmark only: Case x FileName match (%) [including Allrun]")
heat("standard", "heatmap_standard_only.png", "Standard only: Case x FileName match (%) [including Allrun]")

summary = []
summary.append("# Dual heatmaps + difference analysis (v3)")
summary.append("")
summary.append("Included files: 0/, constant/, system/, and Allrun.")
summary.append("Basic comments are stripped before comparison.")
summary.append(f"Total rows compared: {len(df)}")
(root / "summary_dual_heatmaps_and_differences.md").write_text("\n".join(summary), encoding="utf-8")
print("UPDATED_HEATMAPS_WITH_ALLRUN")
