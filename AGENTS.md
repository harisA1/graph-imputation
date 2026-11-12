# Handover for agents

Read this before changing anything. It is the working contract for any agent (or person) picking up this repo.

## What this project is

Reimplementing ~63 papers on imputation and learning with missing data on graphs, so they can be compared under one protocol. Owner: Haris (GitHub `harisA1`). Repo: https://github.com/harisA1/graph-imputation (public).

## Current state (keep this section up to date)

- 2026-11-12: skeleton created. No datasets downloaded, no implementations. `gimpute/` holds empty stubs only.
- Calypso work folder: `/home/jupyter-haris/graph-imputation` (a clone of this repo), created by Haris and writable by `administrator` via ACL. Verified working 2026-11-12.
- 2026-11-12: every paper assessed for reproduction suitability, see [`reports/reproduction-suitability.md`](reports/reproduction-suitability.md) and the `code_url` / `open_data` / `repro_tier` columns in `papers.csv`. Official code exists for 35 of 63; start with the tier-1 papers.
- Next: choose datasets and define the shared protocol in `gimpute/` and `configs/`, then start on the priority-5 papers.

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

1. Read the paper (PDF in `SELECTED/`, filename in `papers.csv`) and the paper's `README.md`.
2. Copy `papers/_template/v1/` into `papers/<slug>/v1/`.
3. Fill in the method summary and the paper's reported numbers in `papers/<slug>/README.md` before writing code.
4. Implement against `gimpute` interfaces; run on calypso; write `reports/<slug>.md`.
5. Set `status` in `papers.csv` (`not-started` → `in-progress` → `reproduced` / `partial` / `failed`), rebuild the index, commit, push.
