"""The standard downstream model: a 2-layer GCN trained on imputed features.

Every imputation method is scored with this same classifier, so differences in accuracy come
from the imputed features and not from the classifier. Pure torch (sparse matmul), no extra deps.
"""
from __future__ import annotations

import torch
import torch.nn.functional as F

from .data import GraphData
from .metrics import accuracy


def normalized_adjacency(edge_index: torch.Tensor, n: int, self_loops: bool = True) -> torch.Tensor:
    """Sparse D^-1/2 (A [+ I]) D^-1/2."""
    if self_loops:
        loops = torch.arange(n, device=edge_index.device)
        edge_index = torch.cat([edge_index, torch.stack([loops, loops])], dim=1)
    row, col = edge_index
    deg = torch.zeros(n, device=edge_index.device).scatter_add_(0, row, torch.ones(row.numel(), device=edge_index.device))
    w = deg.clamp(min=1).pow(-0.5)
    return torch.sparse_coo_tensor(edge_index, w[row] * w[col], (n, n)).coalesce()


class GCN(torch.nn.Module):
    def __init__(self, in_dim: int, hidden: int, out_dim: int, dropout: float):
        super().__init__()
        self.l1 = torch.nn.Linear(in_dim, hidden)
        self.l2 = torch.nn.Linear(hidden, out_dim)
        self.dropout = dropout

    def forward(self, x, adj):
        x = F.dropout(x, self.dropout, self.training)
        x = F.relu(torch.sparse.mm(adj, self.l1(x)))
        x = F.dropout(x, self.dropout, self.training)
        return torch.sparse.mm(adj, self.l2(x))


def train_gcn(data: GraphData, x: torch.Tensor, seed: int, hidden: int = 64, dropout: float = 0.5,
              lr: float = 0.01, weight_decay: float = 5e-4, epochs: int = 500, patience: int = 100) -> dict:
    """Train on `x` (same device as `data`), early-stop on validation accuracy.
    Returns validation and test accuracy at the best validation epoch."""
    torch.manual_seed(seed)
    adj = normalized_adjacency(data.edge_index, data.num_nodes)
    model = GCN(x.shape[1], hidden, data.num_classes, dropout).to(x.device)
    opt = torch.optim.Adam(model.parameters(), lr=lr, weight_decay=weight_decay)
    best = {"val_acc": -1.0, "test_acc": float("nan")}
    wait = 0
    for _ in range(epochs):
        model.train()
        opt.zero_grad()
        F.cross_entropy(model(x, adj)[data.train_mask], data.y[data.train_mask]).backward()
        opt.step()
        model.eval()
        with torch.no_grad():
            logits = model(x, adj)
        val = accuracy(logits, data.y, data.val_mask)
        if val > best["val_acc"]:
            best = {"val_acc": val, "test_acc": accuracy(logits, data.y, data.test_mask)}
            wait = 0
        else:
            wait += 1
            if wait >= patience:
                break
    return best
