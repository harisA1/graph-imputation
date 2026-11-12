# GRIOT: Reconstructing the Unseen: GRIOT for Attributed Graph Imputation with Optimal Transport

| | |
|---|---|
| Authors | Serrano et al. |
| Year | 2024 |
| Category | A - missing node attributes |
| Priority | 5 |
| Venue | ECML PKDD 2024 |
| Official code | https://github.com/RichardSrn/GRIOT |
| PDF (private, not in repo) | `SELECTED/Serrano 2024 -- Reconstructing the unseen -- GRIOT for attributed graph imputation with optimal transport -- R SEE+++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed variants, WikiCS-type graphs, synthetic SBM
- Open data: yes
- Notes: Priority 5, official code, public data. Needs POT. OT cost is quadratic in nodes, so PubMed-size runs are slow; the repo is ~130 MB.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
