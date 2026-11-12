"""Feature Propagation (Rossi et al., LoG 2022), version 1.

Algorithm 1 of the paper: start with missing features at zero, repeatedly multiply by the
symmetrically normalised adjacency D^-1/2 A D^-1/2 (no self-loops) and reset the known entries
to their true values. Each feature channel diffuses independently, so entries can be missing
per node and per feature. There are no trainable parameters.
"""
import torch

from gimpute.downstream import normalized_adjacency
from gimpute.methods import Method, Output


class FeaturePropagation(Method):
    def run(self, data, observed, seed):
        adj = normalized_adjacency(data.edge_index, data.num_nodes, self_loops=False)
        known = data.x
        x = known.clone()  # missing entries are already zero
        for _ in range(int(self.config.get("num_iterations", 40))):
            x = torch.sparse.mm(adj, x)
            x = torch.where(observed, known, x)
        return Output(x_hat=x)
