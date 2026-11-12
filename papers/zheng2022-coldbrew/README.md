# Cold Brew: Distilling Graph Node Representations with Incomplete or Missing Neighborhoods

| | |
|---|---|
| Authors | Zheng et al. |
| Year | 2022 |
| Category | B - incomplete features and structure |
| Priority | 4 |
| Venue | ICLR 2022 |
| Official code | https://github.com/amazon-science/gnn-tail-generalization |
| PDF (private, not in repo) | `SELECTED/Zheng 2022 -- COLD BREW -- DISTILLING GRAPH NODE REPRESENTATIONS WITH INCOMPLETE OR MISSING NEIGHBORHOODS -- R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **2 - feasible with caveats** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, PubMed, ogbn-arxiv, Chameleon; plus 4 proprietary e-commerce sets
- Open data: partial
- Notes: Official code (Apache-2.0). Only the public-dataset tables are reproducible. About missing neighbourhoods (cold start), not missing attributes.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
