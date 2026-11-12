# PCFI (Um et al., ICLR 2023): reproduction report

**Verdict so far: partially reproduced (v1, untuned).** With the fixed default hyper-parameters of the authors' code, our implementation is within about 1.7 points of the paper on the three citation graphs but 1.4 to 6.5 points below it on the two Amazon graphs. The paper tunes `alpha` and `beta` per dataset on the validation set; the results below indicate that this tuning, and `beta` in particular, is what the Amazon numbers depend on. A tuned version (v2) is the next step.

- Paper: *Confidence-Based Feature Imputation for Graphs with Partially Known Features*, Um, Park, Park, Choi. [Official code](https://github.com/daehoum1/pcfi).
- Implementation: [`papers/um2023-pcfi/v1`](../papers/um2023-pcfi/v1/) (2026-11-12), `alpha = 0.9`, `beta = 1.0`, 100 diffusion steps. The authors' code diffuses one feature channel at a time; ours processes all channels at once (the two were checked to agree to 1e-6 against a literal implementation of the paper's equations), which brings the imputation to about 0.1 s per graph.
- Numbers are test accuracy (%) of the shared-protocol GCN on the imputed features, mean ± standard deviation over 10 random splits, largest connected component.

## Comparison with the paper at 99.5% missing

| Dataset | Structural: ours | Structural: paper | Uniform: ours | Uniform: paper |
|---|---|---|---|---|
| Cora | 74.16 ± 1.98 | 75.49 ± 2.10 | 76.88 ± 1.07 | 78.53 ± 1.39 |
| CiteSeer | 64.67 ± 2.25 | 66.18 ± 2.75 | 69.14 ± 1.33 | 69.40 ± 1.85 |
| PubMed | 74.15 ± 2.08 | 74.66 ± 2.26 | 75.00 ± 1.48 | 76.44 ± 1.64 |
| Photo | 81.20 ± 5.37 | 87.70 ± 1.29 | 87.19 ± 1.26 | 88.60 ± 1.30 |
| Computers | 73.76 ± 1.53 | 79.25 ± 1.19 | 78.46 ± 1.80 | 81.79 ± 0.70 |

As a check of the setup itself, Feature Propagation run through the same pipeline matches the FP numbers that the PCFI paper reports at this rate (for example structural Cora 72.45 against 72.84, uniform Computers 80.99 against 81.47), so the gap is specific to PCFI's settings and not to the data handling or the classifier.

## What the untuned version shows

- **On the citation graphs PCFI behaves as the paper describes.** It improves on FP most under structural missingness (CiteSeer at 99.5%: 64.7 against 61.7 for FP; at 90%: 69.3 against 67.9).
- **On Photo and Computers, `beta = 1` is harmful at every missing rate.** Even with only 50% of features missing, PCFI v1 reaches 86.8 on Photo where FP and even zero-filling reach 91.5. The second stage (inter-channel correction, scaled by `beta`) is the only part that can change values this much; the paper's search range for `beta` goes down to 1e-6, which effectively switches that stage off.

Full tables for all rates are in the [leaderboard](comparisons/leaderboard.md).

## Deviations and limits

- Fixed hyper-parameters instead of the paper's per-dataset grid search; the paper does not list the selected values.
- The paper also tunes the classifier's learning rate and dropout and, in the authors' code, defaults to a 3-layer GCN; we use the shared 2-layer GCN with fixed settings.
- Random splits are redrawn per seed here; the authors' code inherits FP's fixed test set (see the [FP report](rossi2020-fp.md)).
- OGBN-Arxiv and link prediction are not reproduced.
