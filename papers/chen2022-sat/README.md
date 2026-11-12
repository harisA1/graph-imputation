# SAT: Learning on Attribute-Missing Graphs

| | |
|---|---|
| Authors | Chen et al. |
| Year | 2022 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | IEEE TPAMI 2022 |
| Official code | https://github.com/xuChenSJTU/SAT-master-online |
| PDF (private, not in repo) | `SELECTED/Chen 2022 IEEE-- SAT -- Learning on Attribute-Missing Graphs -- R  SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, PubMed, Steam, Amazon-Computers/Photo, Coauthor-CS
- Open data: yes
- Notes: The reference setting for attribute-missing graphs (Recall@k / nDCG@k profiling plus node classification). Its protocol is reused by ITR, SVGA, MATE, TDAR and others, so reproducing it first fixes the shared protocol.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
