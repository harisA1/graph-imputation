"""PCFI: pseudo-confidence-based feature imputation (Um et al., ICLR 2023), version 1.

Two stages, no trainable parameters:

1. Channel-wise inter-node diffusion. For every feature channel d, S[i, d] is the shortest-path
   distance from node i to the nearest node where d is observed, and alpha^S is the
   pseudo-confidence of the value recovered there. Features diffuse for K steps over the graph
   with self-loops, where a neighbour j contributes to node i with weight alpha^(S[j,d] - S[i,d])
   (row-normalised), and known entries are reset after every step. Because the factor that
   depends on i cancels in the row normalisation, one step is
       X <- (A+I)(P * X) / (A+I)P,   P = alpha^S,
   which lets all channels be processed at once instead of one channel at a time
   (gimpute/propagation.py).
2. Node-wise inter-channel propagation. With R the correlation matrix between recovered
   channels (diagonal zero) and m the channel means,
       X <- X + beta * (1 - P) * ((P * (X - m)) R),
   so low-confidence entries are corrected by high-confidence, correlated channels.

Checked against the authors' code (github.com/daehoum1/pcfi, Apache-2.0), including its
conventions: self-loops in the diffusion graph and distance 0 for nodes that cannot reach
any observed node.
"""
import torch

from gimpute.methods import Method, Output
from gimpute.propagation import adjacency_with_self_loops, confidence_diffusion, distance_to_observed


class PCFI(Method):
    def run(self, data, observed, seed):
        alpha = float(self.config.get("alpha", 0.9))
        beta = float(self.config.get("beta", 1.0))
        adj = adjacency_with_self_loops(data.edge_index, data.num_nodes)
        conf = alpha ** distance_to_observed(adj, observed)  # pseudo-confidence P
        x = confidence_diffusion(adj, data.x, observed, conf, int(self.config.get("num_iterations", 100)))

        corr = torch.corrcoef(x.T).nan_to_num()
        corr.fill_diagonal_(0)
        x = x + beta * (1 - conf) * ((conf * (x - x.mean(dim=0))) @ corr)
        return Output(x_hat=x)
