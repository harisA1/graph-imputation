# FISF, "Propagate and Inject" (Um et al., ICML 2025): reproduction report

**Verdict so far: partially reproduced (v1, untuned).** With the fixed default hyper-parameters of the authors' code, our implementation is within 0.4 to 1.6 points of the paper under uniform missingness and within 0.8 to 2.9 points under structural missingness. The paper's main claim is reproduced on the citation graphs: FISF clearly beats FP and PCFI when whole nodes have no features. On the Amazon graphs, untuned FISF only matches FP. The paper tunes three hyper-parameters per dataset; a tuned version (v2) is the next step.

- Paper: *Propagate and Inject: Revisiting Propagation-Based Feature Imputation for Graphs with Partially Observed Features*, Um, Kim, Park, Lim, Ahn, Park. [Official code](https://github.com/daehoum1/fisf).
- Implementation: [`papers/um2025-propinject/v1`](../papers/um2025-propinject/v1/) (2026-11-12), `alpha = 0.9`, `beta = 0.9`, `gamma = 0.7`, 100 diffusion steps, all channels processed at once (about 0.1 s per graph).
- Numbers are test accuracy (%) of the shared-protocol GCN on the imputed features, mean ± standard deviation over 10 random splits, largest connected component.

## Comparison with the paper at 99.5% missing

| Dataset | Structural: ours | Structural: paper | Uniform: ours | Uniform: paper |
|---|---|---|---|---|
| Cora | 77.55 ± 1.24 | 79.29 ± 1.72 | 78.49 ± 1.02 | 79.09 ± 1.73 |
| CiteSeer | 68.91 ± 1.08 | 69.68 ± 2.47 | 69.16 ± 1.38 | 69.52 ± 1.81 |
| PubMed | 75.64 ± 2.14 | 76.90 ± 1.50 | 75.95 ± 2.11 | 77.53 ± 1.28 |
| Photo | 86.26 ± 1.51 | 88.22 ± 0.79 | 87.64 ± 1.44 | 88.32 ± 1.37 |
| Computers | 76.52 ± 1.58 | 79.40 ± 1.11 | 81.14 ± 1.97 | 82.12 ± 0.51 |

## The paper's claim, in our runs

Structural missingness, 99.5% of nodes without features (ours, all three methods through the same pipeline):

| Dataset | FP | PCFI v1 | FISF v1 |
|---|---|---|---|
| Cora | 72.45 | 74.16 | **77.55** |
| CiteSeer | 61.73 | 64.67 | **68.91** |
| PubMed | 73.25 | 74.15 | **75.64** |
| Photo | 86.22 | 81.20 | **86.26** |
| Computers | **76.60** | 73.76 | 76.52 |

On the citation graphs the ordering FP < PCFI < FISF and the size of the gains (about 5 points over FP on Cora, 7 on CiteSeer) agree with the paper. On Photo and Computers the paper reports gains of 2.8 points over FP; untuned FISF gives none.

Full tables for all rates are in the [leaderboard](comparisons/leaderboard.md).

## Deviations and limits

- Fixed hyper-parameters instead of the paper's per-dataset grid search (`alpha`, `beta` in {0.1, ..., 0.9}, `gamma` in {10%, ..., 90%}); the selected values are not listed in the paper.
- The injected node and value are drawn from our seed; in the authors' code an injected value can overwrite an observed feature, whereas our pipeline always keeps observed features.
- The paper averages 5 splits, we use 10; the authors' code defaults to a 3-layer GCN, we use the shared 2-layer GCN.
- OGBN-Arxiv and link prediction are not reproduced.
