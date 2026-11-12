# MIGDiff: Multi-Attribute Imputations for Attribute-Missing Graphs via Graph Denoising Diffusion Model

| | |
|---|---|
| Authors | Liu et al. |
| Year | 2026 |
| Category | A - missing node attributes |
| Priority | 5 |
| Venue | AAAI 2026 |
| Official code | https://github.com/YeLiu-Lab/MIGDiff |
| PDF (private, not in repo) | `SELECTED/Liu 2026 -- MIGDiff - Multi-attributes Imputations for Attribute-missing Graphs via Graph  Denoising Diffusion Model R SEE+++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

TODO: what is missing (attributes / structure / views / labels), what the downstream task is.

## Method summary

TODO: the core idea in a few sentences, key equations with page references, training objective.

## Reported results (from the paper)

TODO: datasets, missing mechanism and rates, metrics, and the numbers to reproduce (table/figure and page).

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, Citeseer, Amazon-Computers, Amazon-Photo
- Open data: yes
- Notes: Priority 5, official code, small graphs. Diffusion sampling makes it slower than the propagation methods but well within one A40.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). No implementation yet.
