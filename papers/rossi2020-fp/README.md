# FP: On the Effectiveness of Feature Propagation in Graph Learning with Missing Node Attributes

| | |
|---|---|
| Authors | Rossi et al. |
| Year | 2020 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | LoG 2022 (arXiv 2021) |
| Official code | https://github.com/twitter-research/feature-propagation |
| PDF (private, not in repo) | `SELECTED/Rossi 2020 - FP -- On the Effectiveness of Feat Propagation in Graph Learning with Missing Node Attributes -- R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv, OGBN-Products
- Open data: yes
- Notes: The canonical baseline; almost every later paper compares with it. Trivial compute. Skip OGBN-Products/papers100M at first (large downloads).

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
