# FP: On the Unreasonable Effectiveness of Feature Propagation in Learning on Graphs with Missing Node Features

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

Node classification on a graph where part of the node feature matrix is missing. Two patterns are studied: *uniform* (every entry of the feature matrix is missing independently with the same probability) and *structural* (a fraction of nodes has no features at all). The graph structure and the training labels are fully known.

## Method summary

Feature Propagation (FP) fills in the missing features before any learning happens. It minimises the Dirichlet energy of the features on the graph (missing values should be as smooth as possible given the known ones), which leads to a simple iteration (Algorithm 1):

1. Start with missing entries at zero.
2. Multiply the feature matrix by the symmetrically normalised adjacency `D^-1/2 A D^-1/2`.
3. Reset the known entries to their true values.
4. Repeat 40 times.

Each feature channel diffuses independently. There are no trainable parameters; a standard GNN (GCN in the main results) is then trained on the reconstructed features.

## Reported results (from the paper)

Test accuracy of FP followed by a 2-layer GCN, uniform missingness, mean over 10 random splits (Table 1):

| Dataset | Full features | 50% missing | 90% missing | 99% missing |
|---|---|---|---|---|
| Cora | 80.39 | 79.70 | 79.77 | 78.22 |
| CiteSeer | 67.48 | 65.74 | 65.57 | 65.40 |
| PubMed | 77.36 | 76.68 | 75.85 | 74.29 |
| Photo | 91.73 | 91.29 | 89.48 | 87.73 |
| Computers | 85.65 | 84.77 | 82.71 | 80.94 |

Setup stated in the paper: 20 training nodes per class, 1500 validation nodes, rest test; Adam, learning rate 0.005, at most 10000 epochs, early stopping with patience 200; 2 layers, hidden size 64, dropout 0.5; no hyper-parameter tuning. The paper also reports OGBN-Arxiv and OGBN-Products, which are not reproduced here yet.

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv, OGBN-Products
- Open data: yes
- Notes: The canonical baseline; almost every later paper compares with it. Trivial compute. Skip OGBN-Products/papers100M at first (large downloads).

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). Current: [`v1`](v1/). Reproduction report: [`reports/rossi2020-fp.md`](../../reports/rossi2020-fp.md).
