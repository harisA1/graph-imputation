# Conventions

## Paper directories

```
papers/<slug>/
  README.md        # paper card: citation, method summary, reported numbers, official code link, status
  CHANGELOG.md     # one entry per version: what changed and why
  v1/
    README.md      # how to run this version, deviations from the paper
    method.py      # one Method subclass (see gimpute/methods.py); method-specific code only
    configs/       # method settings (default.yaml), passed to the Method as self.config
    results/       # results.jsonl appended by the runner; backs the reports
  v2/ ...
```

Slug format: `<firstauthor><year>-<method>`, lowercase, hyphens only (e.g. `rossi2020-fp`). The slug is fixed once created; `papers.csv` is the source of truth.

## Versioning

Versions are kept side by side so any reported number can be regenerated.

- `v1` is the first implementation that follows the paper as closely as possible.
- A version is **frozen** once results from it appear in `reports/`. After that, any change that can alter results (model, training, hyper-parameters, data handling) goes into a copy, `vN+1/`, with a `CHANGELOG.md` entry.
- Pure bug fixes that do not change results, and documentation edits, may go into the existing version.
- When a version is frozen, tag the commit: `git tag <slug>/vN` and push the tag.
- Every result row records the git commit it was produced with.

## Shared evaluation protocol

Implemented in `gimpute/`; the grid is `configs/protocol.yaml`.

- A method never sees ground-truth features: it receives the masked features (missing = 0) and the bool mask, and returns imputed features, class scores, or both (`gimpute/methods.py`).
- Splits and masks depend only on the seed, so every method gets identical splits and identical missing entries.
- Missingness: `uniform` (each entry missing independently) and `structural` (whole nodes without features).
- Metrics: RMSE/MAE on missing entries; Recall@k and nDCG@k for binary features under structural missingness; node classification accuracy, using the method's own classifier if it has one and otherwise the standard GCN (`gimpute/downstream.py`) on its imputed features.
- Run a version: `python -m gimpute.run --paper <slug> --version vN` (resumable; one row per cell in `papers/<slug>/vN/results/results.jsonl`, with the git commit). Queue several: `python -m gimpute.queue add ...` then `python -m gimpute.queue work`.
- `python -m gimpute.report` rebuilds `reports/comparisons/leaderboard.md` from all results.
- `python tests/test_smoke.py` checks the shared layer on a synthetic graph; run it after changing `gimpute/`.

Paper-specific protocols are allowed **in addition** (as extra code in the version folder), to check that we match the paper's own numbers before comparing under the shared protocol.

## Status values (`papers.csv`)

`not-started` (candidate, not shown in the README), `next` (committed, up next), `in-progress`, `reproduced` (within reported variance), `partial` (runs, numbers off), `failed`, `skipped`.

## Priority (`papers.csv`)

Taken from Haris's filename markers (`SEE+++` = 3 ... `SEE+++++` = 5; 0 = unmarked). Higher means more important.
