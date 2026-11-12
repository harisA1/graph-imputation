# DART: Mitigating Structural Overfitting: A Distribution-Aware Missing Feature Imputation via Two-step Reconstruction

| | |
|---|---|
| Authors | Song et al. |
| Year | 2026 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | KDD 2026 (to confirm) |
| Official code | https://github.com/yfsong00/DART |
| PDF (private, not in repo) | `SELECTED/Song 2026 - DART- Mitigating Struct Overfitting- A Distribution-Aware Missing Feature Imputation via Two-step Reconstruction + MAE-R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, PubMed, ogbn-arxiv, Flickr, Reddit, and their new Sailing dataset
- Open data: yes
- Notes: Official code and data (MIT). Reddit is the only larger set (a few GB); the rest is small. Introduces a dataset with naturally missing features.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
