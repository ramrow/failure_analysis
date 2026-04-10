#!/usr/bin/env python3
"""
Levenshtein comparison: qwen-standard vs velocity-qwen-standard vs Ground Truth (Basic).

For each case/variant, compares input files (0/, constant/, system/) only.
Produces:
  output/heatmap_standard_vs_gt.png
  output/heatmap_velocity_vs_gt.png
  output/heatmap_standard_vs_velocity.png
  output/bar_case_avg.png
  output/results.json
"""

import json
import re
import sys
from pathlib import Path

try:
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import matplotlib.colors as mcolors
except ImportError:
    sys.exit("pip install numpy matplotlib")

try:
    from Levenshtein import ratio as lev_ratio
except ImportError:
    import difflib
    def lev_ratio(a, b):
        return difflib.SequenceMatcher(None, a, b).ratio()

# ---------------------------------------------------------------------------
ROOT      = Path(__file__).parent
GT_ROOT   = ROOT / "Basic"
STD_ROOT  = ROOT / "qwen-standard_runs"
VEL_ROOT  = ROOT / "velocity-qwen-standard_runs"
OUT_DIR   = ROOT / "levenshtein_output"
OUT_DIR.mkdir(exist_ok=True)

CASES = [
    "BernardCells", "Cavity", "counterFlowFlame2D", "Cylinder",
    "damBreakWithObstacle", "forwardStep", "obliqueShock", "pitzDaily",
    "shallowWaterWithSquareBump", "squareBend", "wedge",
]
VARIANTS = ["1", "2", "3"]

# Only compare these subdirectories (not simulation timestep output folders)
INPUT_DIRS = {"0", "constant", "system"}

# Remove block comments, line comments, and the OpenFOAM file-header separator lines
COMMENT_RE   = re.compile(r"/\*.*?\*/", re.DOTALL)
LINE_CMT_RE  = re.compile(r"//[^\n]*")
# FoamFile { ... } block contains path metadata (location, object) — strip it
FOAMFILE_RE  = re.compile(r"FoamFile\s*\{[^}]*\}", re.DOTALL)
# Collapse runs of blank lines down to one
BLANK_RE     = re.compile(r"\n{3,}")

def strip(text: str) -> str:
    text = COMMENT_RE.sub("", text)
    text = LINE_CMT_RE.sub("", text)
    text = FOAMFILE_RE.sub("", text)
    text = BLANK_RE.sub("\n\n", text)
    return text.strip()

def read(path: Path) -> str:
    try:
        return strip(path.read_text(encoding="utf-8", errors="ignore"))
    except Exception:
        return ""

def gt_input_files(gt_case_dir: Path) -> dict:
    """Return {rel_path_str: text} for all files inside INPUT_DIRS within GT_Files."""
    gt_files_dir = gt_case_dir / "GT_Files"
    result = {}
    for sub in INPUT_DIRS:
        subdir = gt_files_dir / sub
        if subdir.is_dir():
            for f in subdir.rglob("*"):
                if f.is_file():
                    result[str(f.relative_to(gt_files_dir))] = read(f)
    return result

def run_input_files(run_case_dir: Path) -> dict:
    """Return {rel_path_str: text} for all files inside INPUT_DIRS in a run dir."""
    result = {}
    for sub in INPUT_DIRS:
        subdir = run_case_dir / sub
        if subdir.is_dir():
            for f in subdir.rglob("*"):
                if f.is_file():
                    result[str(f.relative_to(run_case_dir))] = read(f)
    return result

def compare_dicts(gt: dict, run: dict) -> float:
    """Average Levenshtein similarity over all GT files."""
    if not gt:
        return float("nan")
    scores = []
    for rel, gt_text in gt.items():
        run_text = run.get(rel, "")
        scores.append(lev_ratio(gt_text, run_text))
    return sum(scores) / len(scores)

# ---------------------------------------------------------------------------
# Build similarity matrices  (cases × variants)
# ---------------------------------------------------------------------------
n_cases, n_var = len(CASES), len(VARIANTS)
std_gt  = np.full((n_cases, n_var), np.nan)
vel_gt  = np.full((n_cases, n_var), np.nan)
std_vel = np.full((n_cases, n_var), np.nan)

records = {}

for i, case in enumerate(CASES):
    records[case] = {}
    for j, var in enumerate(VARIANTS):
        gt_dir  = GT_ROOT  / case / var
        std_dir = STD_ROOT / case / var
        vel_dir = VEL_ROOT / case / var

        gt_files  = gt_input_files(gt_dir)  if gt_dir.is_dir()  else {}
        std_files = run_input_files(std_dir) if std_dir.is_dir() else {}
        vel_files = run_input_files(vel_dir) if vel_dir.is_dir() else {}

        s_gt  = compare_dicts(gt_files, std_files)
        v_gt  = compare_dicts(gt_files, vel_files)
        s_v   = compare_dicts(std_files, vel_files) if std_files else float("nan")

        std_gt[i, j]  = s_gt
        vel_gt[i, j]  = v_gt
        std_vel[i, j] = s_v

        records[case][var] = {
            "standard_vs_gt":  round(s_gt, 4)  if not np.isnan(s_gt)  else None,
            "velocity_vs_gt":  round(v_gt, 4)  if not np.isnan(v_gt)  else None,
            "standard_vs_velocity": round(s_v, 4) if not np.isnan(s_v) else None,
        }

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
TICK_LABELS = [c if len(c) <= 14 else c[:12] + ".." for c in CASES]

def save_heatmap(matrix, title, filepath, cmap="RdYlGn", vmin=0, vmax=1):
    fig, ax = plt.subplots(figsize=(6, 8))
    masked = np.ma.masked_invalid(matrix)
    im = ax.imshow(masked, cmap=cmap, vmin=vmin, vmax=vmax, aspect="auto")
    plt.colorbar(im, ax=ax, label="Levenshtein similarity (0–1)")
    ax.set_xticks(range(n_var))
    ax.set_xticklabels([f"v{v}" for v in VARIANTS])
    ax.set_yticks(range(n_cases))
    ax.set_yticklabels(TICK_LABELS, fontsize=8)
    ax.set_title(title, fontsize=11, pad=10)
    for i in range(n_cases):
        for j in range(n_var):
            val = matrix[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:.2f}", ha="center", va="center",
                        fontsize=7, color="black" if 0.35 < val < 0.85 else "white")
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")

def save_bar_chart(std_gt, vel_gt, filepath):
    std_means = np.nanmean(std_gt, axis=1)
    vel_means = np.nanmean(vel_gt, axis=1)

    x = np.arange(n_cases)
    w = 0.38
    fig, ax = plt.subplots(figsize=(13, 5))
    b1 = ax.bar(x - w/2, std_means, w, label="qwen-standard vs GT",  color="#4C72B0", alpha=0.85)
    b2 = ax.bar(x + w/2, vel_means, w, label="velocity-qwen-standard vs GT", color="#DD8452", alpha=0.85)
    ax.set_xticks(x)
    ax.set_xticklabels(CASES, rotation=35, ha="right", fontsize=8)
    ax.set_ylabel("Avg Levenshtein similarity")
    ax.set_title("Per-case average similarity to Ground Truth")
    ax.set_ylim(0, 1)
    ax.axhline(0.8, color="green", linestyle="--", linewidth=0.8, label="0.80 threshold")
    ax.legend()
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")

def save_delta_heatmap(std_gt, vel_gt, filepath):
    """vel_gt minus std_gt — positive = velocity run is closer to GT."""
    delta = vel_gt - std_gt
    vabs = np.nanmax(np.abs(delta))
    fig, ax = plt.subplots(figsize=(6, 8))
    masked = np.ma.masked_invalid(delta)
    im = ax.imshow(masked, cmap="RdBu", vmin=-vabs, vmax=vabs, aspect="auto")
    plt.colorbar(im, ax=ax, label="Δ similarity (velocity − standard)")
    ax.set_xticks(range(n_var))
    ax.set_xticklabels([f"v{v}" for v in VARIANTS])
    ax.set_yticks(range(n_cases))
    ax.set_yticklabels(TICK_LABELS, fontsize=8)
    ax.set_title("Δ similarity: velocity − standard\n(blue = velocity closer to GT)", fontsize=10, pad=10)
    for i in range(n_cases):
        for j in range(n_var):
            val = delta[i, j]
            if not np.isnan(val):
                ax.text(j, i, f"{val:+.2f}", ha="center", va="center",
                        fontsize=7, color="white" if abs(val) > vabs * 0.6 else "black")
    plt.tight_layout()
    fig.savefig(filepath, dpi=150)
    plt.close(fig)
    print(f"Saved: {filepath}")

# ---------------------------------------------------------------------------
# Generate all outputs
# ---------------------------------------------------------------------------
save_heatmap(std_gt,  "qwen-standard vs Ground Truth",          OUT_DIR / "heatmap_standard_vs_gt.png")
save_heatmap(vel_gt,  "velocity-qwen-standard vs Ground Truth", OUT_DIR / "heatmap_velocity_vs_gt.png")
save_heatmap(std_vel, "qwen-standard vs velocity-qwen-standard\n(agreement between runs)", OUT_DIR / "heatmap_standard_vs_velocity.png", cmap="Blues")
save_bar_chart(std_gt, vel_gt, OUT_DIR / "bar_case_avg.png")
save_delta_heatmap(std_gt, vel_gt, OUT_DIR / "heatmap_delta_velocity_minus_standard.png")

# Summary stats
std_overall = float(np.nanmean(std_gt))
vel_overall = float(np.nanmean(vel_gt))
sv_overall  = float(np.nanmean(std_vel))
summary = {
    "standard_vs_gt_mean":          round(std_overall, 4),
    "velocity_vs_gt_mean":          round(vel_overall, 4),
    "standard_vs_velocity_mean":    round(sv_overall, 4),
    "winner_vs_gt": "velocity-qwen-standard" if vel_overall > std_overall else "qwen-standard",
    "per_case": records,
}
out_json = OUT_DIR / "results.json"
out_json.write_text(json.dumps(summary, indent=2), encoding="utf-8")
print(f"Saved: {out_json}")

print("\n=== SUMMARY ===")
print(f"qwen-standard vs GT:          {std_overall:.4f}")
print(f"velocity-qwen-standard vs GT: {vel_overall:.4f}")
print(f"standard vs velocity (agreement): {sv_overall:.4f}")
print(f"Winner vs GT: {summary['winner_vs_gt']}")

