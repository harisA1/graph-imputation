"""Metrics shared by all papers. Imputation metrics are computed on missing entries only."""
from __future__ import annotations

import torch


def rmse(x_hat: torch.Tensor, x: torch.Tensor, observed: torch.Tensor) -> float:
    m = ~observed
    return float(((x_hat[m] - x[m]) ** 2).mean().sqrt()) if m.any() else float("nan")


def mae(x_hat: torch.Tensor, x: torch.Tensor, observed: torch.Tensor) -> float:
    m = ~observed
    return float((x_hat[m] - x[m]).abs().mean()) if m.any() else float("nan")


def recall_ndcg_at_k(x_hat: torch.Tensor, x: torch.Tensor, observed: torch.Tensor, k: int):
    """Recall@k and nDCG@k for binary attributes, averaged over nodes whose features are entirely
    missing and that have at least one positive attribute (the SAT profiling protocol)."""
    rows = (~observed).all(dim=1) & (x.sum(dim=1) > 0)
    if not rows.any():
        return float("nan"), float("nan")
    truth = x[rows] > 0
    k = min(k, x.shape[1])
    top = x_hat[rows].topk(k, dim=1).indices
    hits = truth.gather(1, top).float()
    recall = (hits.sum(1) / truth.sum(1).clamp(min=1)).mean()
    discount = 1.0 / torch.log2(torch.arange(2, k + 2, device=x.device).float())
    dcg = (hits * discount).sum(1)
    ideal = torch.cumsum(discount, 0)[truth.sum(1).clamp(max=k) - 1]
    return float(recall), float((dcg / ideal).mean())


def accuracy(logits: torch.Tensor, y: torch.Tensor, mask: torch.Tensor) -> float:
    return float((logits[mask].argmax(1) == y[mask]).float().mean())
