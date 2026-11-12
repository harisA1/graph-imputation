# FISF, "Propagate and Inject" (Um et al., ICML 2025): reproduction report

**Verdict: reproduced, with validation tuning (v2).** With the paper's light hyper-parameter search, all ten headline numbers (5 datasets, 2 missingness types, 99.5% missing) are within 1.4 points of the paper, and seven of the ten within 1 point; our numbers are consistently slightly below the paper's. The paper's main claim holds in our runs: when whole nodes have no features, FISF clearly beats FP and PCFI on the citation graphs. On the Amazon graphs its advantage over tuned PCFI is small.

- Paper: *Propagate and Inject: Revisiting Propagation-Based Feature Imputation for Graphs with Partially Observed Features*, Um, Kim, Park, Lim, Ahn, Park. [Official code](https://github.com/daehoum1/fisf).
- Implementation: [`papers/um2025-propinject`](../papers/um2025-propinject/) (2026-11-12).
  - [`v1`](../papers/um2025-propinject/v1/): the method with `alpha = 0.9`, `beta = 0.9`, `gamma = 0.7` (code defaults), 100 diffusion steps, all channels processed at once (about 0.1 s per graph).
  - [`v2`](../papers/um2025-propinject/v2/): v1 with the paper's light search (appendix C.7): `alpha = beta` in {0.1, 0.3, 0.5, 0.7, 0.9} and `gamma` in {0.1, 0.3, 0.5, 0.7, 0.9}, chosen per run by validation accuracy (25 candidates, about 3 minutes per run).
- Numbers are test accuracy (%) of the shared-protocol GCN on the imputed features, mean ± standard deviation over 10 random splits, largest connected component.

## Comparison with the paper at 99.5% missing

| Dataset | Missing | v1 (defaults) | v2 (tuned) | Paper |
|---|---|---|---|---|
| Cora | structural | 77.55 ± 1.24 | 77.96 ± 1.38 | 79.29 ± 1.72 |
| | uniform | 78.49 ± 1.02 | 78.25 ± 0.95 | 79.09 ± 1.73 |
| CiteSeer | structural | 68.91 ± 1.08 | 68.57 ± 1.23 | 69.68 ± 2.47 |
| | uniform | 69.16 ± 1.38 | 69.33 ± 1.50 | 69.52 ± 1.81 |
| PubMed | structural | 75.64 ± 2.14 | 76.61 ± 1.02 | 76.90 ± 1.50 |
| | uniform | 75.95 ± 2.11 | 76.85 ± 1.32 | 77.53 ± 1.28 |
| Photo | structural | 86.26 ± 1.51 | 87.18 ± 1.27 | 88.22 ± 0.79 |
| | uniform | 87.64 ± 1.44 | 88.11 ± 1.36 | 88.32 ± 1.37 |
| Computers | structural | 76.52 ± 1.58 | 78.99 ± 1.55 | 79.40 ± 1.11 |
| | uniform | 81.14 ± 1.97 | 81.95 ± 1.08 | 82.12 ± 0.51 |

## The paper's claim, in our runs

Structural missingness, 99.5% of nodes without features, all methods through the same pipeline:

| Dataset | FP | PCFI (tuned) | FISF (tuned) |
|---|---|---|---|
| Cora | 72.45 | 74.20 | **77.96** |
| CiteSeer | 61.73 | 64.51 | **68.57** |
| PubMed | 73.25 | 75.22 | **76.61** |
| Photo | 86.22 | 87.00 | **87.18** |
| Computers | 76.60 | 78.38 | **78.99** |

The ordering FP < PCFI < FISF holds on every dataset. On the citation graphs the gains are large (5.5 points over FP on Cora, 6.8 on CiteSeer) and agree with the paper. On Photo and Computers FISF is ahead of tuned PCFI by 0.2 and 0.6 points, well inside the standard deviation; the paper reports similarly small margins there (0.7 and 0.4).

## What we learned

- On the citation graphs the defaults are already close to the tuned result; the search mostly keeps `alpha = beta` between 0.5 and 0.9.
- On Photo and Computers the search most often picks `alpha = beta = 0.1`, the same direction as tuned PCFI on these graphs: trust nearby observed values strongly.
- Under uniform missingness all propagation methods are within about a point of each other at this rate; the differences between them are a structural-missingness phenomenon.

Full tables for all rates (v1) are in the [leaderboard](comparisons/leaderboard.md); v2 was run at 99.5% only.

## Deviations and limits

- The light search (25 combinations with `alpha = beta`) instead of the full 125-combination grid; selection is per run (split and mask) rather than per dataset.
- The injected node and value are drawn from our seed; in the authors' code an injected value can overwrite an observed feature, whereas our pipeline always keeps observed features.
- The paper averages 5 splits, we use 10; the authors' code defaults to a 3-layer GCN, we use the shared 2-layer GCN.
- OGBN-Arxiv and link prediction are not reproduced.
