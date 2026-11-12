# Feature Propagation (Rossi et al., LoG 2022): reproduction report

**Verdict: reproduced.** Under the authors' own evaluation split, our implementation is within about one point of the paper's Table 1 on CiteSeer, PubMed, Photo and Computers, and 0.1 to 1.5 points above it on Cora. Under this repository's shared protocol the numbers differ more on the small graphs, and the reason is the split, not the method.

- Paper: *On the Unreasonable Effectiveness of Feature Propagation in Learning on Graphs with Missing Node Features*, Rossi, Kenlay, Gorinova, Chamberlain, Dong, Bronstein. [Official code](https://github.com/twitter-research/feature-propagation).
- Implementation: [`papers/rossi2020-fp/v1`](../papers/rossi2020-fp/v1/) (2026-11-12). The method is 40 iterations of feature diffusion with known entries reset after each step; it has no trainable parameters and takes a few milliseconds per graph on the GPU.
- All numbers are test accuracy (%) of a 2-layer GCN trained on the imputed features, mean ± standard error over 10 runs.

## 1. Paper setting (Table 1 of the paper)

Uniform missingness, the authors' split: one fixed set of 1500 "development" nodes; each run draws 20 training nodes per class from it, validates on the rest of it and tests on all remaining nodes. Run with [`paper_setting.py`](../papers/rossi2020-fp/v1/paper_setting.py).

| Dataset | | Full features | 50% missing | 90% missing | 99% missing |
|---|---|---|---|---|---|
| Cora | ours | 81.86 ± 0.37 | 80.76 ± 0.39 | 79.82 ± 0.35 | 78.88 ± 0.29 |
| | paper | 80.39 | 79.70 | 79.77 | 78.22 ± 0.32 |
| CiteSeer | ours | 67.61 ± 0.86 | 65.48 ± 0.88 | 65.40 ± 0.83 | 65.02 ± 0.47 |
| | paper | 67.48 | 65.74 | 65.57 | 65.40 |
| PubMed | ours | 77.33 ± 0.87 | 76.12 ± 0.98 | 75.91 ± 0.98 | 74.30 ± 0.70 |
| | paper | 77.36 | 76.68 | 75.85 | 74.29 |
| Photo | ours | 91.79 ± 0.28 | 91.46 ± 0.28 | 90.08 ± 0.39 | 88.33 ± 0.50 |
| | paper | 91.73 | 91.29 | 89.48 | 87.73 |
| Computers | ours | 84.93 ± 0.42 | 84.31 ± 0.46 | 82.65 ± 0.59 | 81.23 ± 0.53 |
| | paper | 85.65 | 84.77 | 82.71 | 80.94 |

The paper's central claim holds in our runs: with 99% of the features missing, accuracy drops by only 3 to 4 points relative to full features on every dataset.

## 2. Shared protocol

Same method and classifier, but a fresh random split for every seed (20 training nodes per class, 1500 validation nodes, all other nodes for testing), and both missingness mechanisms. Run with `python -m gimpute.run --paper rossi2020-fp --seeds 0-9`.

| Dataset | Full features | Uniform 50% | Uniform 90% | Uniform 99% | Structural 50% | Structural 90% | Structural 99% |
|---|---|---|---|---|---|---|---|
| Cora | 81.92 | 80.66 ± 0.49 | 79.40 ± 0.37 | 77.50 ± 0.31 | 80.02 ± 0.39 | 78.00 ± 0.40 | 74.28 ± 0.53 |
| CiteSeer | 70.44 | 68.21 ± 0.39 | 68.57 ± 0.31 | 68.32 ± 0.33 | 67.99 ± 0.53 | 67.94 ± 0.40 | 64.70 ± 0.70 |
| PubMed | 76.48 | 75.18 ± 0.72 | 74.57 ± 0.76 | 73.59 ± 0.74 | 74.87 ± 0.69 | 73.97 ± 0.85 | 73.36 ± 0.76 |
| Photo | 92.12 | 91.46 ± 0.14 | 89.91 ± 0.31 | 87.92 ± 0.48 | 91.47 ± 0.21 | 89.55 ± 0.24 | 87.20 ± 0.53 |
| Computers | 85.09 | 84.42 ± 0.42 | 83.06 ± 0.44 | 81.53 ± 0.47 | 84.39 ± 0.41 | 82.00 ± 0.30 | 78.45 ± 0.55 |

Comparison with other methods under this protocol is in the [leaderboard](comparisons/leaderboard.md).

## 3. What we learned

**The fixed test set matters on small graphs.** Before using the authors' split, our CiteSeer numbers were about 3 points *above* the paper's (68.3 against 65.4 at 99% missing), with the other datasets within 1.5 points. CiteSeer's largest connected component has 2120 nodes, so the authors' split leaves a single fixed test set of 620 nodes for all runs. Scoring on that particular set instead of averaging over random test sets accounts for the whole difference: with their split we get 65.0. Papers that reuse this code inherit the same test set, so their absolute numbers are comparable with each other but not with numbers from random splits. The shared protocol in this repository averages over random test sets.

**Details that are in the code but not in the paper.**
- The graph is restricted to its largest connected component. This is essential: on the full CiteSeer graph FP at 99% missing reaches only about 52%, because isolated components without any observed feature cannot be reconstructed.
- The authors' code adds self-loops to the graph before building the diffusion matrix, while the paper defines it without them. We follow the paper; in a side check the two variants differed by less than their standard errors on Cora and PubMed, and by about one standard error on CiteSeer.

## 4. Deviations and limits

- The downstream GCN is this repository's implementation (same architecture and training settings as the paper), not PyTorch Geometric's `GCNConv`.
- Masks are drawn from our own seeds; only averages are comparable with the paper.
- OGBN-Arxiv and OGBN-Products, the GraphSAGE variant, and the paper's other baselines (GCNMF, PaGNN, label propagation) are not reproduced here.
- The self-loop and full-graph observations above come from 5-seed side checks whose outputs are not stored in the repository.
