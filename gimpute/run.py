"""Run one paper version through the shared protocol.

    python -m gimpute.run --paper rossi2020-fp --version v1
    python -m gimpute.run --paper baseline-mean --version v1 --datasets cora,citeseer --rates 0.5,0.99

Defaults (datasets, mechanisms, rates, seeds) come from configs/protocol.yaml; command-line
values override them. The method's own settings come from papers/<slug>/<version>/configs/default.yaml
(or --config). Each finished cell is appended to the version's results.jsonl at once, and cells
already present are skipped, so an interrupted run can simply be started again.
"""
from __future__ import annotations

import argparse
import datetime
import itertools
import json
import subprocess
import sys
from pathlib import Path

import torch
import yaml

from .methods import load_method
from .protocol import evaluate_cell

ROOT = Path(__file__).resolve().parents[1]
KEY = ("dataset", "mechanism", "rate", "seed")


def results_path(paper: str, version: str) -> Path:
    if paper.startswith("baseline-"):
        return ROOT / "reports" / "baselines" / f"{paper.removeprefix('baseline-')}.jsonl"
    return ROOT / "papers" / paper / version / "results" / "results.jsonl"


def read_rows(path: Path) -> list:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def git_commit() -> str:
    try:
        rev = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        dirty = subprocess.run(["git", "status", "--porcelain", "--untracked-files=no"], cwd=ROOT, capture_output=True, text=True).stdout.strip()
        return rev + ("-dirty" if dirty else "")
    except OSError:
        return "unknown"


def parse_seeds(text: str) -> list:
    if "-" in text:
        a, b = text.split("-")
        return list(range(int(a), int(b) + 1))
    return [int(s) for s in text.split(",")]


def main(argv=None) -> int:
    proto = yaml.safe_load((ROOT / "configs" / "protocol.yaml").read_text(encoding="utf-8"))
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--paper", required=True)
    p.add_argument("--version", default="v1")
    p.add_argument("--datasets", help="comma-separated; default from configs/protocol.yaml")
    p.add_argument("--mechanisms", help="comma-separated: uniform,structural")
    p.add_argument("--rates", help="comma-separated missing rates")
    p.add_argument("--seeds", help="e.g. 0-4 or 0,1,2")
    p.add_argument("--config", help="method config YAML (default: the version's configs/default.yaml)")
    p.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu")
    p.add_argument("--force", action="store_true", help="re-run cells that already have results")
    a = p.parse_args(argv)

    datasets = a.datasets.split(",") if a.datasets else proto["datasets"]
    mechanisms = a.mechanisms.split(",") if a.mechanisms else proto["mechanisms"]
    rates = [float(r) for r in a.rates.split(",")] if a.rates else proto["rates"]
    seeds = parse_seeds(a.seeds) if a.seeds else proto["seeds"]

    cfg_path = Path(a.config) if a.config else ROOT / "papers" / a.paper / a.version / "configs" / "default.yaml"
    config = (yaml.safe_load(cfg_path.read_text(encoding="utf-8")) or {}) if cfg_path.exists() else {}
    method = load_method(a.paper, a.version)(config)

    out = results_path(a.paper, a.version)
    out.parent.mkdir(parents=True, exist_ok=True)
    done = set() if a.force else {tuple(r[k] for k in KEY) for r in read_rows(out)}
    commit = git_commit()
    cells = list(itertools.product(datasets, mechanisms, rates, seeds))
    print(f"{a.paper}/{a.version}: {len(cells)} cells, {sum(c in done for c in cells)} already done, device={a.device}")
    failures = 0
    for dataset, mechanism, rate, seed in cells:
        if (dataset, mechanism, rate, seed) in done:
            continue
        row = {"paper": a.paper, "version": a.version, "dataset": dataset, "mechanism": mechanism, "rate": rate, "seed": seed}
        try:
            row.update(evaluate_cell(method, dataset, mechanism, rate, seed, a.device))
        except Exception as e:  # keep going: one failing cell must not lose the rest of a long run
            failures += 1
            print(f"  FAILED {dataset} {mechanism} {rate} seed={seed}: {type(e).__name__}: {e}", file=sys.stderr)
            continue
        row.update(commit=commit, time=datetime.datetime.now().isoformat(timespec="seconds"))
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(row) + "\n")
        shown = {k: round(v, 4) for k, v in row.items() if k in ("rmse", "test_acc", "method_seconds")}
        print(f"  {dataset} {mechanism} {rate} seed={seed}: {shown}")
    print(f"results: {out.relative_to(ROOT)}" + (f"  ({failures} cells failed)" if failures else ""))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
