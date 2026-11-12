# PCFI (Um et al., ICLR 2023): reproduction report

**Verdict: reproduced, with validation tuning (v2).** With `alpha` and `beta` selected on the validation set as in the paper, all ten headline numbers (5 datasets, 2 missingness types, 99.5% missing) are within 1.7 points of the paper, and eight of the ten within 1 point, which is inside one standard deviation of the runs. With the fixed defaults of the authors' code (v1) the citation graphs are close but Photo and Computers fall 1.4 to 6.5 points short: the tuning is part of the method.

- Paper: *Confidence-Based Feature Imputation for Graphs with Partially Known Features*, Um, Park, Park, Choi. [Official code](https://github.com/daehoum1/pcfi).
- Implementation: [`papers/um2023-pcfi`](../papers/um2023-pcfi/) (2026-11-12).
  - [`v1`](../papers/um2023-pcfi/v1/): the method with `alpha = 0.9`, `beta = 1.0` (code defaults), 100 diffusion steps. The authors' code diffuses one feature channel at a time; ours processes all channels at once (checked to agree to 1e-6 with a literal implementation of the paper's equations), which brings the imputation to about 0.1 s per graph.
  - [`v2`](../papers/um2023-pcfi/v2/): v1 with `alpha` in {0.1, 0.3, 0.5, 0.7, 0.9} and `beta` in {1e-6, 1e-4, 1e-2, 1} chosen per run by validation accuracy (20 candidates, about 2 minutes per run).
- Numbers are test accuracy (%) of the shared-protocol GCN on the imputed features, mean ± standard deviation over 10 random splits, largest connected component.

## Comparison with the paper at 99.5% missing

| Dataset | Missing | v1 (defaults) | v2 (tuned) | Paper |
|---|---|---|---|---|
| Cora | structural | 74.16 ± 1.98 | 74.20 ± 2.08 | 75.49 ± 2.10 |
| | uniform | 76.88 ± 1.07 | 78.01 ± 0.91 | 78.53 ± 1.39 |
| CiteSeer | structural | 64.67 ± 2.25 | 64.51 ± 1.47 | 66.18 ± 2.75 |
| | uniform | 69.14 ± 1.33 | 69.54 ± 0.90 | 69.40 ± 1.85 |
| PubMed | structural | 74.15 ± 2.08 | 75.22 ± 1.74 | 74.66 ± 2.26 |
| | uniform | 75.00 ± 1.48 | 75.88 ± 1.48 | 76.44 ± 1.64 |
| Photo | structural | 81.20 ± 5.37 | 87.00 ± 1.15 | 87.70 ± 1.29 |
| | uniform | 87.19 ± 1.26 | 88.35 ± 1.19 | 88.60 ± 1.30 |
| Computers | structural | 73.76 ± 1.53 | 78.38 ± 1.23 | 79.25 ± 1.19 |
| | uniform | 78.46 ± 1.80 | 81.99 ± 1.24 | 81.79 ± 0.70 |

As a check of the setup itself, Feature Propagation run through the same pipeline matches the FP numbers that the PCFI paper reports at this rate (for example structural Cora 72.45 against 72.84, uniform Computers 80.99 against 81.47).

## What we learned

- **`beta` decides the Amazon results.** With `beta = 1` the second stage (inter-channel correction) is harmful on Photo and Computers at every missing rate: even with only 50% of features missing, v1 reaches 86.8 on Photo where FP and zero-filling reach 91.5. On Computers, and on Photo under structural missingness, the validation search most often picks `beta` of 1e-4 or 1e-6, which effectively switches that stage off, together with a small `alpha` (0.1 to 0.3). On the citation graphs the selected values are spread over the grid and matter much less.
- **On the citation graphs PCFI's gain over FP is largest under structural missingness** (CiteSeer at 99.5%: 64.5 against 61.7 for FP).
- The paper does not list the selected hyper-parameters, so a reader running the released code with its defaults will not get the paper's Amazon numbers.

Full tables for all rates (v1) are in the [leaderboard](comparisons/leaderboard.md); v2 was run at 99.5% only.

## Deviations and limits

- The tuning grid is a coarser subset of the paper's (20 instead of 117 combinations), and selection is per run (split and mask) rather than per dataset.
- The paper also tunes the classifier's learning rate and dropout and, in the authors' code, defaults to a 3-layer GCN; we use the shared 2-layer GCN with fixed settings.
- Random splits are redrawn per seed here; the authors' code inherits FP's fixed test set (see the [FP report](rossi2020-fp.md)).
- OGBN-Arxiv and link prediction are not reproduced.
