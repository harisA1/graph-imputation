# Handover for agents

Read this before changing anything. It is the working contract for any agent (or person) picking up this repo.

## What this project is

Reimplementing ~63 papers on imputation and learning with missing data on graphs, so they can be compared under one protocol. Owner: Haris (GitHub `harisA1`). Repo: https://github.com/harisA1/graph-imputation (public).

## Current state (keep this section up to date)

- Calypso work folder `/home/jupyter-haris/graph-imputation` (a clone of this repo), writable by `administrator` via ACL. `torch_geometric` and `POT` are installed in the `haris` env. Datasets (Cora, CiteSeer, PubMed, Photo, Computers) are in `data/` there.
- Every paper was assessed for reproduction suitability: [`reports/reproduction-suitability.md`](reports/reproduction-suitability.md), columns `venue` / `code_url` / `open_data` / `repro_tier` in `papers.csv`.
- Shared layer (`gimpute/`) is complete and in use; the protocol follows the Feature Propagation setting (`configs/protocol.yaml`).
- **Done:** Feature Propagation `rossi2020-fp/v1` reproduced ([report](reports/rossi2020-fp.md), tag `rossi2020-fp/v1`).
- **In progress (2026-11-12):** PCFI `um2023-pcfi` and FISF `um2025-propinject`. v1 of both (authors' default hyper-parameters) is run and reported, partially reproducing the papers. v2 of both (validation-tuned through `gimpute/tuning.py`) was queued on calypso at rate 0.995, 10 seeds; when it finishes: copy `papers/*/v2/results/results.jsonl` back, run `python -m gimpute.report`, update the two reports and changelogs, set the status in `papers.csv`.
- **Next:** SAT (`chen2022-sat`), the first trained model and the first to use the Recall@k / nDCG@k profiling metrics. After that, ask Haris which papers to take on.
- Three reference baselines (zero, mean, neighbour mean) are run on the full grid; results in `reports/baselines/`, comparison in [`reports/comparisons/leaderboard.md`](reports/comparisons/leaderboard.md).
- The README lists only papers with status other than `not-started`. Haris was asked whether to remove the placeholder folders of unstarted papers from the public repo; no answer yet, so leave them.
- The laptop has no Python. Run scripts, tests and experiments in the calypso clone. `administrator` cannot push from calypso: copy generated files back to the laptop clone (`ssh ... cat file > file`), commit and push there, then delete the copies on calypso and `git pull`.
- Several queue workers can run side by side (`python -m gimpute.queue work <slot>`); jobs here use about 1 GB of GPU memory each.
- Paper PDFs cannot be read on the laptop (no PDF tools). Pipe them to calypso and extract text with pdfminer in the `haris` env; do not store the PDF or its text in the repo.

## Where things are

| Thing | Location |
|---|---|
| Paper PDFs | Haris's laptop, `C:\Users\theoc\graph imputation\SELECTED\` (git-ignored, **never commit**; the repo is public and the PDFs are copyrighted) |
| Laptop working copy | `C:\Users\theoc\graph imputation\` (this repo; `SELECTED/` sits beside the tracked files) |
| Server working copy | `calypso:/home/jupyter-haris/graph-imputation` |
| Python env | `haris` conda env on calypso, see [`docs/compute.md`](docs/compute.md) |
| Catalogue | [`papers/papers.csv`](papers/papers.csv) → regenerate [`papers/INDEX.md`](papers/INDEX.md) with `scripts/build_index.py` |

## Rules

1. **Stay inside the dedicated folders**: the laptop folder, `~/graph-imputation` on calypso, and this repo. Do not write elsewhere on calypso (the root disk is ~98% full and the server is shared).
2. **Use the `haris` env** for every dependency. Do not create new envs. Install with `pip install --user` only after telling Haris what you are adding, and record it in `requirements.txt`.
3. **Never commit PDFs, datasets, checkpoints or large outputs.** `data/` and `runs/` are git-ignored. Small result tables (CSV/JSON under `papers/<slug>/vN/results/`) and figures for reports are fine.
4. **Versions are never overwritten.** Follow [`docs/conventions.md`](docs/conventions.md): once a version has reported results it is frozen; changes go into a new `vN+1/`.
5. **Shared code goes in `gimpute/`**, not copied between papers. Paper-specific code stays in its own directory.
6. **Report for humans** in `reports/`: what was run, the numbers, how they compare with the paper's, and any deviation from the paper.
7. Update the *Current state* section above and the paper's `status` in `papers.csv` whenever you finish a unit of work.

## How to start a paper

1. Read the paper (PDF in `SELECTED/`, filename in `papers.csv`), the paper's `README.md`, and the official code if `code_url` is set.
2. Fill in the method summary and the paper's reported numbers in `papers/<slug>/README.md` before writing code.
3. Copy `papers/_template/v1/` into `papers/<slug>/v1/` and implement one `Method` subclass in `method.py` (interface: `gimpute/methods.py`; examples: `gimpute/baselines.py`). Put anything reusable by other papers into `gimpute/`.
4. On calypso: `python -m gimpute.run --paper <slug> --version v1 --datasets cora --seeds 0` to check, then queue the full grid with `python -m gimpute.queue add --paper <slug> --version v1` and `python -m gimpute.queue work`.
5. First match the paper's own numbers under the paper's own setting (document how in the version README), then report the shared-protocol numbers. Write `reports/<slug>.md` and run `python -m gimpute.report`.
6. Set `status` in `papers.csv` (`not-started` → `in-progress` → `reproduced` / `partial` / `failed`), run `scripts/build_index.py`, add a `CHANGELOG.md` entry, commit, push, tag `<slug>/v1` when frozen.
