# PCFI: Confidence-Based Feature Imputation for Graphs with Partially Known Features

| | |
|---|---|
| Authors | Um et al. |
| Year | 2023 |
| Category | A - missing node attributes |
| Priority | 3 |
| Venue | ICLR 2023 |
| Official code | https://github.com/daehoum1/pcfi |
| PDF (private, not in repo) | `SELECTED/Um 2023 -- PCFI -- CONFIDENCE-BASED FEATURE IMPUTATION FOR GRAPHS WITH PARTIALLY KNOWN FEATURES -- R SEE+++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

Same as Feature Propagation: node classification (and link prediction) on a graph where most of the feature matrix is missing, either as random entries (*uniform*) or as whole nodes without features (*structural*). The paper concentrates on very high missing rates (99.5%).

## Method summary

PCFI (pseudo-confidence-based feature imputation) refines feature propagation with a notion of how trustworthy each recovered value is. It has no trainable parameters and two stages:

1. **Channel-wise inter-node diffusion.** For each feature channel, the *pseudo-confidence* of a node is `alpha^S`, where `S` is its shortest-path distance to the nearest node where that channel is observed. Features diffuse over the graph (with self-loops, row-normalised, known entries reset every step, 100 steps), and a node listens more to neighbours that are closer to an observed value than itself.
2. **Node-wise inter-channel propagation.** Within each node, low-confidence channels are corrected using high-confidence channels in proportion to the correlation between channels: `X <- X + beta * (1 - P) * ((P * (X - mean)) R)`, with `P` the pseudo-confidence and `R` the channel correlation matrix.

Hyper-parameters: `alpha` in (0, 1) and `beta` in (0, 1], tuned per dataset on the validation set in the paper (the chosen values are not listed); the authors' code defaults to `alpha = 0.9`, `beta = 1.0`.

## Reported results (from the paper)

Test accuracy (%) at 99.5% missing, GCN downstream, 10 random splits (Table 1, mean ± standard deviation):

| Dataset | Structural: FP | Structural: PCFI | Uniform: FP | Uniform: PCFI |
|---|---|---|---|---|
| Cora | 72.84 ± 2.85 | 75.49 ± 2.10 | 77.55 ± 2.01 | 78.53 ± 1.39 |
| CiteSeer | 59.76 ± 2.47 | 66.18 ± 2.75 | 68.00 ± 2.16 | 69.40 ± 1.85 |
| PubMed | 72.69 ± 2.66 | 74.66 ± 2.26 | 73.88 ± 2.35 | 76.44 ± 1.64 |
| Photo | 86.57 ± 1.50 | 87.70 ± 1.29 | 87.75 ± 1.07 | 88.60 ± 1.30 |
| Computers | 77.45 ± 1.59 | 79.25 ± 1.19 | 81.47 ± 0.91 | 81.79 ± 0.70 |

The paper tunes the learning rate and dropout of the classifier per setting as well; OGBN-Arxiv and the link-prediction results are not reproduced here yet.

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv (PyG)
- Open data: yes
- Notes: Official code (Apache-2.0), tiny, propagation-based. Priority 3 by marker, but it is a standard baseline and nearly free to run.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). Current: [`v1`](v1/).
