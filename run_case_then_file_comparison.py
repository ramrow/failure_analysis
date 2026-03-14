import json
from pathlib import Path
from difflib import SequenceMatcher
from collections import defaultdict
import matplotlib.pyplot as plt
import numpy as np

ROOT = Path(r"C:\Users\Peijing Xu\projects\yue_research\error_analysis")
BASIC = ROOT / "Basic"
RUNS = {
    "benchmark": ROOT / "qwen-benchmark_runs",
    "standard": ROOT / "qwen-standard_runs",
}
OUT = ROOT / "analysis_output_case_file"
OUT.mkdir(parents=True, exist_ok=True)

EXCLUDE_CASES = {"dambreakwithobstacle"}


def strip_comments(t: str) -> str:
    out=[]
    for line in t.splitlines():
        s=line.strip()
        if s.startswith('//') or s.startswith('#') or s.startswith('/*') or s.startswith('*'):
            continue
        out.append(line)
    return "\n".join(out)


def read_text(p: Path, strip=False):
    if not p.exists() or not p.is_file():
        return None
    t=p.read_text(encoding='utf-8', errors='ignore')
    return strip_comments(t) if strip else t


def sim(a,b):
    if a is None or b is None:
        return 0.0
    return SequenceMatcher(None,a,b).ratio()


def gt_file_map(case_dir: Path):
    gt = case_dir / '1' / 'GT_files'
    m={}
    if not gt.exists():
        return m
    for p in gt.rglob('*'):
        if not p.is_file():
            continue
        rel=p.relative_to(gt).as_posix()
        top=rel.split('/',1)[0]
        if top not in {'0','constant','system'}:
            continue
        if p.name=='Allrun':
            continue
        m[rel]=p
    return m

records=[]
by_case_file=defaultdict(lambda: defaultdict(dict))  # case->file->run->sim
by_case_rel=defaultdict(lambda: defaultdict(dict))   # case->rel->run->sim

for case_dir in BASIC.iterdir():
    if not case_dir.is_dir():
        continue
    case=case_dir.name
    if case.lower() in EXCLUDE_CASES:
        continue
    gt_map=gt_file_map(case_dir)
    for rel,gtp in sorted(gt_map.items()):
        fname=Path(rel).name
        gt_text=read_text(gtp, strip=True)
        row={"case":case,"relpath":rel,"file_name":fname}
        for run_name, run_root in RUNS.items():
            rp = run_root / case / '1' / rel
            rtxt=read_text(rp, strip=False)
            s=sim(gt_text, rtxt)
            row[f"{run_name}_sim"]=s
            row[f"{run_name}_exists"]=bool(rp.exists())
            by_case_file[case][fname][run_name]=max(by_case_file[case][fname].get(run_name,0.0), s)
            by_case_rel[case][rel][run_name]=s
        records.append(row)

# summary by case then file_name
summary={}
for case, files in by_case_file.items():
    summary[case]={}
    for fname, d in files.items():
        b=d.get('benchmark',0.0); s=d.get('standard',0.0)
        summary[case][fname]={
            'benchmark_sim': b,
            'standard_sim': s,
            'winner': 'benchmark' if b>s else ('standard' if s>b else 'tie')
        }

(OUT/'case_file_similarity.json').write_text(json.dumps(summary, indent=2), encoding='utf-8')
(OUT/'detailed_records.json').write_text(json.dumps(records, indent=2), encoding='utf-8')

# Graph 1: case-level average similarity (grouped bars)
cases=sorted(by_case_rel.keys())
bench_case=[]; std_case=[]
for c in cases:
    vals=list(by_case_rel[c].values())
    bench_case.append(sum(v.get('benchmark',0.0) for v in vals)/len(vals) if vals else 0.0)
    std_case.append(sum(v.get('standard',0.0) for v in vals)/len(vals) if vals else 0.0)

x=np.arange(len(cases)); w=0.38
plt.figure(figsize=(max(10,len(cases)*0.7),4.2))
plt.bar(x-w/2, bench_case, width=w, label='benchmark')
plt.bar(x+w/2, std_case, width=w, label='standard')
plt.xticks(x, cases, rotation=45, ha='right')
plt.ylim(0,1)
plt.ylabel('Mean similarity')
plt.title('Case-wise similarity (case_name first)')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'casewise_similarity.png', dpi=170)
plt.close()

# Graph 2: file-name-level average similarity (across all cases)
file_names=sorted({r['file_name'] for r in records})
bench_f=[]; std_f=[]
for fn in file_names:
    rows=[r for r in records if r['file_name']==fn]
    bench_f.append(sum(r['benchmark_sim'] for r in rows)/len(rows) if rows else 0.0)
    std_f.append(sum(r['standard_sim'] for r in rows)/len(rows) if rows else 0.0)

x=np.arange(len(file_names))
plt.figure(figsize=(max(10,len(file_names)*0.8),4.2))
plt.bar(x-w/2, bench_f, width=w, label='benchmark')
plt.bar(x+w/2, std_f, width=w, label='standard')
plt.xticks(x, file_names, rotation=45, ha='right')
plt.ylim(0,1)
plt.ylabel('Mean similarity')
plt.title('File-name-wise similarity (then file_name)')
plt.legend()
plt.tight_layout()
plt.savefig(OUT/'filename_similarity.png', dpi=170)
plt.close()

# Graph 3: heatmap for best run per case/file_name
matrix=np.full((len(cases), len(file_names)), np.nan)
for i,c in enumerate(cases):
    for j,fn in enumerate(file_names):
        entry=summary.get(c,{}).get(fn)
        if entry:
            matrix[i,j]=max(entry['benchmark_sim'], entry['standard_sim'])

plt.figure(figsize=(max(8,len(file_names)*0.5), max(6,len(cases)*0.35)))
im=plt.imshow(matrix, aspect='auto', vmin=0, vmax=1)
plt.colorbar(im, label='Best similarity')
plt.yticks(np.arange(len(cases)), cases)
plt.xticks(np.arange(len(file_names)), file_names, rotation=45, ha='right')
plt.title('Case x FileName best similarity heatmap')
plt.tight_layout()
plt.savefig(OUT/'case_file_heatmap.png', dpi=170)
plt.close()

md=[]
md.append('# Case-then-File Character Comparison Summary')
md.append('')
md.append('Organized as: case_name first, then file_name.')
md.append('Exclusions: damBreakWithObstacle, Allrun; Basic comments ignored.')
md.append('')
md.append(f'- Cases analyzed: **{len(cases)}**')
md.append(f'- Distinct file names analyzed: **{len(file_names)}**')
md.append(f'- Total file comparisons: **{len(records)}**')
md.append('')
md.append('## Charts')
md.append(f'- {OUT / "casewise_similarity.png"}')
md.append(f'- {OUT / "filename_similarity.png"}')
md.append(f'- {OUT / "case_file_heatmap.png"}')
md.append('')
md.append('## Per-case winners by file_name (sample)')
for c in cases[:10]:
    md.append(f'### {c}')
    for fn in sorted(summary[c].keys())[:20]:
        e=summary[c][fn]
        md.append(f"- {fn}: winner={e['winner']} (bench={e['benchmark_sim']:.3f}, std={e['standard_sim']:.3f})")

(ROOT/'summary_report_case_then_file.md').write_text('\n'.join(md), encoding='utf-8')
print('WROTE', ROOT/'summary_report_case_then_file.md')
print('WROTE_DIR', OUT)
