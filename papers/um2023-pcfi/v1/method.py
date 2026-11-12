"""PCFI: pseudo-confidence-based feature imputation (Um et al., ICLR 2023), version 1.

Two stages, no trainable parameters:

1. Channel-wise inter-node diffusion. For every feature channel d, S[i, d] is the shortest-path
   distance from node i to the nearest node where d is observed, and alpha^S is the
   pseudo-confidence of the value recovered there. Features diffuse for K steps over the graph
   with self-loops, where a neighbour j contributes to node i with weight alpha^(S[j,d] - S[i,d])
   (row-normalised), and known entries are reset after every step. Because the factor that
   depends on i cancels in the row normalisation, one step is
       X <- (A+I)(P * X) / (A+I)P,   P = alpha^S,
   which lets all channels be processed at once instead of one channel at a time.
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


def distance_to_observed(adj: torch.Tensor, observed: torch.Tensor) -> torch.Tensor:
    """S[i, d]: hops from node i to the nearest node with channel d observed (multi-source BFS
    for all channels at once). Unreachable entries keep distance 0, as in the authors' code."""
    reached = observed.clone()
    dist = torch.zeros(observed.shape, device=observed.device)
    step = 0
    while True:
        step += 1
        frontier = (torch.sparse.mm(adj, reached.float()) > 0) & ~reached
        if not frontier.any():
            return dist
        dist[frontier] = step
        reached |= frontier


class PCFI(Method):
    def run(self, data, observed, seed):
        alpha = float(self.config.get("alpha", 0.9))
        beta = float(self.config.get("beta", 1.0))
        n = data.num_nodes
        loops = torch.arange(n, device=data.x.device)
        ei = torch.cat([data.edge_index, torch.stack([loops, loops])], dim=1)
        adj = torch.sparse_coo_tensor(ei, torch.ones(ei.shape[1], device=data.x.device), (n, n)).coalesce()

        conf = alpha ** distance_to_observed(adj, observed)  # pseudo-confidence P
        denom = torch.sparse.mm(adj, conf)
        known = data.x
        x = known.clone()
        for _ in range(int(self.config.get("num_iterations", 100))):
            x = torch.sparse.mm(adj, conf * x) / denom
            x = torch.where(observed, known, x)

        corr = torch.corrcoef(x.T).nan_to_num()
        corr.fill_diagonal_(0)
        x = x + beta * (1 - conf) * ((conf * (x - x.mean(dim=0))) @ corr)
        return Output(x_hat=x)
