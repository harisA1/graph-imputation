# Handover for agents

Read this before changing anything. It is the working contract for any agent (or person) picking up this repo.

## What this project is

Reimplementing ~63 papers on imputation and learning with missing data on graphs, so they can be compared under one protocol. Owner: Haris (GitHub `harisA1`). Repo: https://github.com/harisA1/graph-imputation (public).

## Current state (keep this section up to date)

- 2026-11-12: skeleton created; calypso work folder `/home/jupyter-haris/graph-imputation` (a clone of this repo) created by Haris and writable by `administrator` via ACL.
- 2026-11-12: every paper assessed for reproduction suitability, see [`reports/reproduction-suitability.md`](reports/reproduction-suitability.md) and the `venue` / `code_url` / `open_data` / `repro_tier` columns in `papers.csv`. Official code exists for 35 of 63.
- 2026-11-12: shared layer written and tested on calypso with the synthetic graph and the three reference baselines (`python tests/test_smoke.py`; runner, resume, queue and leaderboard all exercised). **No paper implemented yet and no real dataset downloaded yet**: real datasets need `torch_geometric`, which is not installed in the `haris` env until Haris agrees.
- Next: install `torch_geometric`, run the baselines on the protocol grid, then implement **Feature Propagation (`rossi2020-fp`)** as the first paper, followed by PCFI and Propagate-and-Inject, then SAT.
- The laptop has no Python. Run scripts (`scripts/build_index.py`, tests, experiments) in the calypso clone. `administrator` cannot push from calypso, so copy generated files back to the laptop clone and commit there.

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
