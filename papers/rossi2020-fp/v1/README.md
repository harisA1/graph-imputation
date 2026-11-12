# Feature Propagation, v1

A direct implementation of Algorithm 1 of the paper in [`method.py`](method.py): 40 iterations of diffusion with `D^-1/2 A D^-1/2`, resetting the known entries after every step.

```bash
python -m gimpute.run --paper rossi2020-fp --version v1 --seeds 0-9
```

The shared protocol (`configs/protocol.yaml`) was set up to match this paper's experimental setting, so the shared-protocol numbers are also the numbers to compare with the paper.

## Deviations from the paper

- The downstream GCN is this repository's own (`gimpute/downstream.py`), not PyTorch Geometric's `GCNConv`. It is the same model (2 layers, hidden 64, dropout 0.5, symmetric normalisation with self-loops) with the paper's training settings.
- The paper does not state whether the graph is restricted to its largest connected component; the authors' code does this, and so do we.
- Random splits and masks are our own seeds, so individual runs differ from the authors'; only the averages are comparable.
- OGBN-Arxiv and OGBN-Products are not run yet.
