# PaGNN: Incomplete Graph Representation and Learning via Partial Graph Neural Networks

| | |
|---|---|
| Authors | Jiang et al. |
| Year | 2021 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | arXiv 2021 |
| Official code | https://github.com/yaya1015/PaGCN |
| PDF (private, not in repo) | `SELECTED/Jiang 2021 -- PaGNN -- Incomplete Graph Representation and Learning via Partial GNNs -- R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **2 - feasible with caveats** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, AmaPhoto, AmaComp
- Open data: yes
- Notes: Simple partial-aggregation layer, a standard baseline. Use the authors' PaGCN repo (journal version, see zhang2024-pagc); the FP repo also contains a reimplementation. Do this and zhang2024-pagc as one unit.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
