# FISF: Propagate and Inject: Revisiting Propagation-Based Feature Imputation for Graphs with Partially Observed Features

| | |
|---|---|
| Authors | Um et al. |
| Year | 2025 |
| Category | A - missing node attributes |
| Priority | 4 |
| Venue | ICML 2025 |
| Official code | https://github.com/daehoum1/fisf |
| PDF (private, not in repo) | `SELECTED/Um 2025 -- Propagate and Inject -- Revisiting propagation-based feature imputation for graphs with partially observed features -- R SEE++++.pdf` |

Status is tracked in [`papers/papers.csv`](../papers.csv).

## Problem setting

Same as Feature Propagation and PCFI: learning on a graph where most node features are missing (uniform or structural), evaluated at very high missing rates (99.5% and beyond).

## Method summary

The paper observes that propagation-based imputation produces *low-variance channels*: feature channels whose imputed values are nearly identical on every node (for instance when a channel has almost no observed entries), which contribute nothing to the downstream model. FISF (feature imputation with synthetic features) repairs them. It has no trainable parameters:

1. **Pre-diffusion.** Run PCFI's confidence-weighted diffusion on all channels.
2. **Select** the fraction `gamma` of channels with the lowest variance.
3. **Inject.** In each selected channel, assign a random value to one randomly chosen node and treat it as observed.
4. **Diffuse again** in those channels with a combined pseudo-confidence `alpha^S * beta^V` (`S`: distance to the nearest observed node, `V`: distance to the injected node), so the synthetic value spreads over the graph and gives the channel a structure that follows the graph.

Hyper-parameters: `alpha`, `beta` in {0.1, ..., 0.9} and `gamma` in {10%, ..., 90%}, tuned per dataset on the validation set in the paper; the authors' code defaults to 0.9, 0.9 and 0.7.

## Reported results (from the paper)

Test accuracy (%) at 99.5% missing, GCN downstream, 5 random splits (Table 1, mean ± standard deviation):

| Dataset | Structural: FP | Structural: PCFI | Structural: FISF | Uniform: FP | Uniform: PCFI | Uniform: FISF |
|---|---|---|---|---|---|---|
| Cora | 71.86 ± 2.82 | 74.62 ± 1.78 | 79.29 ± 1.72 | 77.58 ± 1.98 | 78.82 ± 1.48 | 79.09 ± 1.73 |
| CiteSeer | 58.61 ± 1.74 | 66.06 ± 3.26 | 69.68 ± 2.47 | 68.55 ± 2.33 | 68.94 ± 1.95 | 69.52 ± 1.81 |
| PubMed | 71.96 ± 3.06 | 74.47 ± 2.54 | 76.90 ± 1.50 | 72.62 ± 4.18 | 76.28 ± 2.52 | 77.53 ± 1.28 |
| Photo | 85.42 ± 3.16 | 87.49 ± 1.50 | 88.22 ± 0.79 | 87.50 ± 1.49 | 88.09 ± 1.41 | 88.32 ± 1.37 |
| Computers | 76.62 ± 1.94 | 79.02 ± 1.22 | 79.40 ± 1.11 | 80.75 ± 0.70 | 81.80 ± 0.71 | 82.12 ± 0.51 |

OGBN-Arxiv and the link-prediction results are not reproduced here yet.

## Reproduction suitability (assessed 2026-11-12)

- Tier: **1 - start here** (see [`reports/reproduction-suitability.md`](../../reports/reproduction-suitability.md))
- Datasets in the paper: Cora, CiteSeer, PubMed, Photo, Computers, OGBN-Arxiv, synthetic
- Open data: yes
- Notes: Official code (FISF, Apache-2.0). Natural follow-up to PCFI; do the two together.

## Versions

See [`CHANGELOG.md`](CHANGELOG.md). Versions: [`v1`](v1/) (default settings), [`v2`](v2/) (validation-tuned). Reproduction report: [`reports/um2025-propinject.md`](../../reports/um2025-propinject.md).
