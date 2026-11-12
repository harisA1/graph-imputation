"""Building blocks shared by the propagation-based imputation methods (PCFI, FISF, ...)."""
from __future__ import annotations

import torch


def adjacency_with_self_loops(edge_index: torch.Tensor, n: int) -> torch.Tensor:
    """Sparse binary A + I."""
    loops = torch.arange(n, device=edge_index.device)
    ei = torch.cat([edge_index, torch.stack([loops, loops])], dim=1)
    return torch.sparse_coo_tensor(ei, torch.ones(ei.shape[1], device=edge_index.device), (n, n)).coalesce()


def distance_to_observed(adj: torch.Tensor, observed: torch.Tensor) -> torch.Tensor:
    """S[i, d]: hops from node i to the nearest node where channel d is observed, by multi-source
    BFS on all channels at once. Entries that cannot reach an observed node keep distance 0
    (the convention of the PCFI and FISF reference code)."""
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


def confidence_diffusion(adj: torch.Tensor, known: torch.Tensor, observed: torch.Tensor,
                         conf: torch.Tensor, num_iterations: int) -> torch.Tensor:
    """Channel-wise diffusion where neighbour j contributes to node i in channel d with weight
    conf[j, d] / conf[i, d], row-normalised, and observed entries are reset after every step.
    The factor depending on i cancels in the normalisation, so one step is
        X <- adj (conf * X) / (adj conf),
    which handles every channel at once. `adj` must contain self-loops."""
    denom = torch.sparse.mm(adj, conf)
    x = torch.where(observed, known, torch.zeros_like(known))
    for _ in range(num_iterations):
        x = torch.sparse.mm(adj, conf * x) / denom
        x = torch.where(observed, known, x)
    return x
