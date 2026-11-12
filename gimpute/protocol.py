"""The shared evaluation protocol: one (dataset, mechanism, rate, seed) cell -> one result row.

For every cell:
  1. load the dataset with the split of that seed,
  2. build the seeded mask and hand the method only the masked features,
  3. score imputation on the missing entries (if the method returns features),
  4. score node classification: the method's own logits if it returns them, otherwise the
     standard GCN (gimpute.downstream) trained on its imputed features.
"""
from __future__ import annotations

import time

import torch

from . import metrics
from .data import load_dataset
from .downstream import train_gcn
from .masking import apply_mask, make_mask
from .methods import Method


def evaluate_cell(method: Method, dataset: str, mechanism: str, rate: float, seed: int, device: str,
                  protocol: dict | None = None) -> dict:
    """`protocol` is the dict from configs/protocol.yaml (keys used: largest_component, downstream)."""
    protocol = protocol or {}
    data = load_dataset(dataset, split_seed=seed, lcc=bool(protocol.get("largest_component", False)))
    observed = make_mask(data.num_nodes, data.x.shape[1], mechanism, rate, seed)
    truth = data.x.to(device)
    observed = observed.to(device)
    masked = data.with_features(apply_mask(data.x, observed.cpu())).to(device)

    torch.manual_seed(seed)
    start = time.time()
    out = method.run(masked, observed, seed)
    row = {"method_seconds": round(time.time() - start, 3)}

    if out.x_hat is not None:
        x_hat = torch.where(observed, truth, out.x_hat.detach().to(device))  # observed entries are known
        row["rmse"] = metrics.rmse(x_hat, truth, observed)
        row["mae"] = metrics.mae(x_hat, truth, observed)
        if data.binary_features and mechanism == "structural":
            for k in (10, 20, 50):
                row[f"recall@{k}"], row[f"ndcg@{k}"] = metrics.recall_ndcg_at_k(out.x_hat.detach().to(device), truth, observed, k)
    if out.logits is not None:
        logits = out.logits.detach().to(device)
        row["val_acc"] = metrics.accuracy(logits, masked.y, masked.val_mask)
        row["test_acc"] = metrics.accuracy(logits, masked.y, masked.test_mask)
        row["classifier"] = "own"
    elif out.x_hat is not None:
        row.update(train_gcn(masked, x_hat, seed, **protocol.get("downstream", {})))
        row["classifier"] = "gcn"
    if out.extra:
        row.update(out.extra)
    return row
