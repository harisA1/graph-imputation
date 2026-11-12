"""Reference baselines that belong to no paper. They anchor every comparison table and
exercise the pipeline. Run with `--paper baseline-<name> --version v1`."""
from __future__ import annotations

import torch

from .downstream import normalized_adjacency
from .methods import Method, Output


class Zero(Method):
    """Missing entries stay zero."""

    def run(self, data, observed, seed):
        return Output(x_hat=data.x.clone())


class Mean(Method):
    """Each missing entry gets the mean of the observed entries of its feature."""

    def run(self, data, observed, seed):
        obs = observed.float()
        mean = (data.x * obs).sum(0) / obs.sum(0).clamp(min=1)
        return Output(x_hat=torch.where(observed, data.x, mean.expand_as(data.x)))


class NeighborMean(Method):
    """Each missing entry gets the mean of that feature over neighbours where it is observed;
    falls back to the feature mean when no neighbour has it."""

    def run(self, data, observed, seed):
        n = data.num_nodes
        row, col = data.edge_index
        adj = torch.sparse_coo_tensor(data.edge_index, torch.ones(row.numel(), device=data.x.device), (n, n)).coalesce()
        obs = observed.float()
        num = torch.sparse.mm(adj, data.x * obs)
        den = torch.sparse.mm(adj, obs)
        mean = (data.x * obs).sum(0) / obs.sum(0).clamp(min=1)
        fill = torch.where(den > 0, num / den.clamp(min=1), mean.expand_as(data.x))
        return Output(x_hat=torch.where(observed, data.x, fill))


BASELINES = {"zero": Zero, "mean": Mean, "neighbor-mean": NeighborMean}
