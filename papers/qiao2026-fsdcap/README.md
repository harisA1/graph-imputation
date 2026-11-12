# FSD-CAP: Fractional Subgraph Diffusion with Class-Aware Propagation for Graph Feature Imputation

| | |
|---|---|
| Authors | Qiao et al. |
| Year | 2026 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | ICLR 2026 |
| Official code | https://github.com/ssjcode/FSD-CAP |
| PDF (private, not in repo) | `SELECTED/Qiao 2026 --FSD-CAP -FRACTIONAL SUBGRAPH DIFFUSION WITH with CLASS - AWARE PROPAGATION FOR GRAPH FEATURE IMPUTATION -- R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed, Photo, Computers, heterophilic sets, ogbn-arxiv (all via PyG)
- Open data: yes
- Notes: Official code with seeds. Recent and strong venue; compares against FP, PCFI, PaGCN, ITR, so it doubles as a check of our baselines.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
