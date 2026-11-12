# Conventions

## Paper directories

```
papers/<slug>/
  README.md        # paper card: citation, method summary, reported numbers, official code link, status
  CHANGELOG.md     # one entry per version: what changed and why
  v1/
    README.md      # how to run this version, deviations from the paper
    model.py       # method-specific code
    train.py       # entry point: python -m papers.<slug>.v1.train --config ...
    configs/       # YAML configs for this version
    results/       # small result tables (CSV/JSON) that back the reports
  v2/ ...
```

Slug format: `<firstauthor><year>-<method>`, lowercase, hyphens only (e.g. `rossi2020-fp`). The slug is fixed once created; `papers.csv` is the source of truth.

## Versioning

Versions are kept side by side so any reported number can be regenerated.

- `v1` is the first implementation that follows the paper as closely as possible.
- A version is **frozen** once results from it appear in `reports/`. After that, any change that can alter results (model, training, hyper-parameters, data handling) goes into a copy, `vN+1/`, with a `CHANGELOG.md` entry.
- Pure bug fixes that do not change results, and documentation edits, may go into the existing version.
- When a version is frozen, tag the commit: `git tag <slug>/vN` and push the tag.
- Every run writes its git commit hash and full config into its output folder under `runs/`.

## Shared evaluation protocol

Defined in `gimpute/` and `configs/` (to be written). Every paper should be evaluated on the same:

- datasets and splits,
- missingness mechanisms (e.g. uniform / structural node-attribute masking, missing edges) and rates,
- seeds (at least 5),
- metrics (imputation: RMSE/MAE, Recall@k / nDCG@k for binary attributes; downstream: node classification accuracy, clustering ACC/NMI/ARI).

Paper-specific protocols are allowed **in addition**, to check that we match the paper's own numbers.

## Status values (`papers.csv`)

`not-started`, `in-progress`, `reproduced` (within reported variance), `partial` (runs, numbers off), `failed`, `skipped`.

## Priority (`papers.csv`)

Taken from Haris's filename markers (`SEE+++` = 3 ... `SEE+++++` = 5; 0 = unmarked). Higher means more important.
