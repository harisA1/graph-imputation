# MEGAE: Handling Missing Data via Max-Entropy Regularized Graph Autoencoder

| | |
|---|---|
| Authors | Gao et al. |
| Year | 2023 |
| Category | A - missing node attributes |
| Priority | 3 |
| Venue | AAAI 2023 |
| Official code | https://github.com/zqgao22/max-entropy-gae |
| PDF (private, not in repo) | `SELECTED/Gao 2023 -- MEGAE-Handling Missing Data via Max-Entropy Regularized Graph Autoencoder +SPECTRAL IMPUTATION-- R SEE+++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **2 - feasible with caveats** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, PubMed, AmaPhoto, plus multi-graph sets
- Open data: yes
- Notes: Official code, small (MIT). Spectral, eigendecomposition-based; fine on small graphs. Priority 3.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
